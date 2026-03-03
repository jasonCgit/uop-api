# REAL: Replace with metrics database / data lake queries

"""
Deterministic mock data for the Outcome Measures page.

Every SEAL gets reproducible metrics derived from hashlib.md5(seal).
This ensures filters work naturally through the existing _filter_dashboard_apps pipeline.
"""

import hashlib
from .apps_registry import APPS_REGISTRY

# ── Helpers ───────────────────────────────────────────────────────────────────

def _seed(seal: str, salt: str = "") -> int:
    """Deterministic int seed from SEAL + salt."""
    return int(hashlib.md5(f"{seal}{salt}".encode()).hexdigest()[:8], 16)


def _pct(seed_val: int, lo: int, hi: int) -> float:
    """Map seed to a float in [lo, hi] with one decimal."""
    return round(lo + (seed_val % 1000) / 999 * (hi - lo), 1)


def _trend_12m(seed_val: int, baseline: float, current: float) -> list[float]:
    """Generate 12 monthly values trending from baseline toward current."""
    steps = 12
    result = []
    for i in range(steps):
        t = i / (steps - 1)
        noise = ((seed_val * (i + 1) * 7) % 100 - 50) / 500  # ±10% noise
        val = baseline + (current - baseline) * t + noise * abs(current - baseline + 1)
        result.append(round(max(0, val), 1))
    return result


MONTH_LABELS = [
    "Apr'25", "May'25", "Jun'25", "Jul'25", "Aug'25", "Sep'25",
    "Oct'25", "Nov'25", "Dec'25", "Jan'26", "Feb'26", "Mar'26",
]


# ── Section definitions ──────────────────────────────────────────────────────

SECTIONS = [
    {"id": 1, "key": "usage",       "label": "Usage & Adoption",          "short": "Usage"},
    {"id": 2, "key": "workstreams", "label": "Workstream Outcomes",       "short": "Workstreams"},
    {"id": 3, "key": "sre",         "label": "SRE Effectiveness",         "short": "SRE"},
    {"id": 4, "key": "support",     "label": "Traditional Support Impact","short": "Support"},
    {"id": 5, "key": "baselines",   "label": "Baselines & Coverage",      "short": "Baselines"},
]

WORKSTREAM_DEFS = [
    {"id": "golden_signals",     "label": "Golden Signal Monitoring",     "icon": "MonitorHeart"},
    {"id": "slo_mgmt",          "label": "SLO Management",               "icon": "Speed"},
    {"id": "incident_zero",     "label": "Incident Zero",                "icon": "Shield"},
    {"id": "blast_radius",      "label": "Blast Radius Analysis",        "icon": "AccountTree"},
    {"id": "zero_touch",        "label": "Zero-Touch M&O",               "icon": "SmartToy"},
    {"id": "sre_telemetry",     "label": "SRE Telemetry",                "icon": "Insights"},
    {"id": "aura_ai",           "label": "AURA AI Assistant",            "icon": "Psychology"},
    {"id": "knowledge_graph",   "label": "Knowledge Graph",              "icon": "Hub"},
]

# ── Per-SEAL metric generation ────────────────────────────────────────────────

