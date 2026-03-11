# REAL: Replace with Customer Journey API / database queries

"""
Deterministic mock data for the Customer Journeys page.

Journeys are seeded from Business Processes and Essential Services, with
additional manually-defined cross-cutting journeys.  Health is derived
bottom-up from mapped application statuses.
"""

import hashlib
from datetime import datetime, timedelta

from .apps_registry import APPS_REGISTRY
from .essential_services_data import (
    ESSENTIAL_SERVICES,
    ES_APP_MAPPINGS,
    BUSINESS_PROCESSES,
    BP_BY_ID,
    ES_BY_ID,
    _worst_status,
    _app_status_from_enriched,
)
from .graph_data import SEAL_COMPONENTS, NODES

# ── Helpers ───────────────────────────────────────────────────────────────────

def _seed(key: str, salt: str = "") -> int:
    """Deterministic int seed from key + salt."""
    return int(hashlib.md5(f"{key}{salt}".encode()).hexdigest()[:8], 16)


def _pct(seed_val: int, lo: int, hi: int) -> float:
    return round(lo + (seed_val % 1000) / 999 * (hi - lo), 1)


def _trend_12m(seed_val: int, baseline: float, current: float) -> list[float]:
    steps = 12
    result = []
    for i in range(steps):
        t = i / (steps - 1)
        noise = ((seed_val * (i + 1) * 7) % 100 - 50) / 500
        val = baseline + (current - baseline) * t + noise * abs(current - baseline + 1)
        result.append(round(max(0, val), 2))
    return result


MONTH_LABELS = [
    "Apr'25", "May'25", "Jun'25", "Jul'25", "Aug'25", "Sep'25",
    "Oct'25", "Nov'25", "Dec'25", "Jan'26", "Feb'26", "Mar'26",
]

_RAW_BY_SEAL = {a["seal"]: a for a in APPS_REGISTRY}

# ── Customer-action journey names (mapped from BP IDs) ───────────────────────

_BP_JOURNEY_NAMES = {
    "bp1":  "Calculate and Distribute Fund Valuations",
    "bp2":  "Onboard a New Client",
    "bp3":  "Execute a Brokerage Trade",
    "bp4":  "Close a Mortgage Loan",
    "bp5":  "Manage an Investment Portfolio (AM)",
    "bp6":  "Manage an Investment Portfolio (WM)",
    "bp7":  "Access Funds from a Credit Facility",
    "bp8":  "Process Shareholder Transactions",
    "bp9":  "Liquidate and Distribute Assets",
    "bp10": "Manage Collateral Positions",
    "bp11": "Administer a Fund",
    "bp12": "Fulfill a Client Service Request",
}

_BP_CUSTOMER_DESCRIPTIONS = {
    "bp1":  "End-to-end daily NAV computation, validation, and distribution for pooled fund investors",
    "bp2":  "From initial prospect application through KYC/AML verification to active account activation",
    "bp3":  "Complete brokerage order lifecycle from order entry through execution, settlement, and cash sweep",
    "bp4":  "Committed mortgage loan closing from document preparation through compliance review and funding",
    "bp5":  "Discretionary portfolio construction, drift analysis, rebalancing, and NAV impact assessment",
    "bp6":  "Advisory portfolio management from client review through proposal, approval, and reporting",
    "bp7":  "Loan draw-down processing from request through collateral check, approval, and disbursement",
    "bp8":  "Purchase, redemption, and distribution processing for pooled fund shareholders",
    "bp9":  "Systematic liquidation of investment holdings and controlled distribution of proceeds",
    "bp10": "End-to-end collateral valuation, margin call processing, substitution, and compliance monitoring",
    "bp11": "Money market and pooled fund daily operations including yield computation, compliance, and reporting",
    "bp12": "Processing essential client instructions across sweep, credit, and portfolio services",
}

_BP_CUSTOMER_SEGMENTS = {
    "bp1":  "Asset Management",
    "bp2":  "Wealth Management",
    "bp3":  "Brokerage",
    "bp4":  "Lending",
    "bp5":  "Asset Management",
    "bp6":  "Wealth Management",
    "bp7":  "Lending",
    "bp8":  "Asset Management",
    "bp9":  "Asset Management",
    "bp10": "Risk Management",
    "bp11": "Asset Management",
    "bp12": "Client Services",
}

_BP_CRITICALITIES = {
    "bp1":  "critical",
    "bp2":  "high",
    "bp3":  "critical",
    "bp4":  "high",
    "bp5":  "high",
    "bp6":  "high",
    "bp7":  "critical",
    "bp8":  "critical",
    "bp9":  "critical",
    "bp10": "medium",
    "bp11": "critical",
    "bp12": "high",
}

_BP_OWNER_LOBS = {
    "bp1":  "Asset & Wealth Management",
    "bp2":  "Asset & Wealth Management",
    "bp3":  "Asset & Wealth Management",
    "bp4":  "Asset & Wealth Management",
    "bp5":  "Asset & Wealth Management",
    "bp6":  "Asset & Wealth Management",
    "bp7":  "Asset & Wealth Management",
    "bp8":  "Asset & Wealth Management",
    "bp9":  "Asset & Wealth Management",
    "bp10": "Asset & Wealth Management",
    "bp11": "Asset & Wealth Management",
    "bp12": "Asset & Wealth Management",
}

