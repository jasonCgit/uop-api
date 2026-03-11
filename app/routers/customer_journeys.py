from fastapi import APIRouter, Query

from app.schemas import JourneyCreate, JourneyUpdate
from app.services.enrichment import _filter_dashboard_apps
from app.mock_data.customer_journeys_data import (
    get_journey_list,
    get_journey_detail,
    get_journey_health_dashboard,
    get_journey_analytics,
    get_analytics_summary,
    get_journey_risk_matrix,
    get_release_readiness,
    get_journey_blast_radius,
    get_journey_flow_graph,
    component_search,
    create_journey,
    update_journey,
    delete_journey,
    suggest_journey,
)

router = APIRouter()


# ── Standard filter params (reused across all endpoints) ──────────────────────

def _filters(
    lob: list[str] | None = Query(None),
    sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None),
    cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None),
    status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    return _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)


# ── GET endpoints ─────────────────────────────────────────────────────────────

@router.get("/api/customer-journeys/list")
def cj_list(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """All customer journeys with rolled-up health status and KPIs."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_journey_list(apps)


@router.get("/api/customer-journeys/health-dashboard")
def cj_health_dashboard(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Auto-generated health dashboard grouped by customer segment."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_journey_health_dashboard(apps)


@router.get("/api/customer-journeys/analytics/summary")
def cj_analytics_summary(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Cross-journey analytics summary with all proactive alerts."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_analytics_summary(apps)


@router.get("/api/customer-journeys/risk-matrix")
def cj_risk_matrix(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Risk matrix (criticality x health) with release readiness scores."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_journey_risk_matrix(apps)


@router.get("/api/customer-journeys/component-search")
def cj_component_search(
    q: str = Query("", min_length=2),
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Unified search across apps, deployments, and components."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return {"results": component_search(q, apps)}


# ── Parameterised GET endpoints (must come after static paths) ────────────────

@router.get("/api/customer-journeys/{journey_id}")
def cj_detail(
    journey_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Detail for a single journey with full step-level health."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_journey_detail(journey_id, apps)
    if result is None:
        return {"error": f"Journey {journey_id} not found"}
    return result


@router.get("/api/customer-journeys/{journey_id}/analytics")
def cj_analytics(
    journey_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """12-month trend analytics for a journey."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_journey_analytics(journey_id, apps)
    if result is None:
        return {"error": f"Journey {journey_id} not found"}
    return result


@router.get("/api/customer-journeys/{journey_id}/readiness")
def cj_readiness(
    journey_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Release readiness score for a journey."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_release_readiness(journey_id, apps)
    if result is None:
        return {"error": f"Journey {journey_id} not found"}
    return result


@router.get("/api/customer-journeys/{journey_id}/blast-radius")
def cj_blast_radius(
    journey_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Blast radius — other journeys impacted by shared apps/components."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_journey_blast_radius(journey_id, apps)
    if result is None:
        return {"error": f"Journey {journey_id} not found"}
    return result


@router.get("/api/customer-journeys/{journey_id}/flow-graph")
def cj_flow_graph(
    journey_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """ReactFlow-compatible nodes and edges for the journey map."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_journey_flow_graph(journey_id, apps)
    if result is None:
        return {"error": f"Journey {journey_id} not found"}
    return result


# ── Mutation endpoints ────────────────────────────────────────────────────────

@router.post("/api/customer-journeys")
def cj_create(body: JourneyCreate):
    """Create a new customer journey."""
    return create_journey(body.model_dump())


@router.put("/api/customer-journeys/{journey_id}")
def cj_update(journey_id: str, body: JourneyUpdate):
    """Update an existing customer journey."""
    result = update_journey(journey_id, body.model_dump(exclude_unset=True))
    if result is None:
        return {"error": f"Journey {journey_id} not found"}
    return result


@router.delete("/api/customer-journeys/{journey_id}")
def cj_delete(journey_id: str):
    """Delete a customer journey."""
    if delete_journey(journey_id):
        return {"ok": True}
    return {"error": f"Journey {journey_id} not found"}


@router.post("/api/customer-journeys/suggest")
def cj_suggest(body: dict = {}):
    """AURA-powered journey suggestion."""
    return suggest_journey(body)
