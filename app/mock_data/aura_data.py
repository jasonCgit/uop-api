# REAL: Replace with AURA AI Streaming API

import uuid
from datetime import datetime


def _aura_incident_analysis():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the current incident analysis for your environment. I'm tracking 2 critical and 1 warning application across all regions."},
            {"type": "metric_cards", "data": [
                {"label": "Active P1s", "value": 2, "color": "#f44336", "trend": -33, "icon": "error", "sparkline": [5, 4, 6, 3, 4, 3, 2]},
                {"label": "Active P2s", "value": 5, "color": "#ff9800", "trend": 12, "icon": "warning", "sparkline": [3, 4, 3, 5, 4, 6, 5]},
                {"label": "MTTR (avg)", "value": "2.4h", "color": "#60a5fa", "trend": -18, "icon": "timer", "sparkline": [3.8, 3.5, 3.2, 2.9, 2.7, 2.5, 2.4]},
                {"label": "Affected Users", "value": "6,220", "color": "#a78bfa", "trend": -5, "icon": "people", "sparkline": [8200, 7800, 7200, 6800, 6500, 6400, 6220]},
            ]},
            {"type": "status_list", "title": "Affected Applications", "data": [
                {"name": "GWM Global Collateral Mgmt", "status": "critical", "detail": "Database connection timeout — recurring pattern in APAC", "seal": "SEAL-90083"},
                {"name": "Payment Gateway API", "status": "critical", "detail": "Connection pool exhaustion on primary DB cluster", "seal": "SEAL-90176"},
                {"name": "User Authentication Service", "status": "warning", "detail": "Elevated login failure rate — 3.2% (threshold 2%)", "seal": "SEAL-92156"},
            ]},
            {"type": "recommendations", "data": [
                {"priority": "high", "text": "Scale database connection pool for GWM Collateral service from 50 to 150 connections", "impact": "Reduces timeout incidents by ~60%"},
                {"priority": "high", "text": "Implement circuit breaker on Payment Gateway upstream calls", "impact": "Prevents cascade failures to 12 downstream services"},
                {"priority": "medium", "text": "Review APAC infrastructure capacity — recurring pattern suggests undersizing", "impact": "Addresses root cause of 67% of recent P1s"},
            ]},
        ],
        "suggested_followups": [
            "What is the blast radius of the Payment Gateway issue?",
            "Show me the MTTR trend for the last quarter",
            "Give me an executive summary for leadership",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_slo_report():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the SLO compliance report across all monitored services. 3 services are currently burning error budget faster than expected."},
            {"type": "metric_cards", "data": [
                {"label": "Overall SLO", "value": "94.2%", "color": "#4caf50", "trend": -1.3, "icon": "check", "sparkline": [95.1, 94.8, 94.5, 94.3, 94.1, 94.0, 94.2]},
                {"label": "Error Budget Left", "value": "38%", "color": "#ff9800", "trend": -12, "icon": "data_usage", "sparkline": [62, 55, 50, 46, 42, 40, 38]},
                {"label": "Services at Risk", "value": 3, "color": "#f44336", "trend": 50, "icon": "error", "sparkline": [1, 1, 2, 2, 2, 3, 3]},
                {"label": "Services Healthy", "value": 41, "color": "#4caf50", "trend": 2, "icon": "check_circle", "sparkline": [38, 39, 39, 40, 40, 41, 41]},
            ]},
            {"type": "table", "title": "SLO Compliance by Service", "data": {
                "columns": ["Service", "SLO Target", "Current", "Error Budget", "Status"],
                "rows": [
                    ["GWM Global Collateral", "99.9%", "98.2%", "12%", "critical"],
                    ["Payment Gateway API", "99.95%", "99.1%", "22%", "warning"],
                    ["User Auth Service", "99.9%", "99.4%", "45%", "warning"],
                    ["Trading Engine", "99.99%", "99.98%", "89%", "healthy"],
                    ["Market Data Feed", "99.9%", "99.85%", "78%", "healthy"],
                    ["Risk Calculator", "99.5%", "99.6%", "92%", "healthy"],
                    ["Notification Hub", "99.9%", "99.7%", "67%", "healthy"],
                ],
            }},
            {"type": "bar_chart", "title": "Error Budget Remaining by Team", "data": {
                "bars": [
                    {"name": "Collateral", "value": 12, "color": "#f44336"},
                    {"name": "Payments", "value": 22, "color": "#ff9800"},
                    {"name": "Security", "value": 45, "color": "#ff9800"},
                    {"name": "Trading", "value": 89, "color": "#4caf50"},
                    {"name": "Data", "value": 78, "color": "#4caf50"},
                    {"name": "Risk", "value": 92, "color": "#4caf50"},
                ],
                "xKey": "name",
                "yKey": "value",
                "unit": "%",
            }},
        ],
        "suggested_followups": [
            "What's causing the GWM Collateral SLO breach?",
            "Show capacity planning recommendations",
            "How are the engineering teams performing?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_blast_radius():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "I've analyzed the blast radius for a potential Payment Gateway failure. This service sits on a critical path — a full outage would cascade to 14 downstream services across 3 teams."},
            {"type": "status_list", "title": "Cascade Impact Chain", "data": [
                {"name": "Payment Gateway API", "status": "critical", "detail": "Primary failure point — connection pool exhaustion", "seal": "SEAL-90176"},
                {"name": "Order Processing Service", "status": "critical", "detail": "Direct dependency — all orders would fail", "seal": "SEAL-91002"},
                {"name": "Invoice Generator", "status": "critical", "detail": "Cannot generate invoices without payment confirmation", "seal": "SEAL-91045"},
                {"name": "Settlement Engine", "status": "warning", "detail": "Queued transactions would back up within 15 min", "seal": "SEAL-91078"},
                {"name": "Client Portal Dashboard", "status": "warning", "detail": "Payment status widgets would show stale data", "seal": "SEAL-92200"},
                {"name": "Mobile Banking App", "status": "warning", "detail": "Payment flows degraded, other features unaffected", "seal": "SEAL-92301"},
            ]},
            {"type": "pie_chart", "title": "Impact by Team", "data": {
                "slices": [
                    {"label": "Payments", "value": 5, "color": "#f44336"},
                    {"label": "Trading", "value": 4, "color": "#ff9800"},
                    {"label": "Client Exp.", "value": 3, "color": "#60a5fa"},
                    {"label": "Operations", "value": 2, "color": "#a78bfa"},
                ],
                "trend": 15,
            }},
            {"type": "recommendations", "data": [
                {"priority": "high", "text": "Implement async fallback queue for Order Processing Service", "impact": "Allows 30-min degraded operation without data loss"},
                {"priority": "high", "text": "Add read replica for Settlement Engine queries", "impact": "Reduces blast radius by isolating read vs write paths"},
                {"priority": "medium", "text": "Enable circuit breaker with 5s timeout on all downstream callers", "impact": "Prevents cascade propagation beyond direct dependencies"},
            ]},
        ],
        "suggested_followups": [
            "Show me the full dependency graph for Payment Gateway",
            "What is the current incident status?",
            "Compare regional health across NA, EMEA, and APAC",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_mttr_analysis():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the MTTR and MTTA analysis for the last quarter. Overall resolution times have improved 18% driven by the new automated runbook adoption."},
            {"type": "metric_cards", "data": [
                {"label": "Avg MTTR", "value": "2.4h", "color": "#60a5fa", "trend": -18, "icon": "timer", "sparkline": [3.8, 3.5, 3.2, 2.9, 2.7, 2.5, 2.4]},
                {"label": "Avg MTTA", "value": "4.2m", "color": "#4caf50", "trend": -25, "icon": "notifications", "sparkline": [6.5, 6.0, 5.5, 5.0, 4.8, 4.5, 4.2]},
                {"label": "Resolution Rate", "value": "94.2%", "color": "#4caf50", "trend": 3, "icon": "check_circle", "sparkline": [89, 90, 91, 92, 93, 93, 94]},
                {"label": "Escalation Rate", "value": "12%", "color": "#ff9800", "trend": -8, "icon": "trending_down", "sparkline": [18, 16, 15, 14, 13, 13, 12]},
            ]},
            {"type": "line_chart", "title": "MTTR Trend (12 Weeks)", "data": {
                "series": [
                    {"key": "mttr", "name": "MTTR (hours)", "color": "#60a5fa", "showTrendLine": True, "showLabeledDots": True},
                    {"key": "mtta", "name": "MTTA (minutes)", "color": "#4caf50", "showTrendLine": True, "showLabeledDots": True},
                ],
                "stats": [
                    {"label": "MTTR", "value": "2.4h", "color": "#60a5fa", "trend": -18},
                    {"label": "MTTA", "value": "4.2m", "color": "#4caf50", "trend": -25},
                ],
                "points": [
                    {"label": "W1", "mttr": 3.8, "mtta": 6.5},
                    {"label": "W2", "mttr": 3.5, "mtta": 6.0},
                    {"label": "W3", "mttr": 3.2, "mtta": 5.8},
                    {"label": "W4", "mttr": 3.6, "mtta": 5.5},
                    {"label": "W5", "mttr": 2.9, "mtta": 5.0},
                    {"label": "W6", "mttr": 2.7, "mtta": 4.8},
                    {"label": "W7", "mttr": 2.8, "mtta": 4.5},
                    {"label": "W8", "mttr": 2.5, "mtta": 4.2},
                    {"label": "W9", "mttr": 2.3, "mtta": 4.0},
                    {"label": "W10", "mttr": 2.6, "mtta": 4.3},
                    {"label": "W11", "mttr": 2.2, "mtta": 3.8},
                    {"label": "W12", "mttr": 2.4, "mtta": 4.2},
                ],
            }},
            {"type": "table", "title": "MTTR by Team", "data": {
                "columns": ["Team", "Avg MTTR", "Avg MTTA", "Incidents Handled", "Resolution Rate"],
                "rows": [
                    ["Security", "1.2h", "2.1m", 18, "97%"],
                    ["Trading", "1.8h", "3.5m", 24, "95%"],
                    ["Payments", "2.9h", "4.8m", 31, "92%"],
                    ["Collateral", "3.4h", "5.2m", 22, "88%"],
                    ["Data Platform", "2.1h", "3.8m", 15, "96%"],
                ],
            }},
        ],
        "suggested_followups": [
            "Why is Collateral team's MTTR so high?",
            "Show me the team performance breakdown",
            "What's the executive summary?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_executive_summary():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Good morning. Here's your executive platform health briefing. Overall stability has improved week-over-week, though two critical applications require continued attention."},
            {"type": "metric_cards", "data": [
                {"label": "Platform Health", "value": "94.2%", "color": "#4caf50", "trend": 1.5, "icon": "health", "sparkline": [91.5, 92.0, 92.8, 93.2, 93.5, 94.0, 94.2]},
                {"label": "Availability", "value": "99.87%", "color": "#4caf50", "trend": 0.02, "icon": "cloud", "sparkline": [99.82, 99.83, 99.84, 99.85, 99.85, 99.86, 99.87]},
                {"label": "Active Incidents", "value": 7, "color": "#ff9800", "trend": -22, "icon": "warning", "sparkline": [12, 10, 9, 11, 8, 9, 7]},
                {"label": "Est. Impact", "value": "$142K", "color": "#f44336", "trend": -35, "icon": "money", "sparkline": [280, 240, 210, 195, 180, 160, 142]},
            ]},
            {"type": "bar_chart", "title": "Incidents by Line of Business", "data": {
                "bars": [
                    {"name": "GWM", "value": 14, "color": "#f44336"},
                    {"name": "IB", "value": 9, "color": "#ff9800"},
                    {"name": "Consumer", "value": 7, "color": "#60a5fa"},
                    {"name": "Operations", "value": 5, "color": "#a78bfa"},
                    {"name": "Corporate", "value": 3, "color": "#34d399"},
                ],
                "xKey": "name",
                "yKey": "value",
            }},
            {"type": "line_chart", "title": "Weekly Incident Trend", "data": {
                "series": [
                    {"key": "p1", "name": "P1 Incidents", "color": "#f44336", "showTrendLine": True, "showLabeledDots": True},
                    {"key": "p2", "name": "P2 Incidents", "color": "#ffab00", "showTrendLine": True, "showLabeledDots": True},
                ],
                "stats": [
                    {"label": "P1", "value": 18, "color": "#f44336", "trend": -29},
                    {"label": "P2", "value": 137, "color": "#ffab00", "trend": -10},
                    {"label": "Resolved", "value": "94.2%", "color": "#4caf50"},
                ],
                "points": [
                    {"label": "W1", "p1": 3, "p2": 18},
                    {"label": "W2", "p1": 2, "p2": 22},
                    {"label": "W3", "p1": 4, "p2": 19},
                    {"label": "W4", "p1": 1, "p2": 15},
                    {"label": "W5", "p1": 2, "p2": 20},
                    {"label": "W6", "p1": 3, "p2": 17},
                    {"label": "W7", "p1": 1, "p2": 14},
                    {"label": "W8", "p1": 2, "p2": 12},
                ],
            }},
            {"type": "recommendations", "data": [
                {"priority": "high", "text": "Prioritize database infrastructure upgrade for APAC region", "impact": "Addresses root cause of 67% of P1 incidents"},
                {"priority": "medium", "text": "Accelerate automated runbook rollout to Collateral team", "impact": "Expected 40% MTTR improvement"},
                {"priority": "low", "text": "Schedule quarterly architecture review for high-incident services", "impact": "Proactive risk reduction for next quarter"},
            ]},
        ],
        "suggested_followups": [
            "Drill into the GWM incidents",
            "Show me SLO compliance details",
            "How are engineering teams performing?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_capacity_planning():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the current capacity utilization analysis. Three services are approaching their resource limits and should be reviewed for scaling before the next quarter."},
            {"type": "bar_chart", "title": "Resource Utilization by Service (%)", "data": {
                "bars": [
                    {"name": "Payment DB", "value": 92, "color": "#f44336"},
                    {"name": "Auth Cache", "value": 87, "color": "#f44336"},
                    {"name": "Trade Engine", "value": 78, "color": "#ff9800"},
                    {"name": "Msg Queue", "value": 65, "color": "#60a5fa"},
                    {"name": "Risk Calc", "value": 52, "color": "#4caf50"},
                    {"name": "Data Lake", "value": 44, "color": "#4caf50"},
                ],
                "xKey": "name",
                "yKey": "value",
                "unit": "%",
            }},
            {"type": "table", "title": "Services Approaching Limits", "data": {
                "columns": ["Service", "CPU", "Memory", "Disk", "Projected Full"],
                "rows": [
                    ["Payment DB Primary", "92%", "88%", "76%", "3 weeks"],
                    ["Auth Redis Cluster", "87%", "91%", "45%", "5 weeks"],
                    ["Trading Engine", "78%", "72%", "68%", "8 weeks"],
                ],
            }},
            {"type": "recommendations", "data": [
                {"priority": "high", "text": "Scale Payment DB from 4 to 8 read replicas and increase connection pool", "impact": "Extends capacity runway to 6+ months"},
                {"priority": "high", "text": "Migrate Auth Redis to clustered mode with 3 additional shards", "impact": "Reduces memory pressure by 60%"},
                {"priority": "medium", "text": "Enable auto-scaling for Trading Engine compute tier", "impact": "Handles peak loads without manual intervention"},
            ]},
        ],
        "suggested_followups": [
            "What's the cost estimate for scaling Payment DB?",
            "Show me the deployment status",
            "What are the current active incidents?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_deployment_status():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the deployment activity for the past 7 days. 23 deployments completed with a 91% success rate. Two rollbacks occurred due to integration test failures."},
            {"type": "table", "title": "Recent Deployments", "data": {
                "columns": ["Service", "Version", "Time", "Status", "Deployer"],
                "rows": [
                    ["Payment Gateway API", "v3.12.1", "2h ago", "healthy", "CI/CD"],
                    ["User Auth Service", "v2.8.0", "5h ago", "healthy", "Jenkins"],
                    ["GWM Collateral", "v4.1.3", "8h ago", "rollback", "CI/CD"],
                    ["Trading Engine", "v7.22.0", "1d ago", "healthy", "ArgoCD"],
                    ["Risk Calculator", "v1.15.2", "1d ago", "healthy", "CI/CD"],
                    ["Notification Hub", "v2.3.1", "2d ago", "rollback", "Jenkins"],
                    ["Market Data Feed", "v5.9.0", "3d ago", "healthy", "ArgoCD"],
                ],
            }},
            {"type": "pie_chart", "title": "Deployment Outcomes (7 Days)", "data": {
                "slices": [
                    {"label": "Successful", "value": 21, "color": "#4caf50"},
                    {"label": "Rolled Back", "value": 2, "color": "#f44336"},
                ],
                "trend": -8,
            }},
            {"type": "status_list", "title": "Upcoming Scheduled Deployments", "data": [
                {"name": "Payment Gateway API v3.13.0", "status": "healthy", "detail": "Scheduled: Tomorrow 2:00 AM EST — connection pool fix", "seal": "SEAL-90176"},
                {"name": "GWM Collateral v4.2.0", "status": "warning", "detail": "Scheduled: Friday 11:00 PM EST — DB migration included", "seal": "SEAL-90083"},
            ]},
        ],
        "suggested_followups": [
            "Why did the GWM Collateral deployment roll back?",
            "Show me the incident analysis",
            "What are the SLO compliance numbers?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_alert_analysis():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "I've analyzed your alerting patterns for the past 30 days. Alert noise is at 34%, meaning roughly 1 in 3 alerts doesn't require human action. Here's the breakdown."},
            {"type": "metric_cards", "data": [
                {"label": "Total Alerts", "value": "1,247", "color": "#60a5fa", "trend": 8, "icon": "notifications", "sparkline": [980, 1020, 1050, 1100, 1150, 1200, 1247]},
                {"label": "Actionable", "value": "66%", "color": "#4caf50", "trend": 5, "icon": "check", "sparkline": [58, 60, 61, 63, 64, 65, 66]},
                {"label": "Noise Rate", "value": "34%", "color": "#f44336", "trend": -3, "icon": "volume_off", "sparkline": [42, 40, 39, 37, 36, 35, 34]},
                {"label": "Avg Response", "value": "4.2m", "color": "#60a5fa", "trend": -12, "icon": "timer", "sparkline": [5.8, 5.5, 5.2, 4.9, 4.6, 4.4, 4.2]},
            ]},
            {"type": "bar_chart", "title": "Alert Volume by Source", "data": {
                "bars": [
                    {"name": "Prometheus", "value": 423, "color": "#f44336"},
                    {"name": "Datadog", "value": 312, "color": "#a78bfa"},
                    {"name": "PagerDuty", "value": 198, "color": "#60a5fa"},
                    {"name": "Custom", "value": 167, "color": "#34d399"},
                    {"name": "CloudWatch", "value": 147, "color": "#ff9800"},
                ],
                "xKey": "name",
                "yKey": "value",
            }},
            {"type": "table", "title": "Noisiest Alerting Rules", "data": {
                "columns": ["Rule Name", "Triggers (30d)", "Actionable", "Noise %", "Owner"],
                "rows": [
                    ["CPU > 80% (5min)", 89, 12, "87%", "Platform"],
                    ["Memory > 90%", 67, 23, "66%", "Platform"],
                    ["Latency P99 > 500ms", 54, 38, "30%", "SRE"],
                    ["Error Rate > 1%", 43, 41, "5%", "SRE"],
                    ["Disk > 85%", 38, 8, "79%", "Platform"],
                ],
            }},
            {"type": "recommendations", "data": [
                {"priority": "high", "text": "Increase CPU alert threshold from 80% to 90% with 15-min window", "impact": "Eliminates ~77 false alerts per month"},
                {"priority": "high", "text": "Add auto-resolve for memory alerts that self-heal within 5 minutes", "impact": "Reduces noise by ~44 alerts per month"},
                {"priority": "medium", "text": "Consolidate disk alerts to daily digest instead of real-time", "impact": "Reduces alert fatigue for non-urgent capacity issues"},
            ]},
        ],
        "suggested_followups": [
            "How can we improve our MTTA?",
            "Show me the incident trends",
            "What's the team performance on alert response?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_regional_comparison():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the regional operational health comparison. APAC is currently the most impacted region, driven primarily by database infrastructure issues affecting the GWM platform."},
            {"type": "metric_cards", "data": [
                {"label": "NA Health", "value": "97.1%", "color": "#4caf50", "trend": 0.3, "icon": "public", "sparkline": [96.2, 96.5, 96.7, 96.8, 96.9, 97.0, 97.1]},
                {"label": "EMEA Health", "value": "95.8%", "color": "#4caf50", "trend": -0.5, "icon": "public", "sparkline": [96.5, 96.3, 96.1, 96.0, 95.9, 95.8, 95.8]},
                {"label": "APAC Health", "value": "89.4%", "color": "#f44336", "trend": -2.1, "icon": "public", "sparkline": [93.2, 92.5, 91.8, 91.0, 90.5, 90.0, 89.4]},
                {"label": "LATAM Health", "value": "96.2%", "color": "#4caf50", "trend": 1.2, "icon": "public", "sparkline": [94.8, 95.0, 95.3, 95.5, 95.8, 96.0, 96.2]},
            ]},
            {"type": "bar_chart", "title": "Incidents by Region (30 Days)", "data": {
                "bars": [
                    {"name": "NA", "value": 12, "color": "#60a5fa"},
                    {"name": "EMEA", "value": 18, "color": "#a78bfa"},
                    {"name": "APAC", "value": 31, "color": "#f44336"},
                    {"name": "LATAM", "value": 7, "color": "#34d399"},
                ],
                "xKey": "name",
                "yKey": "value",
            }},
            {"type": "table", "title": "Regional SLA Comparison", "data": {
                "columns": ["Region", "Availability", "Avg Latency", "P1 Count", "MTTR", "Status"],
                "rows": [
                    ["North America", "99.95%", "45ms", 2, "1.8h", "healthy"],
                    ["EMEA", "99.88%", "62ms", 4, "2.2h", "healthy"],
                    ["APAC", "99.12%", "128ms", 8, "3.6h", "critical"],
                    ["LATAM", "99.91%", "78ms", 1, "1.5h", "healthy"],
                ],
            }},
        ],
        "suggested_followups": [
            "Why is APAC health degraded?",
            "Show me capacity planning for APAC",
            "What's the executive summary?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_trend_forecast():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Based on the last 12 weeks of data and seasonal patterns, here's the projected incident forecast. The model suggests a continued downward trend in P1s, but P2 volume may increase slightly due to upcoming deployment activity."},
            {"type": "line_chart", "title": "Incident Forecast (Historical + Projected)", "data": {
                "series": [
                    {"key": "actual", "name": "Actual", "color": "#60a5fa", "showTrendLine": True, "showLabeledDots": True},
                    {"key": "forecast", "name": "Forecast", "color": "#60a5fa", "dashed": True},
                ],
                "stats": [
                    {"label": "Actual (Avg)", "value": "24.3", "color": "#60a5fa", "trend": -18},
                    {"label": "Forecast", "value": "15.5", "color": "#a78bfa", "trend": -36},
                ],
                "points": [
                    {"label": "W-8", "actual": 28, "forecast": None},
                    {"label": "W-7", "actual": 32, "forecast": None},
                    {"label": "W-6", "actual": 25, "forecast": None},
                    {"label": "W-5", "actual": 22, "forecast": None},
                    {"label": "W-4", "actual": 27, "forecast": None},
                    {"label": "W-3", "actual": 20, "forecast": None},
                    {"label": "W-2", "actual": 18, "forecast": None},
                    {"label": "W-1", "actual": 19, "forecast": 19},
                    {"label": "This Wk", "actual": None, "forecast": 17},
                    {"label": "Next Wk", "actual": None, "forecast": 15},
                    {"label": "W+2", "actual": None, "forecast": 16},
                    {"label": "W+3", "actual": None, "forecast": 14},
                ],
            }},
            {"type": "metric_cards", "data": [
                {"label": "Predicted P1s", "value": 1, "color": "#4caf50", "trend": -50, "icon": "error", "sparkline": [4, 3, 3, 2, 2, 2, 1]},
                {"label": "Predicted P2s", "value": 14, "color": "#ff9800", "trend": 8, "icon": "warning", "sparkline": [10, 11, 12, 12, 13, 13, 14]},
                {"label": "Confidence", "value": "78%", "color": "#60a5fa", "trend": None, "icon": "analytics"},
                {"label": "Risk Level", "value": "Medium", "color": "#ff9800", "trend": None, "icon": "shield"},
            ]},
            {"type": "recommendations", "data": [
                {"priority": "medium", "text": "Schedule change freeze for GWM platform during APAC peak hours", "impact": "Reduces deployment-related incident risk by 40%"},
                {"priority": "medium", "text": "Pre-scale database resources ahead of month-end processing", "impact": "Historical pattern shows 25% traffic increase at month-end"},
                {"priority": "low", "text": "Review and update runbooks for top 5 recurring incident types", "impact": "Supports continued MTTR improvement trend"},
            ]},
        ],
        "suggested_followups": [
            "What are the top recurring incident patterns?",
            "Show me the current incident analysis",
            "How are engineering teams performing?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_team_performance():
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": "Here's the engineering team performance breakdown for incident response. The Security team leads in response time, while the Collateral team has opportunities for improvement."},
            {"type": "table", "title": "Team Performance Metrics", "data": {
                "columns": ["Team", "MTTR", "MTTA", "Incidents (30d)", "Resolution Rate", "SLO Compliance"],
                "rows": [
                    ["Security", "1.2h", "2.1m", 18, "97%", "99.4%"],
                    ["Trading", "1.8h", "3.5m", 24, "95%", "99.98%"],
                    ["Data Platform", "2.1h", "3.8m", 15, "96%", "99.85%"],
                    ["Payments", "2.9h", "4.8m", 31, "92%", "99.1%"],
                    ["Collateral", "3.4h", "5.2m", 22, "88%", "98.2%"],
                    ["Client Experience", "2.3h", "4.1m", 12, "94%", "99.7%"],
                ],
            }},
            {"type": "bar_chart", "title": "MTTR by Team (hours)", "data": {
                "bars": [
                    {"name": "Security", "value": 1.2, "color": "#4caf50"},
                    {"name": "Trading", "value": 1.8, "color": "#4caf50"},
                    {"name": "Data", "value": 2.1, "color": "#60a5fa"},
                    {"name": "Client Exp", "value": 2.3, "color": "#60a5fa"},
                    {"name": "Payments", "value": 2.9, "color": "#ff9800"},
                    {"name": "Collateral", "value": 3.4, "color": "#f44336"},
                ],
                "xKey": "name",
                "yKey": "value",
                "unit": "h",
            }},
            {"type": "recommendations", "data": [
                {"priority": "high", "text": "Pair Collateral team with Security team for runbook best-practice sharing", "impact": "Target: reduce Collateral MTTR from 3.4h to 2.5h within 6 weeks"},
                {"priority": "medium", "text": "Implement automated incident classification for Payments team", "impact": "Reduces triage time, expected 20% MTTA improvement"},
                {"priority": "low", "text": "Recognize Security and Trading teams for top performance", "impact": "Reinforces best practices and team morale"},
            ]},
        ],
        "suggested_followups": [
            "What's driving the Collateral team's high MTTR?",
            "Give me the executive summary",
            "Show me the SLO compliance report",
        ],
        "timestamp": datetime.now().isoformat(),
    }