_BP_OWNER_TEAMS = {
    "bp1":  "Fund Operations",
    "bp2":  "Client Onboarding",
    "bp3":  "Trading Operations",
    "bp4":  "Mortgage Operations",
    "bp5":  "Portfolio Management (AM)",
    "bp6":  "Portfolio Management (WM)",
    "bp7":  "Credit Operations",
    "bp8":  "Transfer Agency",
    "bp9":  "Asset Management Ops",
    "bp10": "Collateral Management",
    "bp11": "Fund Administration",
    "bp12": "Client Service Center",
}


# ── Build journey definitions from Business Processes ─────────────────────────

def _build_step_components(es_id: str) -> list[dict]:
    """Build mapped_components for a step from an Essential Service's SEAL mappings."""
    seals = ES_APP_MAPPINGS.get(es_id, [])
    components = []
    for seal in seals[:3]:  # Limit to 3 apps per step for readability
        app = _RAW_BY_SEAL.get(seal)
        if not app:
            continue
        # Get first component for this app from Knowledge Graph
        comp_ids = SEAL_COMPONENTS.get(seal, [])
        for comp_id in comp_ids[:2]:  # Max 2 components per app
            node = next((n for n in NODES if n["id"] == comp_id), None)
            components.append({
                "seal": seal,
                "app_name": app["name"],
                "deployment": app.get("deploymentTypes", ["unknown"])[0] if app.get("deploymentTypes") else "unknown",
                "component_id": comp_id,
                "component_label": node["label"] if node else comp_id.upper(),
            })
    return components