def _generate_seal_metrics(seal: str) -> dict:
    """Generate all outcome metrics for a single SEAL."""
    s = _seed(seal)

    # Section 1: Usage & Adoption
    prompts_baseline = 10 + (s % 40)
    prompts_current = prompts_baseline + int(prompts_baseline * _pct(_seed(seal, "pr"), 50, 250) / 100)
    dau_baseline = 2 + (s % 8)
    dau_current = dau_baseline + int(dau_baseline * _pct(_seed(seal, "dau"), 20, 120) / 100)
    uop_views_baseline = 5 + (s % 30)
    uop_views_current = uop_views_baseline + int(uop_views_baseline * _pct(_seed(seal, "views"), 30, 180) / 100)
    feature_adoption = _pct(_seed(seal, "fa"), 35, 95)

    # Section 2: Workstreams — per-workstream adoption %
    ws = {}
    for w in WORKSTREAM_DEFS:
        ws_seed = _seed(seal, w["id"])
        ws[w["id"]] = {
            "adopted": ws_seed % 2 == 0,
            "maturity": _pct(ws_seed, 10, 100),
            "value_score": _pct(_seed(seal, w["id"] + "v"), 20, 100),
        }

    # Section 3: SRE Effectiveness
    mttr_baseline = 30 + (s % 90)  # minutes
    mttr_current = max(5, mttr_baseline - int(mttr_baseline * _pct(_seed(seal, "mttr"), 20, 65) / 100))
    p1_baseline = (s % 5)
    p1_current = max(0, p1_baseline - int(p1_baseline * _pct(_seed(seal, "p1r"), 10, 50) / 100))
    p2_baseline = (s % 8)
    p2_current = max(0, p2_baseline - int(p2_baseline * _pct(_seed(seal, "p2r"), 10, 45) / 100))
    noise_baseline = 50 + (s % 200)
    noise_current = noise_baseline + int(noise_baseline * _pct(_seed(seal, "noise"), -30, 80) / 100)
    true_impact_baseline = 45 + (s % 60)  # minutes
    true_impact_current = max(5, true_impact_baseline - int(true_impact_baseline * _pct(_seed(seal, "tid"), 20, 70) / 100))
    slo_compliance = _pct(_seed(seal, "slo"), 88, 99.9)
    error_budget = _pct(_seed(seal, "eb"), 40, 95)

    # Section 4: Support Impact
    service_requests_baseline = 5 + (s % 20)
    service_requests_current = max(0, service_requests_baseline - int(service_requests_baseline * _pct(_seed(seal, "sr"), 10, 55) / 100))
    self_service_pct = _pct(_seed(seal, "ss"), 30, 90)
    escalation_baseline = 3 + (s % 10)
    escalation_current = max(0, escalation_baseline - int(escalation_baseline * _pct(_seed(seal, "esc"), 15, 60) / 100))

    # Section 5: Coverage booleans
    has_golden_signals = _seed(seal, "gs") % 3 != 0  # ~67%
    has_slo = _seed(seal, "slo_cov") % 4 != 0  # ~75%
    has_incident_zero = _seed(seal, "iz") % 3 != 0
    has_blast_radius = _seed(seal, "br") % 5 < 2  # ~40%
    has_runbooks = _seed(seal, "rb") % 3 != 0
    has_day1 = _seed(seal, "d1") % 4 != 0

    return {
        "seal": seal,
        "usage": {
            "prompts":         {"baseline": prompts_baseline, "current": prompts_current, "trend": _trend_12m(_seed(seal, "ptr"), prompts_baseline, prompts_current)},
            "dau":             {"baseline": dau_baseline, "current": dau_current, "trend": _trend_12m(_seed(seal, "dtr"), dau_baseline, dau_current)},
            "uop_views":       {"baseline": uop_views_baseline, "current": uop_views_current, "trend": _trend_12m(_seed(seal, "vtr"), uop_views_baseline, uop_views_current)},
            "feature_adoption": {"baseline": 30.0, "current": feature_adoption, "trend": _trend_12m(_seed(seal, "fatr"), 30.0, feature_adoption)},
        },
        "workstreams": ws,
        "sre": {
            "mttr":            {"baseline": mttr_baseline, "current": mttr_current, "unit": "min", "trend": _trend_12m(_seed(seal, "mtr"), mttr_baseline, mttr_current), "lower_is_better": True},
            "p1_incidents":    {"baseline": p1_baseline, "current": p1_current, "unit": "count", "trend": _trend_12m(_seed(seal, "p1t"), p1_baseline, p1_current), "lower_is_better": True},
            "p2_incidents":    {"baseline": p2_baseline, "current": p2_current, "unit": "count", "trend": _trend_12m(_seed(seal, "p2t"), p2_baseline, p2_current), "lower_is_better": True},
            "noise_events":    {"baseline": noise_baseline, "current": noise_current, "unit": "count", "trend": _trend_12m(_seed(seal, "ntr"), noise_baseline, noise_current), "lower_is_better": True},
            "true_impact_dur": {"baseline": true_impact_baseline, "current": true_impact_current, "unit": "min", "trend": _trend_12m(_seed(seal, "ttr"), true_impact_baseline, true_impact_current), "lower_is_better": True},
            "slo_compliance":  {"baseline": 95.0, "current": slo_compliance, "unit": "%", "trend": _trend_12m(_seed(seal, "str"), 95.0, slo_compliance), "lower_is_better": False},
            "error_budget":    {"baseline": 60.0, "current": error_budget, "unit": "%", "trend": _trend_12m(_seed(seal, "etr"), 60.0, error_budget), "lower_is_better": False},
        },
        "support": {
            "service_requests":{"baseline": service_requests_baseline, "current": service_requests_current, "unit": "count/mo", "trend": _trend_12m(_seed(seal, "srtr"), service_requests_baseline, service_requests_current), "lower_is_better": True},
            "self_service_pct":{"baseline": 25.0, "current": self_service_pct, "unit": "%", "trend": _trend_12m(_seed(seal, "sstr"), 25.0, self_service_pct), "lower_is_better": False},
            "escalations":     {"baseline": escalation_baseline, "current": escalation_current, "unit": "count/mo", "trend": _trend_12m(_seed(seal, "estr"), escalation_baseline, escalation_current), "lower_is_better": True},
        },
        "coverage": {
            "golden_signals": has_golden_signals,
            "slo_defined": has_slo,
            "incident_zero": has_incident_zero,
            "blast_radius": has_blast_radius,
            "runbooks": has_runbooks,
            "day1_complete": has_day1,
        },
    }


