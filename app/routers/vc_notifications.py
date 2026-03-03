from datetime import datetime

from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.schemas import VCNotificationCreate, VCNotificationUpdate
from app.services.email import _send_email_sync
from app.services.vc_monitor import (
    _vc_notifications,
    _vc_alert_state,
    _build_vc_alert_email,
)
import app.services.vc_monitor as vc_mod

router = APIRouter()


@router.get("/api/vc-notifications/{view_id}")
def get_vc_notifications(view_id: str):
    return _vc_notifications.get(view_id, [])


@router.post("/api/vc-notifications/{view_id}")
def create_vc_notification(view_id: str, payload: VCNotificationCreate):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    notif = {
        "id": vc_mod._next_vc_notif_id,
        "view_id": view_id,
        "name": payload.name,
        "alert_types": payload.alert_types,
        "channels": payload.channels,
        "teams_channels": payload.teams_channels,
        "email_recipients": payload.email_recipients,
        "frequency": payload.frequency,
        "days_of_week": payload.days_of_week,
        "start_time": payload.start_time,
        "end_time": payload.end_time,
        "enabled": payload.enabled,
        "view_filters": payload.view_filters,
        "created_at": now,
        "updated_at": now,
    }
    vc_mod._next_vc_notif_id += 1
    _vc_notifications.setdefault(view_id, []).append(notif)
    return notif


@router.put("/api/vc-notifications/{view_id}/{notif_id}")
def update_vc_notification(view_id: str, notif_id: int, payload: VCNotificationUpdate):
    notifs = _vc_notifications.get(view_id, [])
    notif = next((n for n in notifs if n["id"] == notif_id), None)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    for field in [
        "name", "alert_types", "channels", "teams_channels",
        "email_recipients", "frequency", "days_of_week",
        "start_time", "end_time", "enabled", "view_filters",
    ]:
        val = getattr(payload, field, None)
        if val is not None:
            notif[field] = val
    notif["updated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return notif


@router.patch("/api/vc-notifications/{view_id}/{notif_id}/toggle")
def toggle_vc_notification(view_id: str, notif_id: int):
    notifs = _vc_notifications.get(view_id, [])
    notif = next((n for n in notifs if n["id"] == notif_id), None)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    notif["enabled"] = not notif["enabled"]
    notif["updated_at"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return notif


@router.delete("/api/vc-notifications/{view_id}/{notif_id}")
def delete_vc_notification(view_id: str, notif_id: int):
    notifs = _vc_notifications.get(view_id, [])
    before = len(notifs)
    _vc_notifications[view_id] = [n for n in notifs if n["id"] != notif_id]
    if len(_vc_notifications[view_id]) == before:
        raise HTTPException(status_code=404, detail="Notification not found")
    for k in [k for k in _vc_alert_state if k.startswith(f"{notif_id}:")]:
        del _vc_alert_state[k]
    return {"ok": True}


@router.post("/api/vc-notifications/{view_id}/{notif_id}/test")
async def test_vc_notification(view_id: str, notif_id: int, background_tasks: BackgroundTasks):
    notifs = _vc_notifications.get(view_id, [])
    notif = next((n for n in notifs if n["id"] == notif_id), None)
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    if not notif["channels"].get("email") or not notif["email_recipients"]:
        raise HTTPException(status_code=400, detail="No email recipients configured")
    subject = f"[Test] View Central Alert: {notif['name']}"
    html_body = _build_vc_alert_email(
        notif_name=notif["name"],
        view_id=view_id,
        alerts=[{"app_name": "Test App", "app_seal": "00000", "alert_type": "critical", "detail": "This is a test alert"}],
        is_test=True,
    )
    background_tasks.add_task(
        _send_email_sync, notif["email_recipients"], subject, html_body,
        f"Test alert for notification: {notif['name']}",
    )
    return {"ok": True, "detail": f"Test email queued to {len(notif['email_recipients'])} recipients"}
