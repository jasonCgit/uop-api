from app.mock_data import (
    APPS_REGISTRY,
    SEAL_COMPONENTS,
    COMPONENT_INDICATOR_MAP,
    COMPONENT_PLATFORM_EDGES,
    PLATFORM_NODE_MAP,
    DEPLOYMENT_OVERRIDES,
    APP_SLO_DATA,
    TEAMS,
)
from app.services.graph_engine import (
    NODE_MAP,
    COMPONENTS_WITH_INDICATORS,
    forward_adj,
    bfs,
    _effective_status,
)

# ── Mutable state ──────────────────────────────────────────────────────────────

# Enriched app cache — single source of truth for all dashboard endpoints
# Status is computed bottom-up from the enriched /api/applications/enriched logic.
# In production, _filter_dashboard_apps becomes a database query with WHERE clauses.
_enriched_cache: list[dict] | None = None

# In-memory map: app slug -> list of team IDs
# Seeded lazily on first enriched request (fallback in get_enriched_applications
# resolves app.team string -> team id when no explicit assignment exists)
APP_TEAM_ASSIGNMENTS: dict[str, list[int]] = {}

# Health indicator exclusions
APP_EXCLUDED_INDICATORS: dict[str, list[str]] = {}
DEPLOYMENT_EXCLUDED_INDICATORS: dict[str, list[str]] = {}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _app_slug(name: str) -> str:
    """Convert app name to a lookup slug (lowercase, spaces to hyphens)."""
    return name.lower().replace(" ", "-")


# Build component-to-platform lookup once
_comp_platform_map = {}
for _comp_id, _plat_id in COMPONENT_PLATFORM_EDGES:
    _comp_platform_map.setdefault(_comp_id, []).append(_plat_id)


# ── Enrichment pipeline ───────────────────────────────────────────────────────

