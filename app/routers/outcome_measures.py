from fastapi import APIRouter, Query

from app.services.enrichment import _filter_dashboard_apps
from app.mock_data.outcome_measures_data import (
    SECTIONS,
    MONTH_LABELS,
    WORKSTREAM_DEFS,
    aggregate_metrics,
    build_leaderboard,
    compute_executive_kpis,
    compute_executive_summary,
    get_all_seal_metrics,
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


@router.get("/api/outcome-measures/executive-summary")
def get_executive_summary(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Executive summary with top/bottom CTO-CBTs and workstream effectiveness."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    from app.mock_data import APPS_REGISTRY
    seal_set = {a["seal"] for a in apps}
    full_apps = [a for a in APPS_REGISTRY if a["seal"] in seal_set]
    return compute_executive_summary(full_apps)


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


@router.get("/api/outcome-measures/leaderboard")
def get_leaderboard(
    section_id: int = Query(1),
    sort_by: str | None = Query(None),
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """CTO/CBT leaderboard ranked by section metrics."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    section = next((s for s in SECTIONS if s["id"] == section_id), None)
    if not section:
        return {"error": "Section not found"}

    # Need full app records (with cto/cbt) for grouping
    from app.mock_data import APPS_REGISTRY
    seal_set = {a["seal"] for a in apps}
    full_apps = [a for a in APPS_REGISTRY if a["seal"] in seal_set]

    rows = build_leaderboard(full_apps, section["key"], sort_by)
    return {
        "section": section,
        "rows": rows,
        "month_labels": MONTH_LABELS,
    }


@router.get("/api/outcome-measures/coverage")
def get_coverage(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    """Coverage heatmap data grouped by CTO/CBT."""
    apps = _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    all_m = get_all_seal_metrics()

    from app.mock_data import APPS_REGISTRY
    seal_set = {a["seal"] for a in apps}
    full_apps = [a for a in APPS_REGISTRY if a["seal"] in seal_set]

    cov_keys = ["golden_signals", "slo_defined", "incident_zero", "blast_radius", "runbooks", "day1_complete"]
    cov_labels = {
        "golden_signals": "Golden Signals",
        "slo_defined": "SLO Defined",
        "incident_zero": "Incident Zero",
        "blast_radius": "Blast Radius",
        "runbooks": "Runbooks",
        "day1_complete": "Day 1 Complete",
    }

    # Group by CTO
    cto_map: dict[str, list[dict]] = {}
    for a in full_apps:
        cto_map.setdefault(a.get("cto", "Unknown"), []).append(a)

    heatmap = []
    for cto_name, cto_apps in sorted(cto_map.items()):
        seals = [a["seal"] for a in cto_apps]
        n = len(seals)
        cells = {}
        for ck in cov_keys:
            count = sum(1 for s in seals if s in all_m and all_m[s]["coverage"][ck])
            cells[ck] = {"covered": count, "total": n, "pct": round(count / n * 100, 1) if n else 0}
        overall = sum(cells[ck]["covered"] for ck in cov_keys)
        total_possible = n * len(cov_keys)
        heatmap.append({
            "cto": cto_name,
            "app_count": n,
            "cells": cells,
            "overall_pct": round(overall / total_possible * 100, 1) if total_possible else 0,
        })

    heatmap.sort(key=lambda r: r["overall_pct"], reverse=True)
    return {
        "coverage_keys": cov_keys,
        "coverage_labels": cov_labels,
        "heatmap": heatmap,
    }
