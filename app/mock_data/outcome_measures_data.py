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
    {"id": 1, "key": "adoption",           "label": "Adoption Details",         "short": "Adoption Details"},
    {"id": 2, "key": "sre_coverage",       "label": "SRE Coverage Details",     "short": "SRE Coverage"},
    {"id": 3, "key": "results",            "label": "Results Details",          "short": "Results Details"},
    {"id": 4, "key": "workstream_details", "label": "Details by Workstream",    "short": "By Workstream"},
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

    # ── Section 1: Adoption Details ──────────────────────────────────────────
    mcp_requests_baseline = 20 + (s % 80)
    mcp_requests_current = mcp_requests_baseline + int(mcp_requests_baseline * _pct(_seed(seal, "mcp"), 40, 200) / 100)
    uop_chat_baseline = 10 + (s % 40)
    uop_chat_current = uop_chat_baseline + int(uop_chat_baseline * _pct(_seed(seal, "uopc"), 30, 180) / 100)
    clicks_blast_baseline = 5 + (s % 20)
    clicks_blast_current = clicks_blast_baseline + int(clicks_blast_baseline * _pct(_seed(seal, "cbl"), 20, 150) / 100)
    clicks_cuj_baseline = 3 + (s % 15)
    clicks_cuj_current = clicks_cuj_baseline + int(clicks_cuj_baseline * _pct(_seed(seal, "ccuj"), 20, 150) / 100)
    clicks_slo_baseline = 4 + (s % 18)
    clicks_slo_current = clicks_slo_baseline + int(clicks_slo_baseline * _pct(_seed(seal, "cslo"), 20, 150) / 100)
    clicks_aura_baseline = 6 + (s % 25)
    clicks_aura_current = clicks_aura_baseline + int(clicks_aura_baseline * _pct(_seed(seal, "caura"), 25, 170) / 100)
    devgpt_exec_baseline = 8 + (s % 30)
    devgpt_exec_current = devgpt_exec_baseline + int(devgpt_exec_baseline * _pct(_seed(seal, "dgpt"), 30, 200) / 100)
    simulation_baseline = 3 + (s % 12)
    simulation_current = simulation_baseline + int(simulation_baseline * _pct(_seed(seal, "sim"), 20, 150) / 100)
    total_users_baseline = 15 + (s % 50)
    total_users_current = total_users_baseline + int(total_users_baseline * _pct(_seed(seal, "tuw"), 30, 160) / 100)

    # ── Section 2: SRE Coverage Details ──────────────────────────────────────
    sre_telemetry_cov_baseline = _pct(_seed(seal, "stcb"), 40, 75)
    sre_telemetry_cov_current = min(100.0, sre_telemetry_cov_baseline + _pct(_seed(seal, "stcc"), 5, 30))
    uop_coverage_baseline = _pct(_seed(seal, "ucb"), 30, 70)
    uop_coverage_current = min(100.0, uop_coverage_baseline + _pct(_seed(seal, "ucc"), 5, 35))
    dynatrace_cov_baseline = _pct(_seed(seal, "dtb"), 35, 72)
    dynatrace_cov_current = min(100.0, dynatrace_cov_baseline + _pct(_seed(seal, "dtc"), 5, 28))
    golden_signals_cov_baseline = _pct(_seed(seal, "gsb"), 30, 68)
    golden_signals_cov_current = min(100.0, golden_signals_cov_baseline + _pct(_seed(seal, "gsc"), 5, 32))

    # ── Section 3: Results Details ────────────────────────────────────────────
    incidents_avoided_baseline = 0
    incidents_avoided_current = 2 + (s % 15)
    p1_baseline = (s % 5)
    p1_current = max(0, p1_baseline - int(p1_baseline * _pct(_seed(seal, "p1r"), 10, 50) / 100))
    p2_baseline = (s % 8)
    p2_current = max(0, p2_baseline - int(p2_baseline * _pct(_seed(seal, "p2r"), 10, 45) / 100))
    p3_baseline = 2 + (s % 12)
    p3_current = max(0, p3_baseline - int(p3_baseline * _pct(_seed(seal, "p3r"), 5, 40) / 100))
    p4_baseline = 5 + (s % 20)
    p4_current = max(0, p4_baseline - int(p4_baseline * _pct(_seed(seal, "p4r"), 5, 35) / 100))
    p5_baseline = 8 + (s % 30)
    p5_current = max(0, p5_baseline - int(p5_baseline * _pct(_seed(seal, "p5r"), 5, 30) / 100))
    mttr_p1_baseline = 45 + (s % 90)
    mttr_p1_current = max(5, mttr_p1_baseline - int(mttr_p1_baseline * _pct(_seed(seal, "mp1"), 20, 65) / 100))
    mttr_p2_baseline = 25 + (s % 60)
    mttr_p2_current = max(5, mttr_p2_baseline - int(mttr_p2_baseline * _pct(_seed(seal, "mp2"), 15, 55) / 100))
    mttr_p3_baseline = 15 + (s % 40)
    mttr_p3_current = max(3, mttr_p3_baseline - int(mttr_p3_baseline * _pct(_seed(seal, "mp3"), 10, 45) / 100))
    true_impact_baseline = 45 + (s % 60)
    true_impact_current = max(5, true_impact_baseline - int(true_impact_baseline * _pct(_seed(seal, "tid"), 20, 70) / 100))
    cost_zt_baseline = 5000 + (s % 20000)
    cost_zt_current = cost_zt_baseline + int(cost_zt_baseline * _pct(_seed(seal, "czt"), 10, 60) / 100)
    cost_ts_baseline = 3000 + (s % 15000)
    cost_ts_current = cost_ts_baseline + int(cost_ts_baseline * _pct(_seed(seal, "cts"), 10, 55) / 100)
    anomaly_rate_baseline = _pct(_seed(seal, "arb"), 5, 20)
    anomaly_rate_current = max(0.5, anomaly_rate_baseline - _pct(_seed(seal, "arc"), 1, 10))
    change_aware_anomaly_baseline = _pct(_seed(seal, "carb"), 8, 25)
    change_aware_anomaly_current = max(0.5, change_aware_anomaly_baseline - _pct(_seed(seal, "carc"), 2, 12))
    incidents_avoided_uat_baseline = 0
    incidents_avoided_uat_current = 1 + (s % 8)
    incidents_avoided_prod_baseline = 0
    incidents_avoided_prod_current = 1 + (s % 7)
    alert_response_baseline = 8 + (s % 25)
    alert_response_current = max(2, alert_response_baseline - int(alert_response_baseline * _pct(_seed(seal, "art2"), 15, 55) / 100))
    response_type_baseline = 5 + (s % 20)
    response_type_current = response_type_baseline + int(response_type_baseline * _pct(_seed(seal, "rtb"), 20, 120) / 100)
    response_time_type_baseline = 12 + (s % 30)
    response_time_type_current = max(3, response_time_type_baseline - int(response_time_type_baseline * _pct(_seed(seal, "rtt"), 15, 50) / 100))
    pct_p1p2_alerts_baseline = _pct(_seed(seal, "pab"), 20, 55)
    pct_p1p2_alerts_current = min(100.0, pct_p1p2_alerts_baseline + _pct(_seed(seal, "pac"), 5, 30))
    actionable_alerts_baseline = 20 + (s % 80)
    actionable_alerts_current = max(5, actionable_alerts_baseline - int(actionable_alerts_baseline * _pct(_seed(seal, "aar"), 10, 50) / 100))
    noise_baseline = 50 + (s % 200)
    noise_current = noise_baseline + int(noise_baseline * _pct(_seed(seal, "noise"), -30, 80) / 100)
    suppression_baseline = _pct(_seed(seal, "supb"), 5, 30)
    suppression_current = suppression_baseline + _pct(_seed(seal, "supc"), 2, 20)

    # ── Section 4: Workstreams (unchanged) ───────────────────────────────────
    ws = {}
    for w in WORKSTREAM_DEFS:
        ws_seed = _seed(seal, w["id"])
        ws[w["id"]] = {
            "adopted": ws_seed % 2 == 0,
            "maturity": _pct(ws_seed, 10, 100),
            "value_score": _pct(_seed(seal, w["id"] + "v"), 20, 100),
        }

    return {
        "seal": seal,
        "adoption": {
            "mcp_requests":         {"baseline": mcp_requests_baseline,  "current": mcp_requests_current,  "trend": _trend_12m(_seed(seal, "mcpt"), mcp_requests_baseline,  mcp_requests_current),  "unit": "req/mo"},
            "uop_chat_prompts":     {"baseline": uop_chat_baseline,       "current": uop_chat_current,       "trend": _trend_12m(_seed(seal, "ucpt"), uop_chat_baseline,       uop_chat_current),       "unit": "prompts/mo"},
            "clicks_blast_radius":  {"baseline": clicks_blast_baseline,   "current": clicks_blast_current,   "trend": _trend_12m(_seed(seal, "cblt"), clicks_blast_baseline,   clicks_blast_current),   "unit": "clicks/mo"},
            "clicks_cuj":           {"baseline": clicks_cuj_baseline,     "current": clicks_cuj_current,     "trend": _trend_12m(_seed(seal, "ccujt"), clicks_cuj_baseline,    clicks_cuj_current),     "unit": "clicks/mo"},
            "clicks_slo_agent":     {"baseline": clicks_slo_baseline,     "current": clicks_slo_current,     "trend": _trend_12m(_seed(seal, "cslot"), clicks_slo_baseline,    clicks_slo_current),     "unit": "clicks/mo"},
            "clicks_aura":          {"baseline": clicks_aura_baseline,    "current": clicks_aura_current,    "trend": _trend_12m(_seed(seal, "caurat"), clicks_aura_baseline,  clicks_aura_current),    "unit": "clicks/mo"},
            "devgpt_executions":    {"baseline": devgpt_exec_baseline,    "current": devgpt_exec_current,    "trend": _trend_12m(_seed(seal, "dgptt"), devgpt_exec_baseline,   devgpt_exec_current),    "unit": "exec/mo"},
            "simulation_executions":{"baseline": simulation_baseline,     "current": simulation_current,     "trend": _trend_12m(_seed(seal, "simt"), simulation_baseline,     simulation_current),     "unit": "runs/mo"},
            "total_users_week":    {"baseline": total_users_baseline,    "current": total_users_current,    "trend": _trend_12m(_seed(seal, "tuwt"), total_users_baseline,    total_users_current),    "unit": "users/wk"},
        },
        "sre_coverage": {
            "sre_telemetry_coverage": {"baseline": sre_telemetry_cov_baseline, "current": sre_telemetry_cov_current, "trend": _trend_12m(_seed(seal, "stct"), sre_telemetry_cov_baseline, sre_telemetry_cov_current), "unit": "%", "lower_is_better": False},
            "uop_coverage":           {"baseline": uop_coverage_baseline,      "current": uop_coverage_current,      "trend": _trend_12m(_seed(seal, "uct"),  uop_coverage_baseline,      uop_coverage_current),      "unit": "%", "lower_is_better": False},
            "dynatrace_coverage":     {"baseline": dynatrace_cov_baseline,     "current": dynatrace_cov_current,     "trend": _trend_12m(_seed(seal, "dtt"),  dynatrace_cov_baseline,     dynatrace_cov_current),     "unit": "%", "lower_is_better": False},
            "golden_signals_coverage":{"baseline": golden_signals_cov_baseline,"current": golden_signals_cov_current,"trend": _trend_12m(_seed(seal, "gst"),  golden_signals_cov_baseline,golden_signals_cov_current),"unit": "%", "lower_is_better": False},
        },
        "results": {
            "incidents_avoided":       {"baseline": incidents_avoided_baseline, "current": incidents_avoided_current, "trend": _trend_12m(_seed(seal, "iat"), 0, incidents_avoided_current),              "unit": "count",    "lower_is_better": False},
            "incidents_avoided_uat":   {"baseline": incidents_avoided_uat_baseline,  "current": incidents_avoided_uat_current,  "trend": _trend_12m(_seed(seal, "iaut"), 0, incidents_avoided_uat_current),  "unit": "count", "lower_is_better": False},
            "incidents_avoided_prod":  {"baseline": incidents_avoided_prod_baseline, "current": incidents_avoided_prod_current, "trend": _trend_12m(_seed(seal, "iapt"), 0, incidents_avoided_prod_current), "unit": "count", "lower_is_better": False},
            "p1_incidents":            {"baseline": p1_baseline,                "current": p1_current,                "trend": _trend_12m(_seed(seal, "p1t"), p1_baseline, p1_current),                   "unit": "count",    "lower_is_better": True},
            "p2_incidents":            {"baseline": p2_baseline,                "current": p2_current,                "trend": _trend_12m(_seed(seal, "p2t"), p2_baseline, p2_current),                   "unit": "count",    "lower_is_better": True},
            "p3_incidents":            {"baseline": p3_baseline,                "current": p3_current,                "trend": _trend_12m(_seed(seal, "p3t"), p3_baseline, p3_current),                   "unit": "count",    "lower_is_better": True},
            "p4_incidents":            {"baseline": p4_baseline,                "current": p4_current,                "trend": _trend_12m(_seed(seal, "p4t"), p4_baseline, p4_current),                   "unit": "count",    "lower_is_better": True},
            "p5_incidents":            {"baseline": p5_baseline,                "current": p5_current,                "trend": _trend_12m(_seed(seal, "p5t"), p5_baseline, p5_current),                   "unit": "count",    "lower_is_better": True},
            "mttr_p1":                 {"baseline": mttr_p1_baseline,           "current": mttr_p1_current,           "trend": _trend_12m(_seed(seal, "mp1t"), mttr_p1_baseline, mttr_p1_current),        "unit": "min",      "lower_is_better": True},
            "mttr_p2":                 {"baseline": mttr_p2_baseline,           "current": mttr_p2_current,           "trend": _trend_12m(_seed(seal, "mp2t"), mttr_p2_baseline, mttr_p2_current),        "unit": "min",      "lower_is_better": True},
            "mttr_p3":                 {"baseline": mttr_p3_baseline,           "current": mttr_p3_current,           "trend": _trend_12m(_seed(seal, "mp3t"), mttr_p3_baseline, mttr_p3_current),        "unit": "min",      "lower_is_better": True},
            "ai_impact_duration":      {"baseline": true_impact_baseline,       "current": true_impact_current,       "trend": _trend_12m(_seed(seal, "ttr"), true_impact_baseline, true_impact_current),  "unit": "min",      "lower_is_better": True},
            "anomaly_rate":            {"baseline": anomaly_rate_baseline,       "current": anomaly_rate_current,      "trend": _trend_12m(_seed(seal, "art"), anomaly_rate_baseline, anomaly_rate_current), "unit": "/100 chg", "lower_is_better": True},
            "change_aware_anomaly_rate": {"baseline": change_aware_anomaly_baseline, "current": change_aware_anomaly_current, "trend": _trend_12m(_seed(seal, "cart"), change_aware_anomaly_baseline, change_aware_anomaly_current), "unit": "/100 chg", "lower_is_better": True},
            "alert_response_time":     {"baseline": alert_response_baseline,   "current": alert_response_current,   "trend": _trend_12m(_seed(seal, "art2t"), alert_response_baseline, alert_response_current), "unit": "min", "lower_is_better": True},
            "response_type_breakdown": {"baseline": response_type_baseline,    "current": response_type_current,    "trend": _trend_12m(_seed(seal, "rtbt"), response_type_baseline, response_type_current),   "unit": "count", "lower_is_better": False},
            "response_time_by_type":   {"baseline": response_time_type_baseline, "current": response_time_type_current, "trend": _trend_12m(_seed(seal, "rttt"), response_time_type_baseline, response_time_type_current), "unit": "min", "lower_is_better": True},
            "pct_p1p2_detected_by_alerts": {"baseline": pct_p1p2_alerts_baseline, "current": pct_p1p2_alerts_current, "trend": _trend_12m(_seed(seal, "pat"), pct_p1p2_alerts_baseline, pct_p1p2_alerts_current), "unit": "%", "lower_is_better": False},
            "actionable_alerts_reduction": {"baseline": actionable_alerts_baseline, "current": actionable_alerts_current, "trend": _trend_12m(_seed(seal, "aart"), actionable_alerts_baseline, actionable_alerts_current), "unit": "count", "lower_is_better": True},
            "cost_reduction_zero_touch":   {"baseline": cost_zt_baseline,       "current": cost_zt_current,           "trend": _trend_12m(_seed(seal, "cztt"), cost_zt_baseline, cost_zt_current),         "unit": "$",        "lower_is_better": False},
            "cost_reduction_techsupport":  {"baseline": cost_ts_baseline,       "current": cost_ts_current,           "trend": _trend_12m(_seed(seal, "ctst"), cost_ts_baseline, cost_ts_current),         "unit": "$",        "lower_is_better": False},
            "alert_noise_reduction":   {"baseline": noise_baseline,             "current": noise_current,             "trend": _trend_12m(_seed(seal, "ntr"), noise_baseline, noise_current),               "unit": "count",    "lower_is_better": True},
            "suppression_rate":        {"baseline": suppression_baseline,       "current": suppression_current,       "trend": _trend_12m(_seed(seal, "supt"), suppression_baseline, suppression_current),  "unit": "%",        "lower_is_better": False},
        },
        "workstream_details": ws,
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

    # Section 1: Adoption
    if section_key is None or section_key == "adoption":
        adoption_metric_keys = [
            ("total_users_week",       "sum",  False, "users/wk"),
            ("mcp_requests",          "sum",  False, "req/mo"),
            ("uop_chat_prompts",       "sum",  False, "prompts/mo"),
            ("clicks_blast_radius",    "sum",  False, "clicks/mo"),
            ("clicks_cuj",             "sum",  False, "clicks/mo"),
            ("clicks_slo_agent",       "sum",  False, "clicks/mo"),
            ("clicks_aura",            "sum",  False, "clicks/mo"),
            ("devgpt_executions",      "sum",  False, "exec/mo"),
            ("simulation_executions",  "sum",  False, "runs/mo"),
        ]
        result["adoption"] = {}
        for mk, agg_type, lib, unit in adoption_metric_keys:
            result["adoption"][mk] = _build_metric(
                [m["adoption"][mk]["baseline"] for m in metrics],
                [m["adoption"][mk]["current"]  for m in metrics],
                [m["adoption"][mk]["trend"]    for m in metrics],
                agg=agg_type, lower_is_better=lib, unit=unit)

    # Section 2: SRE Coverage
    if section_key is None or section_key == "sre_coverage":
        sre_cov_keys = [
            "sre_telemetry_coverage", "uop_coverage",
            "dynatrace_coverage", "golden_signals_coverage",
        ]
        result["sre_coverage"] = {}
        for mk in sre_cov_keys:
            result["sre_coverage"][mk] = _build_metric(
                [m["sre_coverage"][mk]["baseline"] for m in metrics],
                [m["sre_coverage"][mk]["current"]  for m in metrics],
                [m["sre_coverage"][mk]["trend"]    for m in metrics],
                agg="avg", lower_is_better=False,
                unit=metrics[0]["sre_coverage"][mk]["unit"])

    # Section 3: Results
    if section_key is None or section_key == "results":
        results_metric_defs = [
            ("incidents_avoided",          "sum",  False, "count"),
            ("incidents_avoided_uat",      "sum",  False, "count"),
            ("incidents_avoided_prod",     "sum",  False, "count"),
            ("p1_incidents",               "sum",  True,  "count"),
            ("p2_incidents",               "sum",  True,  "count"),
            ("p3_incidents",               "sum",  True,  "count"),
            ("p4_incidents",               "sum",  True,  "count"),
            ("p5_incidents",               "sum",  True,  "count"),
            ("mttr_p1",                    "avg",  True,  "min"),
            ("mttr_p2",                    "avg",  True,  "min"),
            ("mttr_p3",                    "avg",  True,  "min"),
            ("ai_impact_duration",         "avg",  True,  "min"),
            ("alert_response_time",        "avg",  True,  "min"),
            ("response_type_breakdown",    "sum",  False, "count"),
            ("response_time_by_type",      "avg",  True,  "min"),
            ("anomaly_rate",               "avg",  True,  "/100 chg"),
            ("change_aware_anomaly_rate",  "avg",  True,  "/100 chg"),
            ("pct_p1p2_detected_by_alerts","avg",  False, "%"),
            ("actionable_alerts_reduction","sum",  True,  "count"),
            ("cost_reduction_zero_touch",  "sum",  False, "$"),
            ("cost_reduction_techsupport", "sum",  False, "$"),
            ("alert_noise_reduction",      "sum",  True,  "count"),
            ("suppression_rate",           "avg",  False, "%"),
        ]
        result["results"] = {}
        for mk, agg_type, lib, unit in results_metric_defs:
            result["results"][mk] = _build_metric(
                [m["results"][mk]["baseline"] for m in metrics],
                [m["results"][mk]["current"]  for m in metrics],
                [m["results"][mk]["trend"]    for m in metrics],
                agg=agg_type, lower_is_better=lib, unit=unit)

    # Section 4: Workstream Details
    if section_key is None or section_key == "workstream_details":
        ws_agg = {}
        for w in WORKSTREAM_DEFS:
            adopted = sum(1 for m in metrics if m["workstream_details"][w["id"]]["adopted"])
            avg_maturity = _avg([m["workstream_details"][w["id"]]["maturity"] for m in metrics])
            avg_value = _avg([m["workstream_details"][w["id"]]["value_score"] for m in metrics])
            ws_agg[w["id"]] = {
                "label": w["label"], "icon": w["icon"],
                "adopted_count": adopted, "total_apps": n,
                "adoption_pct": round(adopted / n * 100, 1) if n else 0,
                "avg_maturity": avg_maturity, "avg_value_score": avg_value,
            }
        result["workstream_details"] = ws_agg

    return result


def build_leaderboard(apps: list[dict], section_key: str, sort_by: str | None = None) -> list[dict]:
    """Build a ranked CTO/CBT leaderboard for a given section (kept for future use)."""
    all_m = get_all_seal_metrics()

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

            if section_key == "workstream_details":
                ws_data = section_data
                avg_adoption = round(sum(w["adoption_pct"] for w in ws_data.values()) / len(ws_data), 1) if ws_data else 0
                avg_maturity = round(sum(w["avg_maturity"] for w in ws_data.values()) / len(ws_data), 1) if ws_data else 0
                rows.append({"cto": cto, "cbt": cbt, "app_count": len(seals), "avg_adoption": avg_adoption, "avg_maturity": avg_maturity, "metrics": section_data})
                continue

            if section_key == "adoption":
                primary_key = sort_by or "mcp_requests"
            elif section_key == "sre_coverage":
                primary_key = sort_by or "sre_telemetry_coverage"
            elif section_key == "results":
                primary_key = sort_by or "incidents_avoided"
            else:
                primary_key = sort_by or list(section_data.keys())[0] if section_data else "value"

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

    if section_key == "workstream_details":
        rows.sort(key=lambda r: r.get("avg_adoption", 0), reverse=True)
    else:
        lib = rows[0].get("lower_is_better", False) if rows else False
        rows.sort(key=lambda r: r.get("pct_change", 0), reverse=not lib)

    for i, r in enumerate(rows):
        r["rank"] = i + 1

    return rows


# ── Executive summary computation ─────────────────────────────────────────────

def compute_executive_summary(apps: list[dict]) -> dict:
    """Compute executive insights: workstream effectiveness."""
    seal_list = [a["seal"] for a in apps]
    ws_agg = aggregate_metrics(seal_list, "workstream_details").get("workstream_details", {})
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
        "workstream_insights": ws_insights,
    }