def get_enriched_applications():
    """Return all apps enriched with components, deployments, SLO, and completeness."""
    from collections import OrderedDict

    APPS_BACKEND = APPS_REGISTRY

    _status_rank = {"critical": 0, "warning": 1, "healthy": 2, "no_data": 3}

    def _comp_slo(node, eff_status):
        """Compute deterministic component SLO from SLA target and effective status."""
        if eff_status == "no_data":
            return None
        try:
            target = float(node["sla"].replace("%", ""))
        except (ValueError, KeyError):
            target = 99.0
        if eff_status == "critical":
            return round(target - 1.5 - (node.get("incidents_30d", 0) * 0.08), 2)
        elif eff_status == "warning":
            return round(target - 0.4 - (node.get("incidents_30d", 0) * 0.05), 2)
        else:
            return round(target - 0.05, 2)

    def _build_comp_dict(cid):
        node = NODE_MAP.get(cid)
        if not node:
            return None
        eff = _effective_status(cid)
        return {
            "id": cid,
            "label": node["label"],
            "status": eff,
            "incidents_30d": node["incidents_30d"],
            "indicator_type": COMPONENT_INDICATOR_MAP.get(cid, "Service"),
            "slo": _comp_slo(node, eff),
        }

    results = []
    for app in APPS_BACKEND:
        slug = _app_slug(app["name"])

        # ── Exclusions for this app ──
        app_excl = set(APP_EXCLUDED_INDICATORS.get(slug, []))

        # Components from knowledge graph — SEAL_COMPONENTS is the single source of truth
        comp_ids = SEAL_COMPONENTS.get(app["seal"], [])
        components = []
        for cid in comp_ids:
            cd = _build_comp_dict(cid)
            if cd:
                components.append(cd)

        # Deployments: nest components under their platform
        plat_comp_map = {}  # plat_id -> [component dicts]
        plat_order = []     # preserve discovery order
        for cid in comp_ids:
            node = NODE_MAP.get(cid)
            if not node:
                continue
            for plat_id in _comp_platform_map.get(cid, []):
                if plat_id not in plat_comp_map:
                    plat_comp_map[plat_id] = []
                    plat_order.append(plat_id)
                cd = _build_comp_dict(cid)
                if cd:
                    plat_comp_map[plat_id].append(cd)
        deployments = []
        for plat_id in plat_order:
            pn = PLATFORM_NODE_MAP.get(plat_id)
            if not pn:
                continue
            dep_comps = plat_comp_map[plat_id]
            dep_comps.sort(key=lambda c: _status_rank.get(c["status"], 9))
            # Deployment exclusions = app-level + deployment-level
            dep_excl = app_excl | set(DEPLOYMENT_EXCLUDED_INDICATORS.get(f"{slug}:{plat_id}", []))
            active = [c for c in dep_comps if c["indicator_type"] not in dep_excl]
            # Status = worst of active RAG statuses
            # Empty deployments (no components) -> healthy; components with no indicators -> no_data
            rag_active = [c for c in active if c["status"] != "no_data"]
            if not dep_comps:
                worst = "healthy"
            elif not rag_active:
                worst = "no_data"
            else:
                worst = "healthy"
                for c in rag_active:
                    if _status_rank.get(c["status"], 9) < _status_rank.get(worst, 9):
                        worst = c["status"]
            # SLO = min of active component SLOs
            active_slos = [c["slo"] for c in active if c.get("slo") is not None]
            dep_slo = min(active_slos) if active_slos else None
            deployments.append({
                "id": plat_id,
                "label": pn["label"],
                "type": pn["type"],
                "datacenter": pn["datacenter"],
                "status": worst,
                "components": dep_comps,
                "slo": dep_slo,
                "excluded_indicators": list(DEPLOYMENT_EXCLUDED_INDICATORS.get(f"{slug}:{plat_id}", [])),
            })
        deployments.sort(key=lambda d: _status_rank.get(d["status"], 9))

        # Use deployment overrides if available — resolve component_ids to full data
        if slug in DEPLOYMENT_OVERRIDES:
            deployments = []
            for ovr in DEPLOYMENT_OVERRIDES[slug]:
                d = dict(ovr)
                comp_ids_list = d.pop("component_ids", [])
                dep_comps = []
                for cid in comp_ids_list:
                    cd = _build_comp_dict(cid)
                    if cd:
                        dep_comps.append(cd)
                dep_comps.sort(key=lambda c: _status_rank.get(c["status"], 9))
                dep_id = d.get("id", "")
                dep_excl = app_excl | set(DEPLOYMENT_EXCLUDED_INDICATORS.get(f"{slug}:{dep_id}", []))
                active = [c for c in dep_comps if c["indicator_type"] not in dep_excl]
                # Status = worst of active RAG statuses
                # Empty deployments (no components, e.g. DEV/UAT) -> healthy
                # Deployments with components but no indicators -> no_data
                rag_active = [c for c in active if c["status"] != "no_data"]
                if not dep_comps:
                    worst = "healthy"
                elif not rag_active:
                    worst = "no_data"
                else:
                    worst = "healthy"
                    for c in rag_active:
                        if _status_rank.get(c["status"], 9) < _status_rank.get(worst, 9):
                            worst = c["status"]
                d["status"] = worst
                d["components"] = dep_comps
                active_slos = [c["slo"] for c in active if c.get("slo") is not None]
                d["slo"] = min(active_slos) if active_slos else None
                d["excluded_indicators"] = list(DEPLOYMENT_EXCLUDED_INDICATORS.get(f"{slug}:{dep_id}", []))
                deployments.append(d)
            deployments.sort(key=lambda d: _status_rank.get(d["status"], 9))

        # SLO data — derive from deployment SLOs (bottom-up)
        dep_slos = [d["slo"] for d in deployments if d.get("slo") is not None]
        app_slo_current = min(dep_slos) if dep_slos else None
        base_slo = APP_SLO_DATA.get(slug, {
            "target": 99.0, "current": 99.5, "error_budget": 80,
            "trend": "stable", "burn_rate": "0.2x", "breach_eta": None, "status": "healthy",
        })
        slo = dict(base_slo)
        if app_slo_current is not None:
            slo["current"] = app_slo_current
            # Derive SLO status from current vs target
            target = slo.get("target", 99.0)
            if app_slo_current < target - 0.5:
                slo["status"] = "critical"
            elif app_slo_current < target:
                slo["status"] = "warning"
            else:
                slo["status"] = "healthy"

        # Completeness score
        has_owner = bool(app.get("appOwner"))
        has_sla = bool(app.get("sla"))
        has_slo = slug in APP_SLO_DATA
        has_rto = app.get("rto", "") not in ("", "NRR")
        has_cpof = app.get("cpof") == "Yes"
        has_blast_radius = len(comp_ids) > 0
        checks = [has_owner, has_sla, has_slo, has_rto, has_cpof, has_blast_radius]
        score = round(sum(checks) / len(checks) * 100)

        completeness = {
            "has_owner": has_owner,
            "has_sla": has_sla,
            "has_slo": has_slo,
            "has_rto": has_rto,
            "has_cpof": has_cpof,
            "has_blast_radius": has_blast_radius,
            "score": score,
        }

        # Resolve team references (multi-team)
        if slug not in APP_TEAM_ASSIGNMENTS:
            # Seed from team name string on first access
            team_name = app.get("team", "")
            matched_team = next((t for t in TEAMS if t["name"] == team_name), None)
            if matched_team:
                APP_TEAM_ASSIGNMENTS[slug] = [matched_team["id"]]
        assigned_ids = APP_TEAM_ASSIGNMENTS.get(slug, [])

        # Compute app-level status = worst of deployment statuses (bottom-up)
        if deployments:
            worst_app_rank = 3  # no_data
            for d in deployments:
                r = _status_rank.get(d.get("status", "no_data"), 3)
                if r < worst_app_rank:
                    worst_app_rank = r
            app_status = {0: "critical", 1: "warning", 2: "healthy", 3: "no_data"}[worst_app_rank]
        else:
            app_status = "healthy"

        results.append({
            **app,
            "id": slug,
            "status": app_status,
            "incidents_30d": app["incidents"],
            "components": components,
            "deployments": deployments,
            "slo": slo,
            "completeness": completeness,
            "team_ids": assigned_ids,
            "excluded_indicators": list(APP_EXCLUDED_INDICATORS.get(slug, [])),
        })

    return results


