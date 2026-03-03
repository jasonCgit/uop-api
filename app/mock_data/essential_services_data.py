# REAL: Replace with ES API / database queries

"""
Deterministic mock data for the Essential Services page.

Each Essential Service maps to multiple applications at the deployment level.
RAG status is derived bottom-up from the mapped apps' enriched status.
Business processes link to multiple ES for impact analysis.
"""

import hashlib
from .apps_registry import APPS_REGISTRY

# ── Helpers ───────────────────────────────────────────────────────────────────

def _seed(es_id: str, salt: str = "") -> int:
    """Deterministic int seed from ES ID + salt."""
    return int(hashlib.md5(f"{es_id}{salt}".encode()).hexdigest()[:8], 16)


# ── Essential Service Definitions ─────────────────────────────────────────────

ESSENTIAL_SERVICES = [
    {"id": "3213",   "name": "Administer Sweep Functionality",                                                                        "criticality": "high",     "description": "Automated cash sweep management across client accounts, moving idle balances into yield-generating vehicles"},
    {"id": "3208",   "name": "Calculate and distribute Net Asset Values (NAVs) (AM)",                                                  "criticality": "critical", "description": "Daily NAV computation and distribution for asset management pooled funds, ensuring accurate pricing for investor transactions"},
    {"id": "3198",   "name": "Collateral management & monitoring (WM)",                                                               "criticality": "medium",   "description": "Wealth management collateral tracking, margin monitoring, and pledge management across client lending facilities"},
    {"id": "240292", "name": "Collateral management & monitoring (AM)",                                                               "criticality": "medium",   "description": "Asset management collateral valuation, substitution management, and regulatory compliance for derivatives and repo positions"},
    {"id": "3197",   "name": "Conduct Ongoing Due Diligence",                                                                         "criticality": "medium",   "description": "Continuous KYC/AML monitoring, periodic client reviews, and enhanced due diligence for high-risk relationships"},
    {"id": "3199",   "name": "Essential Client Requests & Actions",                                                                   "criticality": "high",     "description": "Processing time-sensitive client instructions including transfers, withdrawals, address changes, and account maintenance"},
    {"id": "3210",   "name": "Facilitate closing of committed mortgage loans",                                                        "criticality": "high",     "description": "End-to-end mortgage loan closing workflow from commitment through funding, document preparation, and settlement"},
    {"id": "3211",   "name": "Facilitate Purchase & Sell Orders in Brokerage",                                                        "criticality": "critical", "description": "Real-time order routing, execution, and settlement for brokerage buy/sell transactions across equity and fixed income markets"},
    {"id": "3212",   "name": "Liquidate and distribute assets in investment portfolios and deposit accounts",                          "criticality": "critical", "description": "Systematic liquidation of investment holdings and controlled distribution of proceeds from portfolios and deposit accounts"},
    {"id": "3209",   "name": "Maintain shareholder account information and facilitate shareholder transactions in pooled funds (AM)",   "criticality": "high",     "description": "Asset management transfer agency functions including shareholder recordkeeping, purchase/redemption processing, and dividend distribution"},
    {"id": "3196",   "name": "Maintain shareholder account information and facilitate shareholder transactions in pooled funds (WM)",   "criticality": "medium",   "description": "Wealth management transfer agency services for mutual fund shareholder accounts, transaction processing, and statement generation"},
    {"id": "3202",   "name": "Manage US Money Market Mutual Funds",                                                                   "criticality": "critical", "description": "NAV-stable money market fund operations including daily yield computation, portfolio compliance, and SEC regulatory reporting"},
    {"id": "3214",   "name": "Provide Access to Funds from Existing Credit Facilities",                                               "criticality": "critical", "description": "Loan draw-down processing, credit line access, and disbursement management for committed lending facilities"},
    {"id": "3203",   "name": "Provide portfolio/discretionary investment management (AM)",                                             "criticality": "high",     "description": "Asset management discretionary portfolio construction, rebalancing, model management, and performance attribution"},
    {"id": "3204",   "name": "Provide portfolio/discretionary investment management (WM)",                                             "criticality": "high",     "description": "Wealth management advisory and discretionary portfolio management, client investment policy execution, and reporting"},
]

ES_BY_ID = {es["id"]: es for es in ESSENTIAL_SERVICES}

# ── ES → Application SEAL Mappings ───────────────────────────────────────────
# Each ES maps to specific apps by SEAL. In production this comes from a mapping API.
# We hand-curate realistic mappings based on app function, supplemented with
# deterministic random picks so every ES has 3-8 apps.

_ALL_SEALS = [a["seal"] for a in APPS_REGISTRY]

