from fastapi import APIRouter

from app.schemas import AppTeamAssignment, IndicatorExclusion
from app.services.enrichment import (
    get_enriched_applications,
    APP_TEAM_ASSIGNMENTS,
    APP_EXCLUDED_INDICATORS,
    DEPLOYMENT_EXCLUDED_INDICATORS,
)
from app.mock_data import INDICATOR_TYPES

router = APIRouter()


@router.get("/api/applications/enriched")
def get_enriched():
    return get_enriched_applications()


@router.get("/api/indicator-types")
def get_indicator_types():
    return INDICATOR_TYPES


@router.get("/api/applications/{app_id}/teams")
def get_app_teams(app_id: str):
    return {"team_ids": APP_TEAM_ASSIGNMENTS.get(app_id, [])}


@router.put("/api/applications/{app_id}/teams")
def set_app_teams(app_id: str, payload: AppTeamAssignment):
    APP_TEAM_ASSIGNMENTS[app_id] = payload.team_ids
    return {"team_ids": payload.team_ids}


@router.put("/api/applications/{app_id}/excluded-indicators")
def set_app_excluded_indicators(app_id: str, payload: IndicatorExclusion):
    APP_EXCLUDED_INDICATORS[app_id] = payload.excluded_indicators
    return {"excluded_indicators": payload.excluded_indicators}


@router.put("/api/applications/{app_id}/deployments/{dep_id}/excluded-indicators")
def set_dep_excluded_indicators(app_id: str, dep_id: str, payload: IndicatorExclusion):
    key = f"{app_id}:{dep_id}"
    DEPLOYMENT_EXCLUDED_INDICATORS[key] = payload.excluded_indicators
    return {"excluded_indicators": payload.excluded_indicators}