def _generate_journeys() -> list[dict]:
    """Generate journey definitions from Business Processes."""
    journeys = []

    for bp in BUSINESS_PROCESSES:
        bp_id = bp["id"]
        journey_id = f"cj-{bp_id}"
        steps = []

        for i, (step_name, es_id) in enumerate(zip(bp["steps"], bp["services"] + [""] * len(bp["steps"]))):
            # Each step maps to an ES if available
            mapped_es = [es_id] if es_id and es_id in ES_BY_ID else []
            mapped_components = _build_step_components(es_id) if es_id else []

            # Collect all unique SEALs from components
            step_seals = list(dict.fromkeys(c["seal"] for c in mapped_components))

            steps.append({
                "id": f"{journey_id}-step-{i + 1}",
                "name": step_name,
                "description": ES_BY_ID[es_id]["description"] if es_id and es_id in ES_BY_ID else f"Processing step: {step_name}",
                "order": i + 1,
                "mapped_components": mapped_components,
                "mapped_seals": step_seals,
                "mapped_es_ids": mapped_es,
            })

        journeys.append({
            "id": journey_id,
            "name": _BP_JOURNEY_NAMES.get(bp_id, bp["name"]),
            "description": _BP_CUSTOMER_DESCRIPTIONS.get(bp_id, bp["description"]),
            "owner_lob": _BP_OWNER_LOBS.get(bp_id, "Asset & Wealth Management"),
            "owner_team": _BP_OWNER_TEAMS.get(bp_id, "Operations"),
            "criticality": _BP_CRITICALITIES.get(bp_id, "medium"),
            "customer_segment": _BP_CUSTOMER_SEGMENTS.get(bp_id, "General"),
            "steps": steps,
            "source": "auto_es",
            "created_at": "2025-09-15T10:00:00Z",
            "updated_at": "2026-02-01T14:30:00Z",
            "bp_id": bp_id,
        })

    # Add 2 manual cross-cutting journeys
    journeys.append({
        "id": "cj-manual-1",
        "name": "Open a New Brokerage Account",
        "description": "Complete end-to-end flow from prospect registration through account funding and first trade",
        "owner_lob": "Asset & Wealth Management",
        "owner_team": "Digital Experience",
        "criticality": "critical",
        "customer_segment": "Brokerage",
        "steps": [
            {"id": "cj-manual-1-step-1", "name": "Registration", "description": "Client creates account and provides personal details", "order": 1,
             "mapped_components": _build_step_components("3197"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3197"))), "mapped_es_ids": ["3197"]},
            {"id": "cj-manual-1-step-2", "name": "Identity Verification", "description": "KYC/AML verification of client identity", "order": 2,
             "mapped_components": _build_step_components("3199"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3199"))), "mapped_es_ids": ["3199"]},
            {"id": "cj-manual-1-step-3", "name": "Account Provisioning", "description": "Account creation in systems of record", "order": 3,
             "mapped_components": _build_step_components("3199"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3199"))), "mapped_es_ids": ["3199"]},
            {"id": "cj-manual-1-step-4", "name": "Initial Funding", "description": "First deposit or transfer into the new account", "order": 4,
             "mapped_components": _build_step_components("3213"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3213"))), "mapped_es_ids": ["3213"]},
            {"id": "cj-manual-1-step-5", "name": "First Trade", "description": "Client places their first brokerage order", "order": 5,
             "mapped_components": _build_step_components("3211"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3211"))), "mapped_es_ids": ["3211"]},
        ],
        "source": "manual",
        "created_at": "2025-11-01T09:00:00Z",
        "updated_at": "2026-01-20T11:15:00Z",
    })

    journeys.append({
        "id": "cj-manual-2",
        "name": "Transfer Assets to Another Institution",
        "description": "Full asset transfer flow from request initiation through liquidation and external transfer",
        "owner_lob": "Asset & Wealth Management",
        "owner_team": "Transfer Services",
        "criticality": "high",
        "customer_segment": "Wealth Management",
        "steps": [
            {"id": "cj-manual-2-step-1", "name": "Transfer Request", "description": "Client initiates asset transfer request", "order": 1,
             "mapped_components": _build_step_components("3199"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3199"))), "mapped_es_ids": ["3199"]},
            {"id": "cj-manual-2-step-2", "name": "Holdings Review", "description": "Review and validate holdings to be transferred", "order": 2,
             "mapped_components": _build_step_components("3204"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3204"))), "mapped_es_ids": ["3204"]},
            {"id": "cj-manual-2-step-3", "name": "Liquidation", "description": "Liquidate holdings that cannot be transferred in-kind", "order": 3,
             "mapped_components": _build_step_components("3212"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3212"))), "mapped_es_ids": ["3212"]},
            {"id": "cj-manual-2-step-4", "name": "External Transfer", "description": "Execute ACAT or wire transfer to receiving institution", "order": 4,
             "mapped_components": _build_step_components("3214"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3214"))), "mapped_es_ids": ["3214"]},
            {"id": "cj-manual-2-step-5", "name": "Confirmation", "description": "Confirm transfer completion with client and receiving institution", "order": 5,
             "mapped_components": _build_step_components("3199"), "mapped_seals": list(dict.fromkeys(c["seal"] for c in _build_step_components("3199"))), "mapped_es_ids": ["3199"]},
        ],
        "source": "manual",
        "created_at": "2025-12-10T14:00:00Z",
        "updated_at": "2026-02-15T09:45:00Z",
    })

    return journeys


# Pre-compute journey definitions
CUSTOMER_JOURNEYS: list[dict] = _generate_journeys()
CJ_BY_ID: dict[str, dict] = {cj["id"]: cj for cj in CUSTOMER_JOURNEYS}

# Mutable list for CRUD (in-memory, same pattern as announcements)
_journeys_store: list[dict] = list(CUSTOMER_JOURNEYS)
_next_id_counter = [len(CUSTOMER_JOURNEYS) + 1]


# ── Health computation ────────────────────────────────────────────────────────

def _step_health(step: dict, app_by_seal: dict) -> dict:
    """Compute health for a single journey step."""
    mapped_apps = [app_by_seal[s] for s in step.get("mapped_seals", []) if s in app_by_seal]
    statuses = [_app_status_from_enriched(a) for a in mapped_apps]
    status = _worst_status(statuses) if statuses else "no_data"

    # Compute aggregated metrics for the step
    total_incidents = sum(a.get("incidents_today", 0) for a in mapped_apps)
    p1_count = sum(a.get("p1_30d", 0) for a in mapped_apps)

    # Deterministic latency and error rate from step seed
    s = _seed(step["id"], "metrics")
    latency_base = 20 + (s % 800)
    if status == "critical":
        latency = latency_base * 4
        error_rate = round(5 + _pct(s, 5, 25), 1)
    elif status == "warning":
        latency = latency_base * 2
        error_rate = round(1 + _pct(s, 0, 5), 1)
    else:
        latency = latency_base
        error_rate = round(_pct(s, 0, 1), 1)

    return {
        **step,
        "status": status,
        "latency_ms": latency,
        "latency": f"{latency}ms" if latency < 1000 else f"{round(latency / 1000, 1)}s",
        "error_rate": error_rate,
        "app_count": len(mapped_apps),
        "incidents_today": total_incidents,
        "p1_30d": p1_count,
        "mapped_app_details": [
            {
                "seal": a["seal"], "name": a["name"],
                "status": _app_status_from_enriched(a),
                "incidents_today": a.get("incidents_today", 0),
            }
            for a in mapped_apps
        ],
    }


def _journey_health(journey: dict, app_by_seal: dict) -> dict:
    """Compute health for a full journey."""
    enriched_steps = [_step_health(s, app_by_seal) for s in journey["steps"]]
    step_statuses = [s["status"] for s in enriched_steps]
    overall_status = _worst_status(step_statuses) if step_statuses else "no_data"

    # Aggregated counts
    all_seals = set()
    for s in journey["steps"]:
        all_seals.update(s.get("mapped_seals", []))

    total_apps = len([s for s in all_seals if s in app_by_seal])
    total_incidents = sum(s["incidents_today"] for s in enriched_steps)

    # SLO computation (deterministic based on journey status)
    s = _seed(journey["id"], "slo")
    if overall_status == "critical":
        slo_current = round(95 + _pct(s, 0, 300) / 100, 2)
    elif overall_status == "warning":
        slo_current = round(98 + _pct(s, 0, 150) / 100, 2)
    else:
        slo_current = round(99.5 + _pct(s, 0, 49) / 100, 2)

    slo_target = 99.95
    error_budget_total = 100 - slo_target
    error_budget_used = max(0, 100 - slo_current)
    error_budget_remaining = max(0, round((1 - error_budget_used / error_budget_total) * 100, 1)) if error_budget_total > 0 else 100

    # Burn rate
    burn_rate = round(error_budget_used / max(error_budget_total, 0.001), 2)

    # Breach ETA (days)
    if burn_rate > 1 and error_budget_remaining > 0:
        breach_eta_days = max(1, int(error_budget_remaining / (burn_rate - 1) * 30 / 100))
    else:
        breach_eta_days = None

    return {
        "id": journey["id"],
        "name": journey["name"],
        "description": journey["description"],
        "owner_lob": journey["owner_lob"],
        "owner_team": journey["owner_team"],
        "criticality": journey["criticality"],
        "customer_segment": journey["customer_segment"],
        "source": journey["source"],
        "created_at": journey["created_at"],
        "updated_at": journey["updated_at"],
        "status": overall_status,
        "steps": enriched_steps,
        "step_count": len(enriched_steps),
        "app_count": total_apps,
        "incidents_today": total_incidents,
        "slo": {
            "target": slo_target,
            "current": slo_current,
            "error_budget_remaining": error_budget_remaining,
            "burn_rate": burn_rate,
            "breach_eta_days": breach_eta_days,
        },
        "healthy_steps": sum(1 for s in step_statuses if s == "healthy"),
        "warning_steps": sum(1 for s in step_statuses if s == "warning"),
        "critical_steps": sum(1 for s in step_statuses if s == "critical"),
    }


# ── Public API functions ──────────────────────────────────────────────────────

def get_journey_list(enriched_apps: list[dict]) -> dict:
    """All journeys with rolled-up health status."""
    app_by_seal = {a["seal"]: a for a in enriched_apps}
    journeys = [_journey_health(cj, app_by_seal) for cj in _journeys_store]

    # KPI summary
    kpis = {
        "total": len(journeys),
        "healthy": sum(1 for j in journeys if j["status"] == "healthy"),
        "degraded": sum(1 for j in journeys if j["status"] == "warning"),
        "down": sum(1 for j in journeys if j["status"] == "critical"),
        "no_data": sum(1 for j in journeys if j["status"] == "no_data"),
    }

    # Remove step details from list view for efficiency
    journey_summaries = []
    for j in journeys:
        summary = {k: v for k, v in j.items() if k != "steps"}
        summary["steps"] = [{"id": s["id"], "name": s["name"], "status": s["status"], "latency": s["latency"], "error_rate": s["error_rate"]} for s in j["steps"]]
        journey_summaries.append(summary)

    return {
        "journeys": journey_summaries,
        "kpis": kpis,
        "app_count": len(enriched_apps),
    }


def get_journey_detail(journey_id: str, enriched_apps: list[dict]) -> dict | None:
    """Single journey with full step-level health details."""
    cj = next((j for j in _journeys_store if j["id"] == journey_id), None)
    if not cj:
        return None
    app_by_seal = {a["seal"]: a for a in enriched_apps}
    return _journey_health(cj, app_by_seal)


def get_journey_health_dashboard(enriched_apps: list[dict]) -> dict:
    """Auto-generated health dashboard from Essential Services and Business Processes."""
    app_by_seal = {a["seal"]: a for a in enriched_apps}
    journeys = [_journey_health(cj, app_by_seal) for cj in _journeys_store]

    # Group by customer segment
    segments = {}
    for j in journeys:
        seg = j.get("customer_segment", "Other")
        if seg not in segments:
            segments[seg] = {"segment": seg, "journeys": [], "healthy": 0, "degraded": 0, "down": 0}
        segments[seg]["journeys"].append({
            "id": j["id"], "name": j["name"], "status": j["status"],
            "criticality": j["criticality"], "step_count": j["step_count"],
            "app_count": j["app_count"],
            "slo_current": j["slo"]["current"],
            "error_budget_remaining": j["slo"]["error_budget_remaining"],
            "breach_eta_days": j["slo"]["breach_eta_days"],
            "change_freeze_recommended": j["slo"]["error_budget_remaining"] < 15 or j["status"] == "critical",
            "steps": [{"name": s["name"], "status": s["status"]} for s in j["steps"]],
        })
        if j["status"] == "healthy":
            segments[seg]["healthy"] += 1
        elif j["status"] == "warning":
            segments[seg]["degraded"] += 1
        elif j["status"] == "critical":
            segments[seg]["down"] += 1

    # Overall KPIs
    total_slo = round(sum(j["slo"]["current"] for j in journeys) / len(journeys), 2) if journeys else 0
    change_freeze_count = sum(1 for j in journeys if j["slo"]["error_budget_remaining"] < 15 or j["status"] == "critical")

    return {
        "segments": list(segments.values()),
        "kpis": {
            "total_journeys": len(journeys),
            "healthy": sum(1 for j in journeys if j["status"] == "healthy"),
            "degraded": sum(1 for j in journeys if j["status"] == "warning"),
            "down": sum(1 for j in journeys if j["status"] == "critical"),
            "avg_slo_compliance": total_slo,
            "change_freeze_recommended": change_freeze_count,
        },
        "app_count": len(enriched_apps),
    }


def get_journey_analytics(journey_id: str, enriched_apps: list[dict]) -> dict | None:
    """12-month trend analytics for a journey."""
    cj = next((j for j in _journeys_store if j["id"] == journey_id), None)
    if not cj:
        return None

    app_by_seal = {a["seal"]: a for a in enriched_apps}
    health = _journey_health(cj, app_by_seal)

    s = _seed(journey_id, "analytics")

    # SLO compliance trend (trending toward current)
    slo_baseline = round(health["slo"]["current"] - _pct(s, 50, 200) / 100, 2)
    slo_trend = _trend_12m(s, slo_baseline, health["slo"]["current"])

    # Error budget remaining trend
    eb_baseline = min(100, health["slo"]["error_budget_remaining"] + _pct(_seed(journey_id, "eb"), 5, 30))
    eb_trend = _trend_12m(_seed(journey_id, "ebt"), eb_baseline, health["slo"]["error_budget_remaining"])

    # Incident count trend
    inc_baseline = 3 + (_seed(journey_id, "incb") % 15)
    inc_current = max(0, inc_baseline - int(inc_baseline * _pct(_seed(journey_id, "incc"), 10, 60) / 100))
    inc_trend = _trend_12m(_seed(journey_id, "inct"), inc_baseline, inc_current)

    # Change velocity (releases/month)
    cv_baseline = 5 + (_seed(journey_id, "cvb") % 20)
    cv_current = cv_baseline + int(cv_baseline * _pct(_seed(journey_id, "cvc"), -20, 40) / 100)
    cv_trend = _trend_12m(_seed(journey_id, "cvt"), cv_baseline, cv_current)

    # Customer satisfaction proxy (derived from SLO + incidents)
    csat_baseline = round(70 + _pct(_seed(journey_id, "csatb"), 0, 20), 1)
    csat_current = round(csat_baseline + _pct(_seed(journey_id, "csatc"), -5, 15), 1)
    csat_trend = _trend_12m(_seed(journey_id, "csatt"), csat_baseline, csat_current)

    # Proactive alerts
    alerts = []
    if health["slo"]["breach_eta_days"] is not None and health["slo"]["breach_eta_days"] <= 14:
        alerts.append({
            "severity": "critical" if health["slo"]["breach_eta_days"] <= 5 else "warning",
            "message": f"{health['name']} is trending toward SLO breach in {health['slo']['breach_eta_days']} days",
            "metric": "SLO Compliance",
            "current_value": health["slo"]["current"],
            "target_value": health["slo"]["target"],
        })

    if health["slo"]["error_budget_remaining"] < 20:
        alerts.append({
            "severity": "warning",
            "message": f"Error budget for {health['name']} is at {health['slo']['error_budget_remaining']}% — consider change freeze",
            "metric": "Error Budget",
            "current_value": health["slo"]["error_budget_remaining"],
            "target_value": 100,
        })

    if health["status"] == "critical":
        alerts.append({
            "severity": "critical",
            "message": f"{health['name']} has {health['critical_steps']} critical steps impacting customer experience",
            "metric": "Journey Health",
            "current_value": health["critical_steps"],
            "target_value": 0,
        })

    # AURA narrative
    if health["status"] == "critical":
        narrative = (
            f"**{health['name']}** is currently experiencing degraded performance with "
            f"{health['critical_steps']} critical and {health['warning_steps']} warning steps. "
            f"SLO compliance is at {health['slo']['current']}% against a {health['slo']['target']}% target. "
            f"Error budget is {'critically low' if health['slo']['error_budget_remaining'] < 15 else 'depleting'}. "
            f"**Recommendation:** Consider implementing a change freeze for applications in the critical path "
            f"and escalate to the {health['owner_team']} team for immediate investigation."
        )
    elif health["status"] == "warning":
        narrative = (
            f"**{health['name']}** shows some degradation with {health['warning_steps']} steps in warning state. "
            f"SLO compliance remains at {health['slo']['current']}% with {health['slo']['error_budget_remaining']}% "
            f"error budget remaining. While not critical, proactive monitoring is recommended. "
            f"Change velocity is {'elevated' if cv_current > cv_baseline else 'stable'} at {cv_current} releases/month."
        )
    else:
        narrative = (
            f"**{health['name']}** is performing well with all {health['step_count']} steps healthy. "
            f"SLO compliance is strong at {health['slo']['current']}% with ample error budget ({health['slo']['error_budget_remaining']}% remaining). "
            f"Customer satisfaction proxy is {'trending up' if csat_current > csat_baseline else 'stable'} at {csat_current}%. "
            f"The journey is clear for normal release cadence."
        )

    return {
        "journey": {
            "id": health["id"], "name": health["name"], "status": health["status"],
            "criticality": health["criticality"], "customer_segment": health["customer_segment"],
        },
        "month_labels": MONTH_LABELS,
        "metrics": {
            "slo_compliance": {
                "label": "SLO Compliance", "unit": "%", "current": health["slo"]["current"],
                "baseline": slo_baseline, "trend": slo_trend, "lower_is_better": False,
                "pct_change": round((health["slo"]["current"] - slo_baseline) / max(slo_baseline, 0.01) * 100, 1),
            },
            "error_budget_remaining": {
                "label": "Error Budget Remaining", "unit": "%", "current": health["slo"]["error_budget_remaining"],
                "baseline": eb_baseline, "trend": eb_trend, "lower_is_better": False,
                "pct_change": round((health["slo"]["error_budget_remaining"] - eb_baseline) / max(eb_baseline, 0.01) * 100, 1),
            },
            "incident_count": {
                "label": "Incidents (30d)", "unit": "count", "current": inc_current,
                "baseline": inc_baseline, "trend": inc_trend, "lower_is_better": True,
                "pct_change": round((inc_current - inc_baseline) / max(inc_baseline, 1) * 100, 1),
            },
            "change_velocity": {
                "label": "Change Velocity", "unit": "releases/mo", "current": cv_current,
                "baseline": cv_baseline, "trend": cv_trend, "lower_is_better": False,
                "pct_change": round((cv_current - cv_baseline) / max(cv_baseline, 1) * 100, 1),
            },
            "customer_satisfaction": {
                "label": "Customer Satisfaction", "unit": "score", "current": csat_current,
                "baseline": csat_baseline, "trend": csat_trend, "lower_is_better": False,
                "pct_change": round((csat_current - csat_baseline) / max(csat_baseline, 0.01) * 100, 1),
            },
        },
        "alerts": sorted(alerts, key=lambda a: 0 if a["severity"] == "critical" else 1),
        "aura_narrative": narrative,
        "slo_detail": health["slo"],
    }


def get_analytics_summary(enriched_apps: list[dict]) -> dict:
    """Cross-journey analytics summary with proactive alerts."""
    app_by_seal = {a["seal"]: a for a in enriched_apps}
    all_alerts = []
    journey_summaries = []

    for cj in _journeys_store:
        analytics = get_journey_analytics(cj["id"], enriched_apps)
        if not analytics:
            continue

        journey_summaries.append({
            "id": cj["id"],
            "name": cj["name"],
            "status": analytics["journey"]["status"],
            "criticality": analytics["journey"]["criticality"],
            "slo_current": analytics["metrics"]["slo_compliance"]["current"],
            "error_budget": analytics["metrics"]["error_budget_remaining"]["current"],
            "incidents": analytics["metrics"]["incident_count"]["current"],
            "csat": analytics["metrics"]["customer_satisfaction"]["current"],
            "alert_count": len(analytics["alerts"]),
        })

        for alert in analytics["alerts"]:
            all_alerts.append({**alert, "journey_id": cj["id"], "journey_name": cj["name"]})

    return {
        "journeys": journey_summaries,
        "alerts": sorted(all_alerts, key=lambda a: (0 if a["severity"] == "critical" else 1, a.get("current_value", 0))),
        "month_labels": MONTH_LABELS,
    }


def get_journey_risk_matrix(enriched_apps: list[dict]) -> dict:
    """Risk matrix: criticality x health status."""
    app_by_seal = {a["seal"]: a for a in enriched_apps}
    journeys = [_journey_health(cj, app_by_seal) for cj in _journeys_store]

    matrix = {}
    for j in journeys:
        status_label = "down" if j["status"] == "critical" else "degraded" if j["status"] == "warning" else j["status"]
        cell_key = f"{j['criticality']}_{status_label}"
        if cell_key not in matrix:
            matrix[cell_key] = {"count": 0, "journeys": []}
        matrix[cell_key]["count"] += 1
        matrix[cell_key]["journeys"].append({
            "id": j["id"], "name": j["name"], "status": j["status"],
            "slo_current": j["slo"]["current"],
        })

    # Readiness overview
    readiness_rows = []
    for j in journeys:
        score = _compute_readiness_score(j)
        readiness_rows.append({
            "id": j["id"],
            "name": j["name"],
            "criticality": j["criticality"],
            "status": j["status"],
            "readiness_score": score["score"],
            "readiness_label": score["label"],
            "slo_headroom": score["components"]["slo_headroom"],
            "error_budget": j["slo"]["error_budget_remaining"],
            "incidents_today": j["incidents_today"],
            "app_count": j["app_count"],
            "change_freeze_recommended": score["change_freeze_recommended"],
            "change_freeze_reason": score["change_freeze_reason"],
        })

    readiness_rows.sort(key=lambda r: r["readiness_score"])

    return {
        "risk_matrix": matrix,
        "readiness": readiness_rows,
        "criticality_levels": ["critical", "high", "medium", "low"],
        "status_levels": ["down", "degraded", "healthy"],
    }


def _compute_readiness_score(journey_health: dict) -> dict:
    """Compute release readiness score (0-100) for a journey."""
    slo = journey_health["slo"]

    # SLO headroom (30%) — how far above target
    slo_headroom = max(0, slo["current"] - slo["target"])
    slo_score = min(100, slo_headroom * 200)  # 0.5% headroom = 100

    # Error budget remaining (25%)
    eb_score = min(100, slo["error_budget_remaining"])

    # Incident trend (20%) — fewer incidents = better
    s = _seed(journey_health["id"], "readiness")
    inc_trend_pct = _pct(s, -50, 30)  # Negative = improving
    inc_score = min(100, max(0, 50 - inc_trend_pct))

    # Change velocity (15%) — moderate velocity is ideal
    cv = _pct(_seed(journey_health["id"], "cv_score"), 30, 90)
    cv_score = cv

    # Blast radius (10%) — fewer connected apps = lower risk
    blast_size = journey_health["app_count"]
    blast_score = max(0, 100 - blast_size * 5)

    weighted = round(
        slo_score * 0.30 +
        eb_score * 0.25 +
        inc_score * 0.20 +
        cv_score * 0.15 +
        blast_score * 0.10,
        1
    )

    if weighted >= 80:
        label = "green"
    elif weighted >= 50:
        label = "amber"
    else:
        label = "red"

    # Change freeze logic
    freeze = False
    freeze_reason = ""
    if journey_health["status"] == "critical":
        freeze = True
        freeze_reason = "Journey has critical steps impacting customer experience"
    elif slo["error_budget_remaining"] < 15:
        freeze = True
        freeze_reason = f"Error budget critically low at {slo['error_budget_remaining']}%"
    elif slo["burn_rate"] > 3:
        freeze = True
        freeze_reason = f"SLO burn rate is {slo['burn_rate']}x — accelerated error budget consumption"

    return {
        "score": weighted,
        "label": label,
        "change_freeze_recommended": freeze,
        "change_freeze_reason": freeze_reason,
        "components": {
            "slo_headroom": round(slo_headroom, 3),
            "slo_score": round(slo_score, 1),
            "error_budget_score": round(eb_score, 1),
            "incident_score": round(inc_score, 1),
            "change_velocity_score": round(cv_score, 1),
            "blast_radius_score": round(blast_score, 1),
        },
    }


def get_release_readiness(journey_id: str, enriched_apps: list[dict]) -> dict | None:
    """Release readiness detail for a single journey."""
    cj = next((j for j in _journeys_store if j["id"] == journey_id), None)
    if not cj:
        return None
    app_by_seal = {a["seal"]: a for a in enriched_apps}
    health = _journey_health(cj, app_by_seal)
    score = _compute_readiness_score(health)
    return {
        "journey": {"id": health["id"], "name": health["name"], "status": health["status"], "criticality": health["criticality"]},
        **score,
        "slo": health["slo"],
    }


def get_journey_blast_radius(journey_id: str, enriched_apps: list[dict]) -> dict | None:
    """Which other journeys share apps/components with this journey."""
    cj = next((j for j in _journeys_store if j["id"] == journey_id), None)
    if not cj:
        return None

    # Collect all SEALs in this journey
    journey_seals = set()
    for step in cj["steps"]:
        journey_seals.update(step.get("mapped_seals", []))

    # Find other journeys that share SEALs
    impacted = []
    for other in _journeys_store:
        if other["id"] == journey_id:
            continue
        other_seals = set()
        for step in other["steps"]:
            other_seals.update(step.get("mapped_seals", []))

        shared = journey_seals & other_seals
        if shared:
            app_by_seal = {a["seal"]: a for a in enriched_apps}
            other_health = _journey_health(other, app_by_seal)
            impacted.append({
                "id": other["id"],
                "name": other["name"],
                "status": other_health["status"],
                "criticality": other["criticality"],
                "shared_app_count": len(shared),
                "shared_seals": list(shared)[:5],
                "shared_app_names": [_RAW_BY_SEAL[s]["name"] for s in list(shared)[:5] if s in _RAW_BY_SEAL],
            })

    impacted.sort(key=lambda x: x["shared_app_count"], reverse=True)

    return {
        "journey": {"id": cj["id"], "name": cj["name"], "criticality": cj["criticality"]},
        "total_apps": len(journey_seals),
        "impacted_journeys": impacted,
        "impacted_count": len(impacted),
    }


def get_journey_flow_graph(journey_id: str, enriched_apps: list[dict]) -> dict | None:
    """ReactFlow-compatible nodes and edges for the journey map editor."""
    cj = next((j for j in _journeys_store if j["id"] == journey_id), None)
    if not cj:
        return None

    app_by_seal = {a["seal"]: a for a in enriched_apps}
    health = _journey_health(cj, app_by_seal)

    nodes = []
    edges = []

    # Start node
    nodes.append({
        "id": "start",
        "type": "startNode",
        "data": {"label": "Start"},
        "position": {"x": 0, "y": 200},
    })

    # Step nodes
    for i, step in enumerate(health["steps"]):
        node_id = f"step-{i}"
        nodes.append({
            "id": node_id,
            "type": "businessStep",
            "data": {
                "label": step["name"],
                "status": step["status"],
                "latency": step["latency"],
                "error_rate": step["error_rate"],
                "app_count": step["app_count"],
                "step_number": i + 1,
                "mapped_apps": [
                    {"seal": a["seal"], "name": a["name"], "status": a["status"]}
                    for a in step.get("mapped_app_details", [])
                ],
            },
            "position": {"x": 250 + i * 280, "y": 200},
        })

        # Edge from previous
        source = "start" if i == 0 else f"step-{i - 1}"
        edges.append({
            "id": f"e-{source}-{node_id}",
            "source": source,
            "target": node_id,
            "type": "smoothstep",
            "animated": step["status"] == "critical",
        })

    # End node
    end_id = "end"
    nodes.append({
        "id": end_id,
        "type": "endNode",
        "data": {"label": "Complete"},
        "position": {"x": 250 + len(health["steps"]) * 280, "y": 200},
    })
    if health["steps"]:
        edges.append({
            "id": f"e-step-{len(health['steps']) - 1}-end",
            "source": f"step-{len(health['steps']) - 1}",
            "target": end_id,
            "type": "smoothstep",
        })

    return {
        "journey": {"id": health["id"], "name": health["name"], "status": health["status"]},
        "nodes": nodes,
        "edges": edges,
    }


# ── Component search (unified across app/deployment/component) ────────────────

def component_search(query: str, enriched_apps: list[dict], limit: int = 20) -> list[dict]:
    """
    Search across apps (name, SEAL), deployments, and components.
    Returns hierarchical results: app → deployment → component.
    """
    if not query or len(query) < 2:
        return []

    q = query.lower()
    results = []
    seen_keys = set()

    for app in APPS_REGISTRY:
        seal = app["seal"]
        app_name = app["name"]
        app_match = q in app_name.lower() or q in seal.lower()

        comp_ids = SEAL_COMPONENTS.get(seal, [])
        deploy_types = app.get("deploymentTypes", [])

        for comp_id in comp_ids:
            node = next((n for n in NODES if n["id"] == comp_id), None)
            comp_label = node["label"] if node else comp_id.upper()
            comp_match = q in comp_label.lower() or q in comp_id.lower()

            if app_match or comp_match:
                for dt in (deploy_types or ["unknown"]):
                    key = f"{seal}-{dt}-{comp_id}"
                    if key not in seen_keys:
                        seen_keys.add(key)
                        results.append({
                            "seal": seal,
                            "app_name": app_name,
                            "deployment": dt,
                            "component_id": comp_id,
                            "component_label": comp_label,
                            "match_type": "app" if app_match and not comp_match else "component" if comp_match and not app_match else "both",
                        })

        if len(results) >= limit:
            break

    return results[:limit]


# ── CRUD operations (in-memory) ───────────────────────────────────────────────

def create_journey(data: dict) -> dict:
    """Create a new journey definition."""
    journey_id = f"cj-custom-{_next_id_counter[0]}"
    _next_id_counter[0] += 1

    now = datetime.utcnow().isoformat() + "Z"

    journey = {
        "id": journey_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "owner_lob": data.get("owner_lob", ""),
        "owner_team": data.get("owner_team", ""),
        "criticality": data.get("criticality", "medium"),
        "customer_segment": data.get("customer_segment", ""),
        "steps": [],
        "source": "manual",
        "created_at": now,
        "updated_at": now,
    }

    for i, step_data in enumerate(data.get("steps", [])):
        journey["steps"].append({
            "id": f"{journey_id}-step-{i + 1}",
            "name": step_data["name"],
            "description": step_data.get("description", ""),
            "order": i + 1,
            "mapped_components": step_data.get("mapped_components", []),
            "mapped_seals": list(dict.fromkeys(c["seal"] for c in step_data.get("mapped_components", []))),
            "mapped_es_ids": step_data.get("mapped_es_ids", []),
        })

    _journeys_store.append(journey)
    return journey


def update_journey(journey_id: str, data: dict) -> dict | None:
    """Update an existing journey."""
    idx = next((i for i, j in enumerate(_journeys_store) if j["id"] == journey_id), None)
    if idx is None:
        return None

    journey = _journeys_store[idx]
    now = datetime.utcnow().isoformat() + "Z"

    for field in ["name", "description", "owner_lob", "owner_team", "criticality", "customer_segment"]:
        if field in data and data[field] is not None:
            journey[field] = data[field]

    if "steps" in data and data["steps"] is not None:
        journey["steps"] = []
        for i, step_data in enumerate(data["steps"]):
            journey["steps"].append({
                "id": step_data.get("id", f"{journey_id}-step-{i + 1}"),
                "name": step_data["name"],
                "description": step_data.get("description", ""),
                "order": i + 1,
                "mapped_components": step_data.get("mapped_components", []),
                "mapped_seals": list(dict.fromkeys(c["seal"] for c in step_data.get("mapped_components", []))),
                "mapped_es_ids": step_data.get("mapped_es_ids", []),
            })

    journey["updated_at"] = now
    _journeys_store[idx] = journey
    return journey


def delete_journey(journey_id: str) -> bool:
    """Delete a journey by ID."""
    idx = next((i for i, j in enumerate(_journeys_store) if j["id"] == journey_id), None)
    if idx is None:
        return False
    _journeys_store.pop(idx)
    return True


def suggest_journey(context: dict) -> dict:
    """AURA-powered journey suggestion based on context."""
    # In production, this would call AURA AI. For mock, generate from a random BP.
    s = _seed(str(context.get("message", "suggest")), "suggest")
    bp_idx = s % len(BUSINESS_PROCESSES)
    bp = BUSINESS_PROCESSES[bp_idx]

    suggested_steps = []
    for i, (step_name, es_id) in enumerate(zip(bp["steps"], bp["services"] + [""] * len(bp["steps"]))):
        mapped_components = _build_step_components(es_id) if es_id else []
        suggested_steps.append({
            "name": step_name,
            "description": ES_BY_ID[es_id]["description"] if es_id and es_id in ES_BY_ID else f"Processing: {step_name}",
            "mapped_components": mapped_components,
            "mapped_es_ids": [es_id] if es_id and es_id in ES_BY_ID else [],
            "confidence": round(0.7 + _pct(_seed(f"{bp['id']}{i}", "conf"), 0, 30) / 100, 2),
        })

    return {
        "suggested_name": _BP_JOURNEY_NAMES.get(bp["id"], bp["name"]),
        "suggested_description": _BP_CUSTOMER_DESCRIPTIONS.get(bp["id"], bp["description"]),
        "suggested_criticality": _BP_CRITICALITIES.get(bp["id"], "medium"),
        "suggested_customer_segment": _BP_CUSTOMER_SEGMENTS.get(bp["id"], "General"),
        "suggested_steps": suggested_steps,
        "source_bp": bp["id"],
        "source_bp_name": bp["name"],
        "aura_explanation": (
            f"Based on the existing **{bp['name']}** business process, I've identified "
            f"{len(suggested_steps)} key steps that map to {len(bp['services'])} Essential Services. "
            f"Each step has been pre-mapped to the relevant application components from the Knowledge Graph. "
            f"You can customize the step names and mappings to match your team's specific workflow."
        ),
    }