def _get_enriched_apps() -> list[dict]:
    """Return all apps with computed status from the enriched pipeline.
    Cached at module level since mock data is deterministic."""
    global _enriched_cache
    if _enriched_cache is not None:
        return _enriched_cache

    _status_rank = {"critical": 0, "warning": 1, "healthy": 2, "no_data": 3}
    _rank_to_status = {0: "critical", 1: "warning", 2: "healthy", 3: "no_data"}

    enriched = get_enriched_applications()
    # Build a lookup by seal for the enriched data (which has computed deployments)
    enriched_by_seal = {a["seal"]: a for a in enriched}

    dashboard_apps = []
    for app in APPS_REGISTRY:
        e = enriched_by_seal.get(app["seal"])
        # Derive status from deployments (worst of deployment statuses)
        if e and e.get("deployments"):
            worst_rank = 3  # no_data
            for d in e["deployments"]:
                r = _status_rank.get(d.get("status", "no_data"), 3)
                if r < worst_rank:
                    worst_rank = r
            computed_status = _rank_to_status[worst_rank]
        else:
            computed_status = "healthy"

        dashboard_apps.append({
            "seal": app["seal"],
            "name": app["name"],
            "lob": app["lob"],
            "subLob": app.get("subLob", ""),
            "cto": app.get("cto", ""),
            "cbt": app.get("cbt", ""),
            "region": app.get("region", "NA"),
            "status": computed_status,
            "incidents_30d": app.get("incidents", 0),
            "incidents_today": app.get("incidents_today", 0),
            "recurring_30d": app.get("recurring_30d", 0),
            "p1_30d": app.get("p1_30d", 0),
            "p2_30d": app.get("p2_30d", 0),
            "recent_issues": app.get("recent_issues", []),
        })

    _enriched_cache = dashboard_apps
    return _enriched_cache


def _filter_dashboard_apps(
    lob: list[str] | None = None,
    sub_lob: list[str] | None = None,
    cto: list[str] | None = None,
    cbt: list[str] | None = None,
    seal: list[str] | None = None,
    status: list[str] | None = None,
    search: str | None = None,
) -> list[dict]:
    """Filter enriched apps by the given scope params.
    In production this becomes a database query with WHERE clauses."""
    result = _get_enriched_apps()
    if lob:
        result = [a for a in result if a["lob"] in lob]
    if sub_lob:
        result = [a for a in result if a.get("subLob", "") in sub_lob]
    if cto:
        result = [a for a in result if a["cto"] in cto]
    if cbt:
        result = [a for a in result if a["cbt"] in cbt]
    if seal:
        result = [a for a in result if a["seal"] in seal]
    if status:
        result = [a for a in result if a["status"] in status]
    if search:
        q = search.lower()
        result = [a for a in result if q in a["name"].lower() or q in a.get("seal", "").lower()]
    return result


def _parse_filters(
    lob: list[str] | None = None,
    sub_lob: list[str] | None = None,
    cto: list[str] | None = None,
    cbt: list[str] | None = None,
    seal: list[str] | None = None,
    status: list[str] | None = None,
    search: str | None = None,
) -> dict:
    """Bundle filter params for passing to helper functions."""
    return {k: v for k, v in {
        "lob": lob, "sub_lob": sub_lob, "cto": cto, "cbt": cbt,
        "seal": seal, "status": status, "search": search,
    }.items() if v}
