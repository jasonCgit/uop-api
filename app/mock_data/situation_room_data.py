# REAL: Replace with ServiceNow API / incident database

"""
Mock data for the Situation Room — live P1 incident management.

Systems are CTO-scoped groupings of applications.
Situations are mutable incident records managed in real-time.
"""

from .apps_registry import APPS_REGISTRY
from .teams_data import TEAMS

# ── System Definitions ───────────────────────────────────────────────

SYSTEMS = [
    {
        "id": "sys-crm",
        "name": "CRM",
        "description": "Client Relationship Management",
        "cto": "Rod Thomas",
        "seals": ["88180", "90176", "85003", "83278", "90500", "84065"],
    },
    {
        "id": "sys-trading",
        "name": "TRADING",
        "description": "Trade execution and order management",
        "cto": "Lakith Leelasena",
        "seals": ["35206", "87082", "81884", "106195", "85333"],
    },
    {
        "id": "sys-portfolio",
        "name": "PORTFOLIO MGMT",
        "description": "Portfolio construction and rebalancing",
        "cto": "Lakith Leelasena",
        "seals": ["90215", "90645", "34210", "103290"],
    },
    {
        "id": "sys-payments",
        "name": "PAYMENTS",
        "description": "Payment processing and wire transfers",
        "cto": "Joe Pedone",
        "seals": ["62100", "62215", "60100"],
    },
    {
        "id": "sys-ai-eng",
        "name": "AI ENG",
        "description": "AI and data engineering platform",
        "cto": "David Chen",
        "seals": ["52100", "52215", "52330"],
    },
    {
        "id": "sys-architecture",
        "name": "ARCHITECTURE",
        "description": "Infrastructure and platform services",
        "cto": "Thomas Anderson",
        "seals": ["70100", "70215", "70330", "70440"],
    },
    {
        "id": "sys-client-svc",
        "name": "CLIENT SERVICES",
        "description": "Client service and support applications",
        "cto": "Stephen Musacchia",
        "seals": ["89749", "88652", "85928", "85233", "90083"],
    },
    {
        "id": "sys-ipb",
        "name": "IPB",
        "description": "International Private Banking",
        "cto": "Mark Napier",
        "seals": ["110787", "110143", "22703", "10340"],
    },
    {
        "id": "sys-consumer",
        "name": "CONSUMER BANKING",
        "description": "Retail and consumer banking platforms",
        "cto": "Michael Torres",
        "seals": ["45210", "45320", "45115", "45440"],
    },
    {
        "id": "sys-data-platform",
        "name": "DATA PLATFORM",
        "description": "Data management and oversight",
        "cto": "Lakith Leelasena",
        "seals": ["25705", "85589", "86525"],
    },
]

SYSTEM_BY_ID = {s["id"]: s for s in SYSTEMS}

# ── Dropdown Options ─────────────────────────────────────────────────

TIMELINE_OPTIONS = [
    "T0 - Detected",
    "T1 - Acknowledged",
    "T2 - Mitigated",
    "T3 - Stable",
]

NEXT_UPDATE_OPTIONS = [
    "Every 15 min",
    "Every 30 min",
    "1 hr / significant milestones",
    "Every 2 hours (business hours)",
]

STATE_OPTIONS = ["Active", "Monitoring", "Mitigated", "Resolved"]
PRIORITY_OPTIONS = ["P1", "P2"]

# ── Situation Records (mutable) ──────────────────────────────────────

_next_situation_id = 3

SITUATIONS: list[dict] = [
    {
        "id": 1,
        "incident_number": "MINC55445241",
        "title": "8181 Communications Pkwy (Legacy West C Building), Plano, TX was on network SPOF",
        "incident_zoom": "",
        "wm_ait_zoom": "",
        "incident_lead": "",
        "opened_time": "2/23/2026",
        "state": "Resolved",
        "priority": "P1",
        "teams_channels": [],
        "time_period_days": 14,
        "system_overrides": {
            "sys-crm": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": ["CallAssist", "ProfileAssist360"],
                "sre_lead_overrides": ["Amit Nak"],
                "next_update": "Every 15 min",
            },
            "sys-ai-eng": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-architecture": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-trading": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-portfolio": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-payments": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-client-svc": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-ipb": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-consumer": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-data-platform": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
        },
        "escalation_notes": "At 12:15ET on 02/23, IP NRR reported that the primary network circuit provided by vendor AT&T is unavailable at the Legacy West C Building, creating a network single point of failure (SPOF) for the site.",
        "created_at": "2026-02-23T12:15:00Z",
        "updated_at": "2026-02-23T23:53:00Z",
    },
    {
        "id": 2,
        "incident_number": "MINC55446102",
        "title": "APAC Trading Platform Latency Degradation",
        "incident_zoom": "https://zoom.us/j/987654321",
        "wm_ait_zoom": "",
        "incident_lead": "Lakith Leelasena",
        "opened_time": "3/2/2026",
        "state": "Active",
        "priority": "P1",
        "teams_channels": ["#trading-war-room"],
        "time_period_days": 1,
        "system_overrides": {
            "sys-trading": {
                "timeline": "T1 - Acknowledged",
                "impacted_capabilities": ["Order Routing", "FX Execution"],
                "sre_lead_overrides": [],
                "next_update": "Every 15 min",
            },
            "sys-portfolio": {
                "timeline": "T0 - Detected",
                "impacted_capabilities": [],
                "sre_lead_overrides": [],
                "next_update": "Every 30 min",
            },
        },
        "escalation_notes": "Root cause: database failover in APAC region causing intermittent latency spikes on order routing path.",
        "created_at": "2026-03-02T22:45:00Z",
        "updated_at": "2026-03-03T04:10:00Z",
    },
]


