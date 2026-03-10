from fastapi import APIRouter, Query

from app.services.enrichment import _filter_dashboard_apps
from app.mock_data.outcome_measures_data import (
    SECTIONS,
    MONTH_LABELS,
    WORKSTREAM_DEFS,
    aggregate_metrics,
    compute_executive_kpis,
)

router = APIRouter()


def _seal_list(apps: list[dict]) -> list[str]:
    return [a["seal"] for a in apps]


@router.get("/api/outcome-measures/summary")
def get_outcome_summary(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Executive KPI bar + section list."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    seals = _seal_list(apps)
    return {
        "app_count": len(apps),
        "sections": SECTIONS,
        "executive_kpis": compute_executive_kpis(seals),
        "month_labels": MONTH_LABELS,
    }


@router.get("/api/outcome-measures/section/{section_id}")
def get_section_detail(
    section_id: int,
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Section-specific KPI cards + trend data."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    seals = _seal_list(apps)
    section = next((s for s in SECTIONS if s["id"] == section_id), None)
    if not section:
        return {"error": "Section not found"}
    section_key = section["key"]
    agg = aggregate_metrics(seals, section_key)
    return {
        "section": section,
        "app_count": len(apps),
        "month_labels": MONTH_LABELS,
        "metrics": agg.get(section_key, {}),
        "workstream_defs": WORKSTREAM_DEFS if section_key == "workstream_details" else None,
    }