# ── Executive KPI computation ─────────────────────────────────────────────────

def compute_executive_kpis(seal_list: list[str]) -> list[dict]:
    """Return headline KPIs grouped into 3 buckets for the executive bar."""
    agg = aggregate_metrics(seal_list)
    kpis = []

    # ── ADOPTION bucket ──────────────────────────────────────────────────────
    dau = agg.get("adoption", {}).get("uop_chat_prompts", {})
    kpis.append({
        "label": "Total Users / Week", "section": "adoption", "bucket": "adoption",
        "current": dau.get("current", 0), "baseline": dau.get("baseline", 0),
        "pct_change": dau.get("pct_change", 0), "unit": "",
        "spark": dau.get("trend", [])[-7:], "lower_is_better": False,
    })

    prompts = agg.get("adoption", {}).get("mcp_requests", {})
    kpis.append({
        "label": "Total Prompts", "section": "adoption", "bucket": "adoption",
        "current": prompts.get("current", 0), "baseline": prompts.get("baseline", 0),
        "pct_change": prompts.get("pct_change", 0), "unit": "",
        "spark": prompts.get("trend", [])[-7:], "lower_is_better": False,
    })

    # ── SRE COVERAGE bucket ──────────────────────────────────────────────────
    dt_cov = agg.get("sre_coverage", {}).get("dynatrace_coverage", {})
    kpis.append({
        "label": "Dynatrace Coverage", "section": "sre_coverage", "bucket": "sre_coverage",
        "current": dt_cov.get("current", 0), "baseline": dt_cov.get("baseline", 0),
        "pct_change": dt_cov.get("pct_change", 0), "unit": "%",
        "spark": dt_cov.get("trend", [])[-7:], "lower_is_better": False,
    })

    gs_cov = agg.get("sre_coverage", {}).get("golden_signals_coverage", {})
    kpis.append({
        "label": "Golden Signals Coverage", "section": "sre_coverage", "bucket": "sre_coverage",
        "current": gs_cov.get("current", 0), "baseline": gs_cov.get("baseline", 0),
        "pct_change": gs_cov.get("pct_change", 0), "unit": "%",
        "spark": gs_cov.get("trend", [])[-7:], "lower_is_better": False,
    })

    # ── RESULTS bucket ───────────────────────────────────────────────────────
    anomaly = agg.get("results", {}).get("anomaly_rate", {})
    kpis.append({
        "label": "Anomalies / 100 Changes", "section": "results", "bucket": "results",
        "current": anomaly.get("current", 0), "baseline": anomaly.get("baseline", 0),
        "pct_change": anomaly.get("pct_change", 0), "unit": "",
        "spark": anomaly.get("trend", [])[-7:], "lower_is_better": True,
    })

    impact = agg.get("results", {}).get("ai_impact_duration", {})
    kpis.append({
        "label": "AI Impact Duration", "section": "results", "bucket": "results",
        "current": impact.get("current", 0), "baseline": impact.get("baseline", 0),
        "pct_change": impact.get("pct_change", 0), "unit": "min",
        "spark": impact.get("trend", [])[-7:], "lower_is_better": True,
    })

    p1_all = agg.get("results", {}).get("p1_incidents", {})
    kpis.append({
        "label": "Incident/Tickets Trending", "section": "results", "bucket": "results",
        "current": p1_all.get("current", 0), "baseline": p1_all.get("baseline", 0),
        "pct_change": p1_all.get("pct_change", 0), "unit": "",
        "spark": p1_all.get("trend", [])[-7:], "lower_is_better": True,
    })

    cost_zt = agg.get("results", {}).get("cost_reduction_zero_touch", {})
    cost_ts = agg.get("results", {}).get("cost_reduction_techsupport", {})
    total_cost = cost_zt.get("current", 0) + cost_ts.get("current", 0)
    total_baseline = cost_zt.get("baseline", 0) + cost_ts.get("baseline", 0)
    kpis.append({
        "label": "Total Cost Reduction", "section": "results", "bucket": "results",
        "current": total_cost, "baseline": total_baseline,
        "pct_change": _safe_pct_change(total_baseline, total_cost), "unit": "$",
        "spark": [], "lower_is_better": False,
    })

    return kpis
