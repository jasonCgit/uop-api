from fastapi import APIRouter, Query

from app.services.enrichment import (
    _filter_dashboard_apps,
    _get_enriched_apps,
)
from app.mock_data import (
    INCIDENT_TRENDS,
    INCIDENT_TREND_SUMMARY,
    _GLOBAL_ACTIVITY_CATEGORIES,
    _FREQUENT_ISSUE_TEMPLATES,
)

router = APIRouter()


@router.get("/api/health-summary")
def get_health_summary(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    if not apps:
        return {"critical_issues": 0, "warnings": 0, "recurring_30d": 0, "incidents_today": 0,
                "trends": {k: {"spark": [0]*7, "pct": 0} for k in ["critical_issues","warnings","recurring_30d","incidents_today"]}}
    crit = sum(1 for a in apps if a["status"] == "critical")
    warn = sum(1 for a in apps if a["status"] == "warning")
    rec = sum(a.get("recurring_30d", 0) for a in apps)
    inc = sum(a.get("incidents_today", 0) for a in apps)

    def _spark(val, trend_pct):
        if val == 0: return [0]*7
        base = max(1, int(val / (1 + trend_pct/100))) if trend_pct != -100 else val
        return [max(0, base + i) for i in [2,1,1,0,1,0,0]][:7]

    return {
        "critical_issues": crit, "warnings": warn, "recurring_30d": rec, "incidents_today": inc,
        "trends": {
            "critical_issues": {"spark": _spark(crit, -33), "pct": -33 if crit > 0 else 0},
            "warnings":        {"spark": _spark(warn, -50), "pct": -50 if warn > 0 else 0},
            "recurring_30d":   {"spark": _spark(rec, 21),   "pct": 21 if rec > 0 else 0},
            "incidents_today": {"spark": _spark(inc, -38),  "pct": -38 if inc > 0 else 0},
        },
    }


@router.get("/api/ai-analysis")
def get_ai_analysis(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    if not apps:
        return {"critical_alert": "No applications match the current filter scope.", "trend_analysis": "", "recommendations": []}
    crits = [a for a in apps if a["status"] == "critical"]
    warns = [a for a in apps if a["status"] == "warning"]
    total_inc = sum(a.get("incidents_30d", 0) for a in apps)
    scope_label = lob[0] if lob and len(lob) == 1 else "the selected scope"
    if crits:
        names = " and ".join(a["name"] for a in crits[:3])
        alert = f"Currently tracking {len(crits)} critical application{'s' if len(crits)>1 else ''} in {scope_label}. {names} {'are' if len(crits)>1 else 'is'} experiencing active incidents requiring immediate attention."
    elif warns:
        alert = f"No critical issues in {scope_label}. {len(warns)} application{'s' if len(warns)>1 else ''} with warnings being monitored."
    else:
        alert = f"All {len(apps)} applications in {scope_label} are operating normally. No active issues detected."
    trend_msg = f"{total_inc} incidents recorded across {len(apps)} applications in the last 30 days." if total_inc > 0 else f"No incidents across {len(apps)} applications in the last 30 days."
    recs = []
    for a in crits[:2]:
        issues = a.get("recent_issues", [])
        desc = issues[0]["description"] if issues else "active critical issue"
        recs.append(f"Investigate {a['name']} — {desc}")
    for a in warns[:2]:
        issues = a.get("recent_issues", [])
        desc = issues[0]["description"] if issues else "warning condition"
        recs.append(f"Monitor {a['name']} — {desc}")
    if not recs:
        recs.append("Continue monitoring — all systems healthy in current scope")
    return {"critical_alert": alert, "trend_analysis": trend_msg, "recommendations": recs}


@router.get("/api/regional-status")
def get_regional_status(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    regions = {}
    for a in apps:
        r = a.get("region", "NA")
        if r not in regions:
            regions[r] = {"region": r, "status": "healthy", "sod_impacts": 0, "app_issues": 0}
        if a["status"] == "critical":
            regions[r]["status"] = "critical"
            regions[r]["sod_impacts"] += 1
            regions[r]["app_issues"] += a.get("incidents_today", 0)
        elif a["status"] == "warning" and regions[r]["status"] != "critical":
            regions[r]["status"] = "warning"
            regions[r]["app_issues"] += a.get("incidents_today", 0)
    for rname in ["NA", "EMEA", "APAC"]:
        if rname not in regions:
            regions[rname] = {"region": rname, "status": "healthy", "sod_impacts": 0, "app_issues": 0}
    return sorted(regions.values(), key=lambda r: {"NA":0,"EMEA":1,"APAC":2}.get(r["region"],3))


@router.get("/api/critical-apps")
def get_critical_apps(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    crits = [a for a in apps if a["status"] == "critical"]
    return [{
        "id": a["seal"],
        "name": a["name"],
        "seal": f"SEAL - {a['seal']}",
        "status": "critical",
        "current_issues": len(a.get("recent_issues", [])),
        "recurring_30d": a.get("recurring_30d", 0),
        "last_incident": (a.get("recent_issues", [{}])[0].get("time_ago", "\u2014") if a.get("recent_issues") else "\u2014"),
        "recent_issues": a.get("recent_issues", []),
    } for a in crits]


@router.get("/api/warning-apps")
def get_warning_apps(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    warns = [a for a in apps if a["status"] == "warning"]
    return [{
        "id": a["seal"],
        "name": a["name"],
        "seal": f"SEAL - {a['seal']}",
        "status": "warning",
        "current_issues": len(a.get("recent_issues", [])),
        "recurring_30d": a.get("recurring_30d", 0),
        "last_incident": (a.get("recent_issues", [{}])[0].get("time_ago", "\u2014") if a.get("recent_issues") else "\u2014"),
        "recent_issues": a.get("recent_issues", []),
    } for a in warns]


@router.get("/api/incident-trends")
def get_incident_trends(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    total_p1 = sum(a.get("p1_30d", 0) for a in apps)
    total_p2 = sum(a.get("p2_30d", 0) for a in apps)
    all_apps = _get_enriched_apps()
    all_p1 = sum(a.get("p1_30d", 0) for a in all_apps)
    all_p2 = sum(a.get("p2_30d", 0) for a in all_apps)
    p1_ratio = total_p1 / all_p1 if all_p1 else 0
    p2_ratio = total_p2 / all_p2 if all_p2 else 0
    scaled = []
    for week in INCIDENT_TRENDS:
        scaled.append({
            "week": week["week"], "label": week["label"],
            "p1": max(0, round(week["p1"] * p1_ratio)),
            "p2": max(0, round(week["p2"] * p2_ratio)),
        })
    total_inc = sum(a.get("incidents_30d", 0) for a in apps)
    res_rate = 94.2 if total_inc > 5 else 100.0 if total_inc == 0 else 88.0
    return {"data": scaled, "summary": {**INCIDENT_TREND_SUMMARY, "resolution_rate": res_rate}}


@router.get("/api/frequent-incidents")
def get_frequent_incidents(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    ranked = sorted(apps, key=lambda a: a.get("recurring_30d", 0), reverse=True)
    result = []
    for i, a in enumerate(ranked[:6]):
        if a.get("recurring_30d", 0) == 0 and a.get("incidents_30d", 0) == 0:
            break
        issues = a.get("recent_issues", [])
        desc = issues[0]["description"] if issues else _FREQUENT_ISSUE_TEMPLATES[i % len(_FREQUENT_ISSUE_TEMPLATES)]
        result.append({
            "app": a["name"],
            "seal": a["seal"],
            "status": a["status"],
            "description": desc,
            "occurrences": a.get("recurring_30d", 0) + a.get("incidents_today", 0),
            "last_seen": issues[0]["time_ago"] if issues else "\u2014",
        })
    return result


@router.get("/api/active-incidents")
def get_active_incidents(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    p1_total = sum(a.get("p1_30d", 0) for a in apps)
    p2_total = sum(a.get("p2_30d", 0) for a in apps)
    p1_unresolved = sum(1 for a in apps if a["status"] == "critical")
    p2_unresolved = max(1, p2_total // 3) if p2_total > 0 else 0
    return {
        "week_label": "Last 7 Days",
        "p1": {
            "total": p1_total,
            "trend": -33 if p1_total > 0 else 0,
            "breakdown": [
                {"label": "Unresolved", "count": p1_unresolved, "color": "#f44336"},
                {"label": "Resolved",   "count": max(0, p1_total - p1_unresolved), "color": "#4ade80"},
            ],
        },
        "p2": {
            "total": p2_total,
            "trend": -20 if p2_total > 0 else 0,
            "breakdown": [
                {"label": "Unresolved", "count": p2_unresolved, "color": "#ffab00"},
                {"label": "Resolved",   "count": max(0, p2_total - p2_unresolved), "color": "#4ade80"},
            ],
        },
        "convey": {
            "total": max(1, len(apps) // 5),
            "trend": -20,
            "breakdown": [
                {"label": "Unresolved", "count": max(0, len(apps) // 10), "color": "#60a5fa"},
                {"label": "Resolved",   "count": max(1, len(apps) // 5) - max(0, len(apps) // 10), "color": "#4ade80"},
            ],
        },
        "spectrum": {
            "total": max(1, len(apps) // 6),
            "trend": 0,
            "breakdown": [
                {"label": "Info", "count": max(1, len(apps) // 8), "color": "#60a5fa"},
                {"label": "High", "count": max(0, max(1, len(apps) // 6) - max(1, len(apps) // 8)), "color": "#f44336"},
            ],
        },
    }


@router.get("/api/recent-activities")
def get_recent_activities(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    p1_items = []
    for a in apps:
        if a["status"] == "critical":
            for issue in a.get("recent_issues", []):
                p1_items.append({"status": "CRITICAL", "description": f"{a['name']} \u2014 {issue['description']}", "time_ago": issue["time_ago"]})
    if not p1_items:
        p1_items = [{"status": "OK", "description": "No active P1 incidents in current scope", "time_ago": "\u2014"}]
    p2_items = []
    for a in apps:
        for issue in a.get("recent_issues", []):
            if issue.get("severity") == "warning":
                p2_items.append({"status": "UNRESOLVED", "description": f"{a['name']} \u2014 {issue['description']}", "time_ago": issue["time_ago"]})
    if not p2_items:
        p2_items = [{"status": "OK", "description": "No active P2 incidents in current scope", "time_ago": "\u2014"}]
    return [
        {"category": "P1 INCIDENTS", "color": "#f44336", "items": p1_items[:3]},
        {"category": "P2 INCIDENTS", "color": "#ff9800", "items": p2_items[:3]},
        *_GLOBAL_ACTIVITY_CATEGORIES,
    ]
