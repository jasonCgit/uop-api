# REAL: Replace with ServiceNow incident API


def _build_incident_trends():
    """Daily incident data aggregated into weekly buckets (90 days / ~13 weeks).
    P1: ~15 total, max 2/day.  P2: ~480 total, max 15/day."""
    from datetime import date, timedelta

    today = date.today()
    # Build daily data first (same as original)
    p1_days_map = {3:1, 12:1, 17:1, 24:2, 31:1, 38:1, 45:1, 52:2, 58:1, 65:1, 72:1, 80:1, 87:1, 90:1}
    p2_daily = [
        10, 5, 8, 3, 7, 6, 14, 2, 5, 10,   7, 3, 6, 5, 8, 1, 6, 4, 9, 3,
         5, 3, 8, 1, 4, 6, 3, 8, 4, 5,   7, 2, 4, 3, 8, 6, 5, 2, 4, 7,
         3, 9, 5, 3, 12, 4, 6, 2, 11, 3,  4, 5, 3, 7, 6, 2, 4, 8, 3, 5,
         7, 2, 15, 8, 4, 3, 5, 7, 2, 11,  4, 5, 3, 6, 10, 7, 2, 10, 5, 3,
         4, 2, 6, 3, 5, 4, 9, 3, 2, 1,
    ]
    daily = []
    for i in range(90):
        d = today - timedelta(days=89 - i)
        daily.append({
            "date": d,
            "p1": p1_days_map.get(i + 1, 0),
            "p2": p2_daily[i],
        })

    # Aggregate into weeks (Mon-Sun)
    weeks = {}
    for day in daily:
        # ISO week start (Monday)
        wk_start = day["date"] - timedelta(days=day["date"].weekday())
        key = wk_start.strftime("%Y-%m-%d")
        if key not in weeks:
            weeks[key] = {"week": key, "label": wk_start.strftime("%b %d"), "p1": 0, "p2": 0}
        weeks[key]["p1"] += day["p1"]
        weeks[key]["p2"] += day["p2"]

    return sorted(weeks.values(), key=lambda w: w["week"])

INCIDENT_TRENDS = _build_incident_trends()

INCIDENT_TREND_SUMMARY = {
    "mttr_hours": 2.4,
    "mtta_minutes": 8,
    "resolution_rate": 94.2,
    "escalation_rate": 12,
}


# Platform-wide notification categories (not app-specific, shown globally)
_GLOBAL_ACTIVITY_CATEGORIES = [
    {
        "category": "CONVEY NOTIFICATIONS",
        "color": "#60a5fa",
        "items": [
            {"status": "UNRESOLVED", "description": "Starting Feb 26, all Flipper tasks targeting Production Load Balancers will be blocked and need to be re-targeted.", "time_ago": "22h ago"},
            {"status": "RESOLVED", "description": "Rest of the NAMR alerts are ready to review.", "time_ago": "23h ago"},
            {"status": "UNRESOLVED", "description": "Fees and Billing — Invoice delivery will be down 15 min between 8–10 PM ET for maintenance.", "time_ago": "1d ago"},
        ],
    },
    {
        "category": "SPECTRUM ALERTS",
        "color": "#a78bfa",
        "items": [
            {"status": "INFO", "description": "EMEA MAS: SPMMA has migrated accounts 501388 and 72301 to Axis. Remaining accounts in subsequent phases.", "time_ago": "20h ago"},
            {"status": "WARNING", "description": "Elevated login failure rate on User Authentication service (SEAL-92156)", "time_ago": "4h ago"},
        ],
    },
    {
        "category": "DEPLOYMENTS",
        "color": "#4ade80",
        "items": [
            {"status": "SUCCESS", "description": "Connect OS v3.14.2 deployed to production (SEAL-88180)", "time_ago": "22m ago"},
            {"status": "SUCCESS", "description": "Advisor Connect hotfix v2.8.1 — DB connection pool fix rolled out", "time_ago": "1h ago"},
            {"status": "SUCCESS", "description": "Trade Execution Engine v5.2.0 deployed — order queue optimization", "time_ago": "8h ago"},
        ],
    },
]

# Template descriptions for deriving frequent incidents from enriched app data
_FREQUENT_ISSUE_TEMPLATES = [
    "Database connection timeout",
    "Connection pool exhaustion",
    "Elevated error rate",
    "Memory pressure on primary service",
    "Latency spike on core endpoint",
    "Upstream feed delay",
    "Intermittent routing failures",
    "Cache invalidation storm",
]
