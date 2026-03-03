from fastapi import APIRouter, HTTPException

from app.schemas import TeamCreate, TeamUpdate
from app.mock_data import TEAMS
from app.mock_data.teams_data import _next_team_id

router = APIRouter()


@router.get("/api/teams")
def get_teams():
    return TEAMS


@router.get("/api/teams/{team_id}")
def get_team(team_id: int):
    team = next((t for t in TEAMS if t["id"] == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/api/teams")
def create_team(payload: TeamCreate):
    import app.mock_data.teams_data as td
    new = {"id": td._next_team_id, "name": payload.name, "emails": payload.emails, "teams_channels": payload.teams_channels}
    td._next_team_id += 1
    TEAMS.append(new)
    return new


@router.put("/api/teams/{team_id}")
def update_team(team_id: int, payload: TeamUpdate):
    team = next((t for t in TEAMS if t["id"] == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    for field in ["name", "emails", "teams_channels"]:
        val = getattr(payload, field, None)
        if val is not None:
            team[field] = val
    return team


@router.delete("/api/teams/{team_id}")
def delete_team(team_id: int):
    before = len(TEAMS)
    to_remove = next((t for t in TEAMS if t["id"] == team_id), None)
    if not to_remove:
        raise HTTPException(status_code=404, detail="Team not found")
    TEAMS.remove(to_remove)
    return {"ok": True}