# Curated primary mappings (realistic functional relationships)
_CURATED_MAPPINGS = {
    "3213":   ["90556", "86525", "16649", "85928", "110787"],        # Sweep Functionality → Spectrum UI, Research Desktop, Morgan Money, Payment Connect, IPB Payments
    "3208":   ["83756", "85589", "90645", "90215", "103290"],        # NAV Calculation (AM) → Global Funds, JEDI, Spectrum PM Multi-Asset, Spectrum PM Equities, Charles River
    "3198":   ["31572", "31894", "23419", "90083", "34387"],         # Collateral (WM) → TPR Netting, Collateral Mgmt, CMA, Collateral Mgmt, PB Loan
    "240292": ["31572", "31894", "23419", "85589", "103290"],        # Collateral (AM) → TPR Netting, Collateral Mgmt, CMA, JEDI, Charles River
    "3197":   ["89614", "102987", "85003", "63100", "16367"],        # Due Diligence → OneSentinel, Entitlements, PAM, CIB Digital Onboarding, Ops Party
    "3199":   ["88180", "90176", "89749", "25705", "85003"],         # Client Requests → Connect OS, Advisor Connect, Service Connect, Info Hub, PAM
    "3210":   ["34387", "110787", "85928", "62100", "18506"],        # Mortgage Closing → PB Loan, IPB Payments, Payment Connect, RT Payments, IBM Content Mgr
    "3211":   ["35206", "87082", "81884", "60100", "84412"],         # Brokerage Orders → Spectrum Trading, Center Trading, Order Decision Engine, Trade Engine, DNV Trading
    "3212":   ["90645", "90215", "35206", "79946", "17175"],         # Liquidate & Distribute → Spectrum PM Multi-Asset, Spectrum PM Equities, Spectrum Trading, Salerio, OMNITRUST
    "3209":   ["83756", "80453", "16649", "85589", "33528"],         # Shareholder Accts (AM) → Global Funds, ROME, Morgan Money, JEDI, CD:Lite
    "3196":   ["83756", "80453", "16649", "25705", "33528"],         # Shareholder Accts (WM) → Global Funds, ROME, Morgan Money, Info Hub, CD:Lite
    "3202":   ["106195", "16649", "83756", "85589", "103290"],       # Money Market Funds → Money Markets, Morgan Money, Global Funds, JEDI, Charles River
    "3214":   ["34387", "62100", "62215", "84065", "110787"],        # Credit Facilities → PB Loan, RT Payments, Cross-Border, SWIFT Middleware, IPB Payments
    "3203":   ["90645", "90215", "34210", "103290", "85589"],        # Portfolio Mgmt (AM) → Spectrum PM Multi-Asset, Spectrum PM Equities, PRISM-IM, Charles River, JEDI
    "3204":   ["90645", "90215", "34210", "90556", "86525"],         # Portfolio Mgmt (WM) → Spectrum PM Multi-Asset, Spectrum PM Equities, PRISM-IM, Spectrum UI, Research Desktop
}

def _get_es_seal_mappings(es_id: str) -> list[str]:
    """Return list of SEALs mapped to the given ES, combining curated + deterministic extras."""
    curated = _CURATED_MAPPINGS.get(es_id, [])
    # Add 1-3 extra deterministic apps to diversify
    seed = _seed(es_id, "extra_apps")
    extra_count = 1 + (seed % 3)
    extra = []
    for i in range(extra_count):
        idx = _seed(es_id, f"extra_{i}") % len(_ALL_SEALS)
        s = _ALL_SEALS[idx]
        if s not in curated and s not in extra:
            extra.append(s)
    return curated + extra

# Pre-compute all mappings
ES_APP_MAPPINGS: dict[str, list[str]] = {
    es["id"]: _get_es_seal_mappings(es["id"]) for es in ESSENTIAL_SERVICES
}


# ── Business Process Definitions ─────────────────────────────────────────────

