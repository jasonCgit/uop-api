import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas import AnnouncementCreate, AnnouncementUpdate
from app.services.email import _send_email_sync
from app.mock_data import ANNOUNCEMENTS, WEAVE_INTERFACES
import app.mock_data.announcements_data as ann_data

logger = logging.getLogger("uop-api")

router = APIRouter()


@router.get("/api/announcements")
def get_announcements(status: Optional[str] = None, channel: Optional[str] = None, search: Optional[str] = None):
    results = ANNOUNCEMENTS
    if status:
        results = [a for a in results if a["ann_status"] == status]
    if channel:
        results = [a for a in results if a.get("channels", {}).get(channel, False)]
    if search:
        q = search.lower()
        results = [a for a in results if q in a["title"].lower() or q in a.get("description", "").lower() or q in a.get("author", "").lower()]
    return results


@router.get("/api/announcements/connect/weave-interfaces")
def get_weave_interfaces():
    return WEAVE_INTERFACES


@router.get("/api/announcements/connect/validate")
def validate_connect_selection(entities: str = "", regions: str = ""):
    entity_list = [e.strip() for e in entities.split(",") if e.strip()]
    region_list = [r.strip() for r in regions.split(",") if r.strip()]
    base_per_entity = {
        "CDG-PB": 420, "FRA-PB": 890, "JIB-PB": 310, "LON-PB": 1250,
        "MIL-PB": 380, "USA-PB": 3200, "USA-JPMS": 1800, "USA-CWM": 950, "BAH-ITS": 220,
    }
    total = sum(base_per_entity.get(e, 500) for e in entity_list) if entity_list else 0
    region_str = ", ".join(region_list) if region_list else "all"
    return {"message": f"Announcement will be sent to {total:,} {region_str} Connect users"}


@router.get("/api/announcements/notifications")
def get_notification_announcements():
    return [
        a for a in ANNOUNCEMENTS
        if a.get("channels", {}).get("banner", False) and a.get("ann_status") == "open"
    ]


@router.post("/api/announcements")
async def create_announcement(
    payload: AnnouncementCreate,
    background_tasks: BackgroundTasks,
):
    new = {
        "id": ann_data._next_announcement_id,
        "title": payload.title,
        "status": payload.status,
        "severity": payload.severity,
        "impacted_apps": payload.impacted_apps,
        "start_time": payload.start_time,
        "end_time": payload.end_time,
        "description": payload.description,
        "latest_updates": payload.latest_updates,
        "incident_number": payload.incident_number,
        "impact_type": payload.impact_type,
        "impact_description": payload.impact_description,
        "header_message": payload.header_message,
        "email_recipients": payload.email_recipients,
        "category": payload.category,
        "region": payload.region,
        "next_steps": payload.next_steps,
        "help_info": payload.help_info,
        "email_body": payload.email_body,
        "channels": payload.channels,
        "pinned": payload.pinned,
        "teams_channels": payload.teams_channels,
        "email_source": payload.email_source,
        "email_hide_status": payload.email_hide_status,
        "connect_dont_send_notification": payload.connect_dont_send_notification,
        "connect_banner_position": payload.connect_banner_position,
        "connect_target_entities": payload.connect_target_entities,
        "connect_target_regions": payload.connect_target_regions,
        "connect_weave_interfaces": payload.connect_weave_interfaces,
        "ann_status": "open",
        "author": "Current User",
        "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    }
    ann_data._next_announcement_id += 1
    ANNOUNCEMENTS.insert(0, new)

    if payload.channels.get("email") and payload.email_recipients:
        subject = f"[Announcement] {payload.title}"
        html_body = payload.email_body or f"<p>{payload.description}</p>"
        plain_body = payload.description or payload.title
        background_tasks.add_task(
            _send_email_sync,
            payload.email_recipients,
            subject,
            html_body,
            plain_body,
        )
        logger.info(
            "Queued announcement email (id=%d) to %d recipients",
            new["id"], len(payload.email_recipients),
        )

    return new


@router.put("/api/announcements/{announcement_id}")
def update_announcement(announcement_id: int, payload: AnnouncementUpdate):
    ann = next((a for a in ANNOUNCEMENTS if a["id"] == announcement_id), None)
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    for field in [
        "title", "status", "severity", "impacted_apps", "start_time", "end_time",
        "description", "latest_updates", "incident_number", "impact_type",
        "impact_description", "header_message", "email_recipients", "category",
        "region", "next_steps", "help_info", "email_body", "channels", "pinned",
        "teams_channels", "email_source", "email_hide_status",
        "connect_dont_send_notification", "connect_banner_position",
        "connect_target_entities", "connect_target_regions", "connect_weave_interfaces",
    ]:
        val = getattr(payload, field, None)
        if val is not None:
            ann[field] = val
    return ann


@router.patch("/api/announcements/{announcement_id}/status")
def toggle_announcement_status(announcement_id: int):
    ann = next((a for a in ANNOUNCEMENTS if a["id"] == announcement_id), None)
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    ann["ann_status"] = "closed" if ann["ann_status"] == "open" else "open"
    return ann


@router.delete("/api/announcements/{announcement_id}")
def delete_announcement(announcement_id: int):
    ann = next((a for a in ANNOUNCEMENTS if a["id"] == announcement_id), None)
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    ANNOUNCEMENTS.remove(ann)
    return {"ok": True}
