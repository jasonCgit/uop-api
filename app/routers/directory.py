from fastapi import APIRouter, Query

from app.mock_data.directory_data import DIRECTORY

router = APIRouter()


@router.get("/api/directory/search")
def search_directory(q: str = Query("", min_length=1)):
    """Search mock corporate directory by name, SID, or email."""
    query = q.lower()
    results = [
        p for p in DIRECTORY
        if query in p["firstName"].lower()
        or query in p["lastName"].lower()
        or query in p["sid"].lower()
        or query in p["email"].lower()
        or query in f'{p["firstName"]} {p["lastName"]}'.lower()
    ]
    return results[:20]