BUSINESS_PROCESSES = [
    {
        "id": "bp1",
        "name": "NAV Calculation & Distribution",
        "description": "Daily computation and distribution of Net Asset Values for pooled funds",
        "services": ["3208", "3209", "3202"],
        "steps": ["Price Collection", "NAV Compute", "Validation", "Distribution", "Reconciliation"],
    },
    {
        "id": "bp2",
        "name": "Client Due Diligence & Onboarding",
        "description": "KYC/AML verification, ongoing due diligence, and client account activation",
        "services": ["3197", "3199", "3198"],
        "steps": ["Application", "KYC/AML Check", "Due Diligence", "Account Setup", "Activation"],
    },
    {
        "id": "bp3",
        "name": "Brokerage Trade Lifecycle",
        "description": "End-to-end brokerage order flow from entry through settlement and sweep",
        "services": ["3211", "3212", "3213"],
        "steps": ["Order Entry", "Execution", "Allocation", "Settlement", "Cash Sweep"],
    },
    {
        "id": "bp4",
        "name": "Mortgage Loan Closing",
        "description": "Committed mortgage loan closing from document preparation through funding",
        "services": ["3210", "3214", "3198"],
        "steps": ["Doc Prep", "Compliance Review", "Closing", "Funding", "Recording"],
    },
    {
        "id": "bp5",
        "name": "Portfolio Management (AM)",
        "description": "Asset management discretionary portfolio construction, rebalancing, and NAV impact",
        "services": ["3203", "3208", "240292"],
        "steps": ["Model Review", "Drift Analysis", "Rebalance", "Execution", "NAV Impact"],
    },
    {
        "id": "bp6",
        "name": "Portfolio Management (WM)",
        "description": "Wealth management advisory portfolio management and client reporting",
        "services": ["3204", "3196", "3198"],
        "steps": ["Client Review", "Proposal", "Approval", "Execution", "Reporting"],
    },
    {
        "id": "bp7",
        "name": "Credit Facility Drawdown",
        "description": "Processing loan draw-downs and disbursements from committed credit facilities",
        "services": ["3214", "3198", "240292"],
        "steps": ["Draw Request", "Collateral Check", "Approval", "Disbursement", "Confirmation"],
    },
    {
        "id": "bp8",
        "name": "Shareholder Transaction Processing",
        "description": "Purchase, redemption, and distribution processing for pooled fund shareholders",
        "services": ["3209", "3196", "3202", "3213"],
        "steps": ["Order Receipt", "Validation", "NAV Apply", "Settlement", "Sweep"],
    },
    {
        "id": "bp9",
        "name": "Asset Liquidation & Distribution",
        "description": "Systematic liquidation of holdings and controlled distribution of proceeds",
        "services": ["3212", "3211", "3213", "3208"],
        "steps": ["Liquidation Plan", "Order Generation", "Execution", "Proceeds Calc", "Distribution"],
    },
    {
        "id": "bp10",
        "name": "Collateral Management Lifecycle",
        "description": "End-to-end collateral valuation, substitution, and compliance monitoring",
        "services": ["3198", "240292", "3197"],
        "steps": ["Valuation", "Margin Call", "Substitution", "Monitoring", "Reporting"],
    },
    {
        "id": "bp11",
        "name": "Fund Administration",
        "description": "Money market and pooled fund daily operations including yield, compliance, and reporting",
        "services": ["3202", "3208", "3209", "3197"],
        "steps": ["Yield Compute", "Compliance Check", "NAV Strike", "Shareholder Update", "Regulatory File"],
    },
    {
        "id": "bp12",
        "name": "Client Service Fulfillment",
        "description": "Processing essential client requests across sweep, credit, and portfolio services",
        "services": ["3199", "3213", "3214", "3204"],
        "steps": ["Request Intake", "Validation", "Processing", "Confirmation", "Follow-Up"],
    },
]

BP_BY_ID = {bp["id"]: bp for bp in BUSINESS_PROCESSES}


# ── Status & Aggregation Functions ───────────────────────────────────────────

_STATUS_RANK = {"critical": 0, "warning": 1, "healthy": 2, "no_data": 3}
_RANK_STATUS = {0: "critical", 1: "warning", 2: "healthy", 3: "no_data"}


def _worst_status(statuses: list[str]) -> str:
    """Return the worst status from a list."""
    if not statuses:
        return "no_data"
    worst = min(_STATUS_RANK.get(s, 3) for s in statuses)
    return _RANK_STATUS[worst]


def _app_status_from_enriched(app: dict) -> str:
    """Extract status from an enriched app dict."""
    return app.get("status", "healthy")


# Pre-build SEAL -> raw registry lookup for deployment types
_RAW_BY_SEAL = {a["seal"]: a for a in APPS_REGISTRY}