# ── Pre-compute all SEAL metrics ─────────────────────────────────────────────

_ALL_SEAL_METRICS: dict[str, dict] | None = None

def get_all_seal_metrics() -> dict[str, dict]:
    """Return {seal: metrics_dict} for every app in APPS_REGISTRY.  Cached."""
    global _ALL_SEAL_METRICS
    if _ALL_SEAL_METRICS is not None:
        return _ALL_SEAL_METRICS
    _ALL_SEAL_METRICS = {}
    for app in APPS_REGISTRY:
        seal = app["seal"]
        _ALL_SEAL_METRICS[seal] = _generate_seal_metrics(seal)
    return _ALL_SEAL_METRICS


# ── Aggregation helpers (used by the router) ──────────────────────────────────

def _safe_pct_change(baseline: float, current: float) -> float:
    """Percentage change from baseline to current."""
    if baseline == 0:
        return 0.0 if current == 0 else 100.0
    return round((current - baseline) / baseline * 100, 1)


def aggregate_metrics(seal_list: list[str], section_key: str | None = None) -> dict:
    """Aggregate metrics across a list of SEALs.  Returns summary dicts per section."""
    all_m = get_all_seal_metrics()
    metrics = [all_m[s] for s in seal_list if s in all_m]
    if not metrics:
        return {}

    n = len(metrics)

    def _avg(vals):
        return round(sum(vals) / len(vals), 1) if vals else 0

    def _sum(vals):
        return sum(vals)

    def _avg_trend(trends):
        """Average 12-month trends across apps."""
        if not trends:
            return [0] * 12
        result = []
        for i in range(12):
            vals = [t[i] for t in trends if len(t) > i]
            result.append(round(sum(vals) / len(vals), 1) if vals else 0)
        return result

    def _sum_trend(trends):
        if not trends:
            return [0] * 12
        result = []
        for i in range(12):
            vals = [t[i] for t in trends if len(t) > i]
            result.append(round(sum(vals), 1))
        return result

    def _build_metric(values_b, values_c, trends, agg="sum", lower_is_better=False, unit=""):
        b = _sum(values_b) if agg == "sum" else _avg(values_b)
        c = _sum(values_c) if agg == "sum" else _avg(values_c)
        tr = _sum_trend(trends) if agg == "sum" else _avg_trend(trends)
        return {
            "baseline": b, "current": c, "pct_change": _safe_pct_change(b, c),
            "trend": tr, "lower_is_better": lower_is_better, "unit": unit,
        }

    result = {}

    # Section 1: Usage
    if section_key is None or section_key == "usage":
        result["usage"] = {
            "prompts": _build_metric(
                [m["usage"]["prompts"]["baseline"] for m in metrics],
                [m["usage"]["prompts"]["current"] for m in metrics],
                [m["usage"]["prompts"]["trend"] for m in metrics],
                agg="sum", unit="count"),
            "dau": _build_metric(
                [m["usage"]["dau"]["baseline"] for m in metrics],
                [m["usage"]["dau"]["current"] for m in metrics],
                [m["usage"]["dau"]["trend"] for m in metrics],
                agg="sum", unit="users"),
            "uop_views": _build_metric(
                [m["usage"]["uop_views"]["baseline"] for m in metrics],
                [m["usage"]["uop_views"]["current"] for m in metrics],
                [m["usage"]["uop_views"]["trend"] for m in metrics],
                agg="sum", unit="views/mo"),
            "feature_adoption": _build_metric(
                [m["usage"]["feature_adoption"]["baseline"] for m in metrics],
                [m["usage"]["feature_adoption"]["current"] for m in metrics],
                [m["usage"]["feature_adoption"]["trend"] for m in metrics],
                agg="avg", unit="%"),
        }

    # Section 2: Workstreams
    if section_key is None or section_key == "workstreams":
        ws_agg = {}
        for w in WORKSTREAM_DEFS:
            adopted = sum(1 for m in metrics if m["workstreams"][w["id"]]["adopted"])
            avg_maturity = _avg([m["workstreams"][w["id"]]["maturity"] for m in metrics])
            avg_value = _avg([m["workstreams"][w["id"]]["value_score"] for m in metrics])
            ws_agg[w["id"]] = {
                "label": w["label"], "icon": w["icon"],
                "adopted_count": adopted, "total_apps": n,
                "adoption_pct": round(adopted / n * 100, 1) if n else 0,
                "avg_maturity": avg_maturity, "avg_value_score": avg_value,
            }
        result["workstreams"] = ws_agg

    # Section 3: SRE
    if section_key is None or section_key == "sre":
        result["sre"] = {}
        for mk in ["mttr", "p1_incidents", "p2_incidents", "noise_events", "true_impact_dur", "slo_compliance", "error_budget"]:
            lib = mk in ("slo_compliance", "error_budget")
            agg_type = "avg" if mk in ("mttr", "true_impact_dur", "slo_compliance", "error_budget") else "sum"
            result["sre"][mk] = _build_metric(
                [m["sre"][mk]["baseline"] for m in metrics],
                [m["sre"][mk]["current"] for m in metrics],
                [m["sre"][mk]["trend"] for m in metrics],
                agg=agg_type, lower_is_better=not lib, unit=metrics[0]["sre"][mk]["unit"])

    # Section 4: Support
    if section_key is None or section_key == "support":
        result["support"] = {}
        for mk in ["service_requests", "self_service_pct", "escalations"]:
            lib = mk == "self_service_pct"
            agg_type = "avg" if mk == "self_service_pct" else "sum"
            result["support"][mk] = _build_metric(
                [m["support"][mk]["baseline"] for m in metrics],
                [m["support"][mk]["current"] for m in metrics],
                [m["support"][mk]["trend"] for m in metrics],
                agg=agg_type, lower_is_better=not lib, unit=metrics[0]["support"][mk]["unit"])

    # Section 5: Coverage
    if section_key is None or section_key == "baselines":
        cov_keys = ["golden_signals", "slo_defined", "incident_zero", "blast_radius", "runbooks", "day1_complete"]
        coverage = {}
        for ck in cov_keys:
            count = sum(1 for m in metrics if m["coverage"][ck])
            coverage[ck] = {"covered": count, "total": n, "pct": round(count / n * 100, 1) if n else 0}
        overall = sum(coverage[ck]["covered"] for ck in cov_keys)
        total_possible = n * len(cov_keys)
        coverage["overall"] = {"covered": overall, "total": total_possible, "pct": round(overall / total_possible * 100, 1) if total_possible else 0}
        result["baselines"] = coverage

    return result


