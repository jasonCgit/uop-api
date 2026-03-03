from fastapi import APIRouter, HTTPException

from app.schemas import TeamCreate, TeamUpdate, RoleCreate, RoleRename
from app.mock_data import TEAMS
from app.mock_data.teams_data import _next_team_id, MEMBER_ROLES

router = APIRouter()


@router.get("/api/teams")
def get_teams():
    return TEAMS


@router.get("/api/teams/roles")
def get_roles():
    return MEMBER_ROLES


@router.post("/api/teams/roles")
def create_role(payload: RoleCreate):
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Role name cannot be empty")
    if name in MEMBER_ROLES:
        raise HTTPException(status_code=409, detail="Role already exists")
    MEMBER_ROLES.append(name)
    return {"ok": True, "roles": MEMBER_ROLES}


@router.put("/api/teams/roles/{role_name}")
def rename_role(role_name: str, payload: RoleRename):
    if role_name not in MEMBER_ROLES:
        raise HTTPException(status_code=404, detail="Role not found")
    new_name = payload.name.strip()
    if not new_name:
        raise HTTPException(status_code=400, detail="Role name cannot be empty")
    if new_name != role_name and new_name in MEMBER_ROLES:
        raise HTTPException(status_code=409, detail="Role name already exists")
    # Update the role list
    idx = MEMBER_ROLES.index(role_name)
    MEMBER_ROLES[idx] = new_name
    # Update all team members that have this role
    for team in TEAMS:
        for member in team.get("members", []):
            if member["role"] == role_name:
                member["role"] = new_name
    return {"ok": True, "roles": MEMBER_ROLES}


@router.delete("/api/teams/roles/{role_name}")
def delete_role(role_name: str):
    if role_name not in MEMBER_ROLES:
        raise HTTPException(status_code=404, detail="Role not found")
    # Check if any team members have this role
    in_use = sum(
        1 for team in TEAMS
        for member in team.get("members", [])
        if member["role"] == role_name
    )
    if in_use > 0:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete role '{role_name}': {in_use} member(s) currently assigned",
        )
    MEMBER_ROLES.remove(role_name)
    return {"ok": True, "roles": MEMBER_ROLES}


@router.get("/api/teams/{team_id}")
def get_team(team_id: int):
    team = next((t for t in TEAMS if t["id"] == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.get("/api/teams/{team_id}/members")
def get_team_members(team_id: int, role: str = None):
    team = next((t for t in TEAMS if t["id"] == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    members = team.get("members", [])
    if role:
        members = [m for m in members if m["role"] == role]
    return members


@router.post("/api/teams")
def create_team(payload: TeamCreate):
    import app.mock_data.teams_data as td
    new = {
        "id": td._next_team_id,
        "name": payload.name,
        "emails": payload.emails,
        "teams_channels": payload.teams_channels,
        "members": [m.dict() for m in payload.members],
    }
    td._next_team_id += 1
    TEAMS.append(new)
    return new


@router.put("/api/teams/{team_id}")
def update_team(team_id: int, payload: TeamUpdate):
    team = next((t for t in TEAMS if t["id"] == team_id), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    for field in ["name", "emails", "teams_channels", "members"]:
        val = getattr(payload, field, None)
        if val is not None:
            if field == "members":
                team[field] = [m.dict() for m in val]
            else:
                team[field] = val
    return team


@router.delete("/api/teams/{team_id}")
def delete_team(team_id: int):
    to_remove = next((t for t in TEAMS if t["id"] == team_id), None)
    if not to_remove:
        raise HTTPException(status_code=404, detail="Team not found")
    TEAMS.remove(to_remove)
    return {"ok": True}