def get_es_summary(enriched_apps: list[dict]) -> dict:
    """
    Compute summary for all 15 essential services.
    enriched_apps should be the result of _filter_dashboard_apps (already filtered).
    """
    app_by_seal = {a["seal"]: a for a in enriched_apps}

    services = []
    risk_matrix = {}
    kpis = {"total": len(ESSENTIAL_SERVICES), "healthy": 0, "degraded": 0, "down": 0}

    for es in ESSENTIAL_SERVICES:
        mapped_seals = ES_APP_MAPPINGS[es["id"]]
        mapped_apps = [app_by_seal[s] for s in mapped_seals if s in app_by_seal]

        # Deployment-level statuses
        app_statuses = [_app_status_from_enriched(a) for a in mapped_apps]
        es_status = _worst_status(app_statuses) if app_statuses else "no_data"

        # Map internal status names to RAG
        rag = "healthy" if es_status == "healthy" else "degraded" if es_status == "warning" else "down" if es_status == "critical" else "no_data"

        service_info = {
            "id": es["id"],
            "name": es["name"],
            "status": rag,
            "criticality": es["criticality"],
            "description": es["description"],
            "app_count": len(mapped_apps),
            "total_mapped": len(mapped_seals),
            "deployment_count": sum(len(_RAW_BY_SEAL.get(a["seal"], {}).get("deploymentTypes", [])) for a in mapped_apps),
        }
        services.append(service_info)

        # KPI counts
        if rag == "healthy":
            kpis["healthy"] += 1
        elif rag == "degraded":
            kpis["degraded"] += 1
        elif rag == "down":
            kpis["down"] += 1

        # Risk matrix: criticality x status
        cell_key = f"{es['criticality']}_{rag}"
        risk_matrix[cell_key] = risk_matrix.get(cell_key, 0) + 1

    return {
        "services": services,
        "kpis": kpis,
        "risk_matrix": risk_matrix,
    }


def get_es_detail(es_id: str, enriched_apps: list[dict]) -> dict | None:
    """
    Detail for a single essential service with mapped apps, CTO/CBT coverage.
    """
    es = ES_BY_ID.get(es_id)
    if not es:
        return None

    app_by_seal = {a["seal"]: a for a in enriched_apps}
    mapped_seals = ES_APP_MAPPINGS[es_id]

    mapped_apps = []
    cto_map = {}
    cbt_map = {}

    for seal in mapped_seals:
        app = app_by_seal.get(seal)
        if not app:
            continue

        app_status = _app_status_from_enriched(app)
        rag = "healthy" if app_status == "healthy" else "degraded" if app_status == "warning" else "down" if app_status == "critical" else "no_data"

        mapped_apps.append({
            "seal": app["seal"],
            "name": app["name"],
            "status": rag,
            "lob": app.get("lob", ""),
            "cto": app.get("cto", ""),
            "cbt": app.get("cbt", ""),
            "deploymentTypes": _RAW_BY_SEAL.get(seal, {}).get("deploymentTypes", []),
            "riskRanking": app.get("riskRanking", ""),
            "incidents_today": app.get("incidents_today", 0),
            "p1_30d": app.get("p1_30d", 0),
        })

        # CTO coverage
        cto = app.get("cto", "Unknown")
        if cto not in cto_map:
            cto_map[cto] = {"cto": cto, "apps": [], "statuses": []}
        cto_map[cto]["apps"].append(app["seal"])
        cto_map[cto]["statuses"].append(rag)

        # CBT coverage
        cbt = app.get("cbt", "Unknown")
        if cbt not in cbt_map:
            cbt_map[cbt] = {"cbt": cbt, "apps": [], "statuses": []}
        cbt_map[cbt]["apps"].append(app["seal"])
        cbt_map[cbt]["statuses"].append(rag)

    # Aggregate CTO/CBT coverage
    cto_coverage = [
        {"cto": v["cto"], "app_count": len(v["apps"]), "status": _worst_status(v["statuses"])}
        for v in cto_map.values()
    ]
    cbt_coverage = [
        {"cbt": v["cbt"], "app_count": len(v["apps"]), "status": _worst_status(v["statuses"])}
        for v in cbt_map.values()
    ]

    app_statuses = [a["status"] for a in mapped_apps]
    es_status = _worst_status(app_statuses) if app_statuses else "no_data"

    return {
        "service": {
            **es,
            "status": es_status,
            "app_count": len(mapped_apps),
            "total_mapped": len(mapped_seals),
        },
        "mapped_apps": mapped_apps,
        "cto_coverage": sorted(cto_coverage, key=lambda x: x["app_count"], reverse=True),
        "cbt_coverage": sorted(cbt_coverage, key=lambda x: x["app_count"], reverse=True),
    }