def build_leaderboard(apps: list[dict], section_key: str, sort_by: str | None = None) -> list[dict]:
    """Build a ranked CTO/CBT leaderboard for a given section.

    Groups apps by CTO→CBT, aggregates the section metrics, and sorts by
    the primary metric (or the given sort_by key).
    """
    all_m = get_all_seal_metrics()

    # Group SEALs by CTO → CBT
    cto_cbt_map: dict[str, dict[str, list[str]]] = {}
    for a in apps:
        cto = a.get("cto", "Unknown")
        cbt = a.get("cbt", "Unknown")
        cto_cbt_map.setdefault(cto, {}).setdefault(cbt, []).append(a["seal"])

    rows = []
    for cto, cbt_map in cto_cbt_map.items():
        for cbt, seals in cbt_map.items():
            agg = aggregate_metrics(seals, section_key)
            section_data = agg.get(section_key, {})

            # Determine primary sort metric
            if section_key == "usage":
                primary_key = sort_by or "prompts"
                primary = section_data.get(primary_key, {})
            elif section_key == "sre":
                primary_key = sort_by or "mttr"
                primary = section_data.get(primary_key, {})
            elif section_key == "support":
                primary_key = sort_by or "service_requests"
                primary = section_data.get(primary_key, {})
            elif section_key == "workstreams":
                # For workstreams, compute average adoption across all workstreams
                ws_data = section_data
                if ws_data:
                    avg_adoption = round(sum(w["adoption_pct"] for w in ws_data.values()) / len(ws_data), 1)
                    avg_maturity = round(sum(w["avg_maturity"] for w in ws_data.values()) / len(ws_data), 1)
                else:
                    avg_adoption = avg_maturity = 0
                rows.append({
                    "cto": cto, "cbt": cbt, "app_count": len(seals),
                    "avg_adoption": avg_adoption, "avg_maturity": avg_maturity,
                    "metrics": section_data,
                })
                continue
            elif section_key == "baselines":
                overall = section_data.get("overall", {})
                rows.append({
                    "cto": cto, "cbt": cbt, "app_count": len(seals),
                    "coverage_pct": overall.get("pct", 0),
                    "metrics": section_data,
                })
                continue
            else:
                primary_key = "prompts"
                primary = section_data.get(primary_key, {})

            rows.append({
                "cto": cto, "cbt": cbt, "app_count": len(seals),
                "primary_metric": primary_key,
                "pct_change": primary.get("pct_change", 0),
                "current": primary.get("current", 0),
                "baseline": primary.get("baseline", 0),
                "trend": primary.get("trend", []),
                "lower_is_better": primary.get("lower_is_better", False),
                "metrics": section_data,
            })

    # Sort
    if section_key == "workstreams":
        rows.sort(key=lambda r: r.get("avg_adoption", 0), reverse=True)
    elif section_key == "baselines":
        rows.sort(key=lambda r: r.get("coverage_pct", 0), reverse=True)
    else:
        # For metrics where lower is better, best = most negative pct_change
        # For metrics where higher is better, best = most positive pct_change
        lib = rows[0].get("lower_is_better", False) if rows else False
        rows.sort(key=lambda r: r.get("pct_change", 0), reverse=not lib)

    # Add rank
    for i, r in enumerate(rows):
        r["rank"] = i + 1

    return rows


