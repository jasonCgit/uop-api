from fastapi import APIRouter, Query

from app.services.enrichment import _filter_dashboard_apps
from app.mock_data.essential_services_data import (
    get_es_summary,
    get_es_detail,
    get_business_processes,
    get_impact_graph,
    get_tree_mapping,
)

router = APIRouter()


@router.get("/api/essential-services/summary")
def es_summary(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """All 15 ES with RAG status, app counts, risk matrix, and KPIs."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_es_summary(apps)


@router.get("/api/essential-services/business-processes")
def es_business_processes(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Business processes with their ES dependencies and derived status."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return {"processes": get_business_processes(apps)}


@router.get("/api/essential-services/tree-mapping")
def es_tree_mapping(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """ES mapped to Business and Technology trees."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_tree_mapping(apps)


@router.get("/api/essential-services/{service_id}")
def es_detail(
    service_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Detail for one ES — mapped apps, CTO/CBT coverage."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_es_detail(service_id, apps)
    if result is None:
        return {"error": f"Essential service {service_id} not found"}
    return result


@router.get("/api/essential-services/impact-graph/{service_id}")
def es_impact_graph(
    service_id: str,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """ReactFlow graph data: ES → deployments → apps."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    result = get_impact_graph(service_id, apps)
    if result is None:
        return {"error": f"Essential service {service_id} not found"}
    return result