# ── Helpers ──────────────────────────────────────────────────────────

_SEAL_TO_APP = {a["seal"]: a for a in APPS_REGISTRY}

STATUS_RANK = {"critical": 0, "warning": 1, "healthy": 2, "no_data": 3}
RANK_STATUS = {v: k for k, v in STATUS_RANK.items()}


def _resolve_sre_leads(seals: list[str], enriched_apps: list[dict]) -> list[dict]:
    """Find SRE-role team members for apps matching the given SEALs."""
    # Build seal -> team_ids from enriched apps
    team_ids = set()
    seal_set = set(seals)
    for app in enriched_apps:
        if app.get("seal") in seal_set:
            for tid in app.get("team_ids", []):
                team_ids.add(tid)

    # Find members with SRE role
    leads = []
    seen = set()
    for team in TEAMS:
        if team["id"] in team_ids:
            for m in team["members"]:
                if m["role"] == "SRE" and m["sid"] not in seen:
                    seen.add(m["sid"])
                    leads.append({
                        "sid": m["sid"],
                        "name": f"{m['firstName']} {m['lastName']}",
                        "email": m["email"],
                        "team": team["name"],
                    })
    return leads


def _get_all_components(seals: list[str], enriched_apps: list[dict]) -> list[str]:
    """Get all unique component labels for apps matching the given SEALs."""
    labels = set()
    seal_set = set(seals)
    for app in enriched_apps:
        if app.get("seal") in seal_set:
            for comp in app.get("components", []):
                labels.add(comp["label"])
    return sorted(labels)


def _worst_status(seals: list[str], enriched_apps: list[dict]) -> str:
    """Compute worst status across apps matching the given SEALs."""
    worst = 3  # no_data
    seal_set = set(seals)
    for app in enriched_apps:
        if app.get("seal") in seal_set:
            rank = STATUS_RANK.get(app.get("status", "no_data"), 3)
            if rank < worst:
                worst = rank
    return RANK_STATUS.get(worst, "no_data")


def compute_system_rows(situation: dict, enriched_apps: list[dict]) -> list[dict]:
    """Build the systems table for a situation with live status + user overrides."""
    overrides = situation.get("system_overrides", {})
    rows = []

    # Only include systems that have overrides (i.e. are part of this situation)
    # If no overrides, include all systems
    system_ids = list(overrides.keys()) if overrides else [s["id"] for s in SYSTEMS]

    for sys_id in system_ids:
        system = SYSTEM_BY_ID.get(sys_id)
        if not system:
            continue

        ovr = overrides.get(sys_id, {})
        sre_leads = _resolve_sre_leads(system["seals"], enriched_apps)
        all_capabilities = _get_all_components(system["seals"], enriched_apps)

        rows.append({
            "system_id": sys_id,
            "name": system["name"],
            "description": system["description"],
            "cto": system["cto"],
            "status": _worst_status(system["seals"], enriched_apps),
            "timeline": ovr.get("timeline", "T0 - Detected"),
            "impacted_capabilities": ovr.get("impacted_capabilities", []),
            "all_capabilities": all_capabilities,
            "sre_leads": sre_leads,
            "sre_lead_overrides": ovr.get("sre_lead_overrides", []),
            "next_update": ovr.get("next_update", "Every 15 min"),
            "app_count": len(system["seals"]),
        })

    return rows


def build_situation_report(situation: dict, enriched_apps: list[dict]) -> dict:
    """Build deep-dive report data for a situation: per-system, per-app, per-component."""
    overrides = situation.get("system_overrides", {})
    system_ids = list(overrides.keys()) if overrides else [s["id"] for s in SYSTEMS]

    systems_report = []
    for sys_id in system_ids:
        system = SYSTEM_BY_ID.get(sys_id)
        if not system:
            continue

        ovr = overrides.get(sys_id, {})
        seal_set = set(system["seals"])
        apps_detail = []

        for app in enriched_apps:
            if app.get("seal") not in seal_set:
                continue
            impacted_components = []
            for comp in app.get("components", []):
                if comp.get("status") in ("critical", "warning"):
                    impacted_components.append({
                        "label": comp["label"],
                        "status": comp["status"],
                        "indicator_type": comp.get("indicator_type", ""),
                    })
            apps_detail.append({
                "name": app["name"],
                "seal": app["seal"],
                "status": app.get("status", "no_data"),
                "impacted_components": impacted_components,
            })

        systems_report.append({
            "system_id": sys_id,
            "name": system["name"],
            "cto": system["cto"],
            "status": _worst_status(system["seals"], enriched_apps),
            "timeline": ovr.get("timeline", "T0 - Detected"),
            "impacted_capabilities": ovr.get("impacted_capabilities", []),
            "next_update": ovr.get("next_update", "Every 15 min"),
            "apps": apps_detail,
        })

    return {
        "incident_number": situation["incident_number"],
        "title": situation["title"],
        "state": situation["state"],
        "priority": situation["priority"],
        "incident_lead": situation.get("incident_lead", ""),
        "opened_time": situation.get("opened_time", ""),
        "escalation_notes": situation.get("escalation_notes", ""),
        "systems": systems_report,
    }