# ── Executive summary computation ─────────────────────────────────────────────

def compute_executive_summary(apps: list[dict]) -> dict:
    """Compute executive insights: top/bottom CTO-CBTs and workstream effectiveness."""
    # Group SEALs by CTO → CBT
    cto_cbt_map: dict[str, dict[str, list[str]]] = {}
    for a in apps:
        cto = a.get("cto", "Unknown")
        cbt = a.get("cbt", "Unknown")
        cto_cbt_map.setdefault(cto, {}).setdefault(cbt, []).append(a["seal"])

    # Score each CTO/CBT across SRE key metrics
    scored = []
    for cto, cbt_map in cto_cbt_map.items():
        for cbt, seals in cbt_map.items():
            agg = aggregate_metrics(seals)
            sre = agg.get("sre", {})
            support = agg.get("support", {})
            usage = agg.get("usage", {})

            # Composite improvement score: average of pct_change across key metrics
            # For lower-is-better, negate so positive = good
            score_parts = []
            for data in {**sre, **support}.values():
                pct = data.get("pct_change", 0)
                lib = data.get("lower_is_better", False)
                score_parts.append(-pct if lib else pct)
            composite_score = round(sum(score_parts) / len(score_parts), 1) if score_parts else 0

            scored.append({
                "cto": cto, "cbt": cbt, "app_count": len(seals),
                "composite_score": composite_score,
                "mttr_pct": sre.get("mttr", {}).get("pct_change", 0),
                "p1_pct": sre.get("p1_incidents", {}).get("pct_change", 0),
                "impact_dur_pct": sre.get("true_impact_dur", {}).get("pct_change", 0),
                "service_req_pct": support.get("service_requests", {}).get("pct_change", 0),
                "prompts_pct": usage.get("prompts", {}).get("pct_change", 0),
            })

    scored.sort(key=lambda r: r["composite_score"], reverse=True)

    top_performers = scored[:5]
    bottom_performers = list(reversed(scored[-5:])) if len(scored) >= 5 else list(reversed(scored))

    # Workstream effectiveness across all apps
    seal_list = [a["seal"] for a in apps]
    ws_agg = aggregate_metrics(seal_list, "workstreams").get("workstreams", {})
    ws_insights = []
    for w in WORKSTREAM_DEFS:
        ws = ws_agg.get(w["id"], {})
        adoption = ws.get("adoption_pct", 0)
        maturity = ws.get("avg_maturity", 0)
        value = ws.get("avg_value_score", 0)
        effectiveness = round(adoption * 0.4 + maturity * 0.3 + value * 0.3, 1)
        status = "strong" if effectiveness >= 65 else "moderate" if effectiveness >= 45 else "needs_attention"
        ws_insights.append({
            "id": w["id"], "label": w["label"], "icon": w["icon"],
            "adoption_pct": adoption, "avg_maturity": maturity,
            "avg_value_score": value, "effectiveness": effectiveness,
            "status": status,
        })
    ws_insights.sort(key=lambda w: w["effectiveness"], reverse=True)

    return {
        "total_cto_cbts": len(scored),
        "top_performers": top_performers,
        "bottom_performers": bottom_performers,
        "workstream_insights": ws_insights,
    }


