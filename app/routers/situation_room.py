from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas import SituationCreate, SituationUpdate, SystemOverrideUpdate
from app.services.enrichment import get_enriched_applications
from app.mock_data.situation_room_data import (
    SYSTEMS,
    SYSTEM_BY_ID,
    SITUATIONS,
    TIMELINE_OPTIONS,
    NEXT_UPDATE_OPTIONS,
    STATE_OPTIONS,
    PRIORITY_OPTIONS,
    compute_system_rows,
    build_situation_report,
    _get_all_components,
)

router = APIRouter()

_next_id_counter = [3]  # mutable counter


def _find_situation(situation_id: int) -> dict | None:
    return next((s for s in SITUATIONS if s["id"] == situation_id), None)


# ── Read Endpoints ───────────────────────────────────────────────────

@router.get("/api/situation-room/situations")
def list_situations():
    """List all situations (summary fields only)."""
    return [
        {
            "id": s["id"],
            "incident_number": s["incident_number"],
            "title": s["title"],
            "state": s["state"],
            "priority": s["priority"],
            "opened_time": s.get("opened_time", ""),
            "updated_at": s.get("updated_at", ""),
        }
        for s in SITUATIONS
    ]


@router.get("/api/situation-room/options")
def get_options():
    """Return all dropdown options for the Situation Room forms."""
    return {
        "timeline_options": TIMELINE_OPTIONS,
        "next_update_options": NEXT_UPDATE_OPTIONS,
        "state_options": STATE_OPTIONS,
        "priority_options": PRIORITY_OPTIONS,
    }


@router.get("/api/situation-room/systems")
def list_systems():
    """Return all system definitions."""
    return SYSTEMS


@router.get("/api/situation-room/systems/{system_id}/capabilities")
def get_system_capabilities(system_id: str):
    """Return all component labels for a system's apps."""
    system = SYSTEM_BY_ID.get(system_id)
    if not system:
        raise HTTPException(status_code=404, detail="System not found")
    enriched = get_enriched_applications()
    labels = _get_all_components(system["seals"], enriched)
    return {"system_id": system_id, "capabilities": labels}


@router.get("/api/situation-room/situations/{situation_id}")
def get_situation(situation_id: int):
    """Full situation detail with computed systems table."""
    situation = _find_situation(situation_id)
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")

    enriched = get_enriched_applications()
    systems = compute_system_rows(situation, enriched)

    return {
        **situation,
        "systems": systems,
    }


@router.get("/api/situation-room/situations/{situation_id}/report")
def get_situation_report(situation_id: int):
    """Per-incident deep-dive report data for export."""
    situation = _find_situation(situation_id)
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")

    enriched = get_enriched_applications()
    return build_situation_report(situation, enriched)


# ── Write Endpoints ──────────────────────────────────────────────────

@router.post("/api/situation-room/situations")
def create_situation(body: SituationCreate):
    """Create a new situation."""
    now = datetime.now(timezone.utc).isoformat()
    new_id = _next_id_counter[0]
    _next_id_counter[0] += 1

    situation = {
        "id": new_id,
        **body.model_dump(),
        "system_overrides": {},
        "created_at": now,
        "updated_at": now,
    }
    SITUATIONS.append(situation)
    return situation


@router.put("/api/situation-room/situations/{situation_id}")
def update_situation(situation_id: int, body: SituationUpdate):
    """Update situation fields (Save Situation button)."""
    situation = _find_situation(situation_id)
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")

    updates = body.model_dump(exclude_unset=True)
    situation.update(updates)
    situation["updated_at"] = datetime.now(timezone.utc).isoformat()
    return situation


@router.patch("/api/situation-room/situations/{situation_id}/systems/{system_id}")
def update_system_override(situation_id: int, system_id: str, body: SystemOverrideUpdate):
    """Update per-system overrides (inline table editing)."""
    situation = _find_situation(situation_id)
    if not situation:
        raise HTTPException(status_code=404, detail="Situation not found")
    if system_id not in SYSTEM_BY_ID:
        raise HTTPException(status_code=404, detail="System not found")

    overrides = situation.setdefault("system_overrides", {})
    sys_ovr = overrides.setdefault(system_id, {
        "timeline": "T0 - Detected",
        "impacted_capabilities": [],
        "sre_lead_overrides": [],
        "next_update": "Every 15 min",
    })
    updates = body.model_dump(exclude_unset=True)
    sys_ovr.update(updates)
    situation["updated_at"] = datetime.now(timezone.utc).isoformat()
    return sys_ovr


@router.delete("/api/situation-room/situations/{situation_id}")
def delete_situation(situation_id: int):
    """Delete a situation."""
    idx = next((i for i, s in enumerate(SITUATIONS) if s["id"] == situation_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Situation not found")
    SITUATIONS.pop(idx)
    return {"deleted": situation_id}