def _aura_default_response(message: str):
    return {
        "message_id": str(uuid.uuid4()),
        "content": [
            {"type": "text", "data": f"Thanks for your question. I'm AURA Assistant, your AI-powered observability companion. I can help you with a wide range of operational topics. Here are some things I'm great at:"},
            {"type": "text", "data": "• **Incident Analysis** — Real-time incident tracking, root cause, and impact assessment\n• **SLO Compliance** — Service level objectives, error budgets, and compliance reporting\n• **Blast Radius Analysis** — Dependency mapping and cascade failure prediction\n• **MTTR / MTTA Trends** — Mean time to resolve and acknowledge, team benchmarks\n• **Executive Summaries** — High-level platform health for leadership briefings\n• **Capacity Planning** — Resource utilization monitoring and scaling recommendations\n• **Deployment Status** — Recent and upcoming deployments with success metrics\n• **Alert Analysis** — Alert noise reduction and optimization insights\n• **Regional Comparison** — Cross-region health and performance benchmarking\n• **Trend Forecasting** — Predictive incident trends and risk assessment\n• **Team Performance** — Engineering team metrics and improvement areas"},
            {"type": "text", "data": "Try asking me something like \"What are the current incidents?\" or \"Give me an executive summary.\""},
        ],
        "suggested_followups": [
            "What are the current active incidents?",
            "Give me an executive summary",
            "Show me SLO compliance",
            "How are the engineering teams performing?",
        ],
        "timestamp": datetime.now().isoformat(),
    }


_AURA_SCENARIOS = [
    (["incident", "issues", "what's happening", "what is happening", "current status", "active p1", "active p2"], _aura_incident_analysis),
    (["slo", "compliance", "service level", "error budget"], _aura_slo_report),
    (["dependency", "blast", "cascade", "downstream", "upstream"], _aura_blast_radius),
    (["mttr", "mtta", "response time", "resolution time", "mean time"], _aura_mttr_analysis),
    (["executive", "summary", "overview", "leadership", "briefing"], _aura_executive_summary),
    (["capacity", "scaling", "resource", "utilization", "cpu", "memory"], _aura_capacity_planning),
    (["deployment", "deploy", "release", "rollout", "rollback"], _aura_deployment_status),
    (["alert", "noise", "false positive", "pager", "alarm"], _aura_alert_analysis),
    (["region", "comparison", "apac", "emea", "latam", "geographic"], _aura_regional_comparison),
    (["forecast", "prediction", "trend", "predict", "next week", "projected"], _aura_trend_forecast),
    (["team", "performance", "engineering", "productivity", "staff"], _aura_team_performance),
]