# ── Executive KPI computation ─────────────────────────────────────────────────

def compute_executive_kpis(seal_list: list[str]) -> list[dict]:
    """Return 6 headline KPIs across all sections for the executive bar."""
    agg = aggregate_metrics(seal_list)
    kpis = []

    # 1. Prompts (Usage)
    u = agg.get("usage", {}).get("prompts", {})
    kpis.append({
        "label": "AI Prompts", "section": "usage",
        "current": u.get("current", 0), "baseline": u.get("baseline", 0),
        "pct_change": u.get("pct_change", 0), "unit": "",
        "spark": u.get("trend", [])[-7:], "lower_is_better": False,
    })

    # 2. MTTR (SRE)
    s = agg.get("sre", {}).get("mttr", {})
    kpis.append({
        "label": "Avg MTTR", "section": "sre",
        "current": s.get("current", 0), "baseline": s.get("baseline", 0),
        "pct_change": s.get("pct_change", 0), "unit": "min",
        "spark": s.get("trend", [])[-7:], "lower_is_better": True,
    })

    # 3. True Impact Duration (SRE)
    t = agg.get("sre", {}).get("true_impact_dur", {})
    kpis.append({
        "label": "Impact Duration", "section": "sre",
        "current": t.get("current", 0), "baseline": t.get("baseline", 0),
        "pct_change": t.get("pct_change", 0), "unit": "min",
        "spark": t.get("trend", [])[-7:], "lower_is_better": True,
    })

    # 4. P1 Incidents (SRE)
    p = agg.get("sre", {}).get("p1_incidents", {})
    kpis.append({
        "label": "P1 Incidents", "section": "sre",
        "current": p.get("current", 0), "baseline": p.get("baseline", 0),
        "pct_change": p.get("pct_change", 0), "unit": "",
        "spark": p.get("trend", [])[-7:], "lower_is_better": True,
    })

    # 5. Service Requests (Support)
    sr = agg.get("support", {}).get("service_requests", {})
    kpis.append({
        "label": "Service Requests", "section": "support",
        "current": sr.get("current", 0), "baseline": sr.get("baseline", 0),
        "pct_change": sr.get("pct_change", 0), "unit": "/mo",
        "spark": sr.get("trend", [])[-7:], "lower_is_better": True,
    })

    # 6. Coverage (Baselines)
    cov = agg.get("baselines", {}).get("overall", {})
    kpis.append({
        "label": "SRE Coverage", "section": "baselines",
        "current": cov.get("pct", 0), "baseline": 0, "pct_change": cov.get("pct", 0),
        "unit": "%", "spark": [], "lower_is_better": False,
    })

    return kpis