def get_business_processes(enriched_apps: list[dict]) -> list[dict]:
    """
    Return all business processes with derived status from their linked ES.
    """
    # First compute ES statuses
    summary = get_es_summary(enriched_apps)
    es_status_map = {s["id"]: s["status"] for s in summary["services"]}

    processes = []
    for bp in BUSINESS_PROCESSES:
        service_statuses = [es_status_map.get(sid, "no_data") for sid in bp["services"]]
        bp_status = _worst_status(service_statuses)

        linked_services = []
        for sid in bp["services"]:
            es = ES_BY_ID.get(sid)
            if es:
                linked_services.append({
                    "id": sid,
                    "name": es["name"],
                    "status": es_status_map.get(sid, "no_data"),
                })

        processes.append({
            "id": bp["id"],
            "name": bp["name"],
            "description": bp["description"],
            "status": bp_status,
            "steps": bp["steps"],
            "services": linked_services,
            "service_count": len(bp["services"]),
        })

    return processes


def get_impact_graph(es_id: str, enriched_apps: list[dict]) -> dict | None:
    """
    Build ReactFlow-compatible graph: ES → deployment types → apps.
    """
    es = ES_BY_ID.get(es_id)
    if not es:
        return None

    app_by_seal = {a["seal"]: a for a in enriched_apps}
    mapped_seals = ES_APP_MAPPINGS[es_id]

    nodes = []
    edges = []
    deploy_type_set = set()

    # ES node (center)
    app_statuses = []
    for seal in mapped_seals:
        app = app_by_seal.get(seal)
        if app:
            app_statuses.append(_app_status_from_enriched(app))
    es_status = _worst_status(app_statuses) if app_statuses else "no_data"
    es_rag = "healthy" if es_status == "healthy" else "degraded" if es_status == "warning" else "down"

    nodes.append({
        "id": f"es-{es_id}",
        "type": "service",
        "data": {"label": es["name"], "status": es_rag, "criticality": es["criticality"]},
    })

    # App nodes and deployment grouping
    for seal in mapped_seals:
        app = app_by_seal.get(seal)
        if not app:
            continue

        app_status = _app_status_from_enriched(app)
        app_rag = "healthy" if app_status == "healthy" else "degraded" if app_status == "warning" else "down"

        app_node_id = f"app-{seal}"
        nodes.append({
            "id": app_node_id,
            "type": "app",
            "data": {
                "label": app["name"],
                "seal": seal,
                "status": app_rag,
                "cto": app.get("cto", ""),
                "cbt": app.get("cbt", ""),
            },
        })

        raw_app = _RAW_BY_SEAL.get(seal, {})
        for dt in raw_app.get("deploymentTypes", []):
            dep_node_id = f"dep-{dt}"
            if dt not in deploy_type_set:
                deploy_type_set.add(dt)
                nodes.append({
                    "id": dep_node_id,
                    "type": "deployment",
                    "data": {"label": dt.upper(), "type": dt},
                })
                edges.append({"source": f"es-{es_id}", "target": dep_node_id})

            edges.append({"source": dep_node_id, "target": app_node_id})

    return {"nodes": nodes, "edges": edges}


def get_tree_mapping(enriched_apps: list[dict]) -> dict:
    """
    Map ES to both Business (LOB→SubLOB→ProductLine) and Technology (LOB→CTO→CBT) trees.
    """
    app_by_seal = {a["seal"]: a for a in enriched_apps}

    business_tree = {}
    technology_tree = {}

    for es in ESSENTIAL_SERVICES:
        mapped_seals = ES_APP_MAPPINGS[es["id"]]
        es_info = {"id": es["id"], "name": es["name"], "criticality": es["criticality"]}

        for seal in mapped_seals:
            app = app_by_seal.get(seal)
            if not app:
                continue

            lob = app.get("lob", "Unknown")
            sub_lob = app.get("subLob", "Unknown")
            product_line = app.get("productLine", "Unknown")
            cto = app.get("cto", "Unknown")
            cbt = app.get("cbt", "Unknown")

            # Business tree
            if lob not in business_tree:
                business_tree[lob] = {}
            if sub_lob not in business_tree[lob]:
                business_tree[lob][sub_lob] = {}
            if product_line not in business_tree[lob][sub_lob]:
                business_tree[lob][sub_lob][product_line] = []
            # Avoid duplicates
            if es["id"] not in [e["id"] for e in business_tree[lob][sub_lob][product_line]]:
                business_tree[lob][sub_lob][product_line].append(es_info)

            # Technology tree
            if lob not in technology_tree:
                technology_tree[lob] = {}
            if cto not in technology_tree[lob]:
                technology_tree[lob][cto] = {}
            if cbt not in technology_tree[lob][cto]:
                technology_tree[lob][cto][cbt] = []
            if es["id"] not in [e["id"] for e in technology_tree[lob][cto][cbt]]:
                technology_tree[lob][cto][cbt].append(es_info)

    return {
        "business_tree": business_tree,
        "technology_tree": technology_tree,
    }
