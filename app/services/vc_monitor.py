import asyncio
import logging
from datetime import datetime

from app.services.email import send_email_async, _send_email_sync
from app.services.enrichment import (
    _filter_dashboard_apps,
    get_enriched_applications,
)

logger = logging.getLogger("uop-api")

# ── View Central Notifications ────────────────────────────────────────────────
# In-memory storage designed for future DB migration:
#   _vc_notifications  -> vc_notifications table (view_id as FK column)
#   _vc_alert_state    -> vc_alert_log table (notif_id, alert_type, app_seal, last_sent_at)

_vc_notifications: dict[str, list[dict]] = {}
_next_vc_notif_id = 1
_vc_alert_state: dict[str, str] = {}
VC_ALERT_COOLDOWN = 300   # seconds -- dedup window per alert
VC_CHECK_INTERVAL = 60    # seconds between background condition checks


def _build_vc_alert_email(notif_name, view_id, alerts, is_test=False):
    """Build HTML email body for VC notification alerts."""
    rows = ""
    for a in alerts:
        color = {"critical": "#f44336", "warning": "#ff9800", "slo": "#a855f7"}.get(a["alert_type"], "#60a5fa")
        rows += (
            f'<tr>'
            f'<td style="padding:8px;border-bottom:1px solid #eee">{a["app_name"]} ({a["app_seal"]})</td>'
            f'<td style="padding:8px;border-bottom:1px solid #eee">'
            f'<span style="color:{color};font-weight:600">{a["alert_type"].upper()}</span></td>'
            f'<td style="padding:8px;border-bottom:1px solid #eee">{a.get("detail", "")}</td>'
            f'</tr>'
        )
    test_banner = '<p style="color:#ff9800;font-weight:700">[TEST] This is a test notification</p>' if is_test else ""
    return (
        f'<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto">'
        f'{test_banner}'
        f'<h2 style="color:#1e293b">View Central Alert: {notif_name}</h2>'
        f'<p style="color:#64748b">The following conditions were detected for your monitored view:</p>'
        f'<table style="width:100%;border-collapse:collapse;margin:16px 0">'
        f'<thead><tr style="background:#f8fafc">'
        f'<th style="padding:8px;text-align:left;border-bottom:2px solid #e2e8f0">Application</th>'
        f'<th style="padding:8px;text-align:left;border-bottom:2px solid #e2e8f0">Alert</th>'
        f'<th style="padding:8px;text-align:left;border-bottom:2px solid #e2e8f0">Detail</th>'
        f'</tr></thead>'
        f'<tbody>{rows}</tbody></table>'
        f'<p style="color:#94a3b8;font-size:12px">View: {view_id} | Sent by Obs Dashboard</p>'
        f'</div>'
    )


def _evaluate_vc_conditions(notif):
    """Check enriched app data against notification alert types.
    Returns list of {app_name, app_seal, alert_type, detail}."""
    view_filters = notif.get("view_filters", {})
    filter_kwargs = {
        k: v for k, v in view_filters.items()
        if k in ("lob", "sub_lob", "cto", "cbt", "seal", "status", "search") and v
    }
    apps = _filter_dashboard_apps(**filter_kwargs)
    alert_types = set(notif.get("alert_types", []))
    triggered = []

    for app in apps:
        if "critical" in alert_types and app["status"] == "critical":
            triggered.append({
                "app_name": app["name"], "app_seal": app["seal"],
                "alert_type": "critical",
                "detail": f'{app["name"]} is in critical status',
            })
        if "warning" in alert_types and app["status"] == "warning":
            triggered.append({
                "app_name": app["name"], "app_seal": app["seal"],
                "alert_type": "warning",
                "detail": f'{app["name"]} is in warning status',
            })
        if "slo" in alert_types:
            enriched = get_enriched_applications()
            match = next((e for e in enriched if e["seal"] == app["seal"]), None)
            if match and match.get("slo", {}).get("status") in ("critical", "warning"):
                triggered.append({
                    "app_name": app["name"], "app_seal": app["seal"],
                    "alert_type": "slo",
                    "detail": f'{app["name"]} SLO is {match["slo"]["status"]} '
                              f'(current: {match["slo"].get("current", "N/A")}%)',
                })
    # "change" and "deployment" alert types require real event streams -- TODO
    return triggered


def _should_send_alert(notif_id, alert_type, app_seal):
    """Check cooldown to avoid duplicate alerts."""
    key = f"{notif_id}:{alert_type}:{app_seal}"
    last_sent = _vc_alert_state.get(key)
    if last_sent:
        elapsed = (datetime.utcnow() - datetime.fromisoformat(last_sent)).total_seconds()
        if elapsed < VC_ALERT_COOLDOWN:
            return False
    return True


def _mark_alert_sent(notif_id, alert_type, app_seal):
    """Record that an alert was sent."""
    key = f"{notif_id}:{alert_type}:{app_seal}"
    _vc_alert_state[key] = datetime.utcnow().isoformat()


async def _evaluate_all_notifications():
    """Iterate all enabled realtime notifications, evaluate conditions, send emails."""
    for view_id, notifs in _vc_notifications.items():
        for notif in notifs:
            if not notif.get("enabled") or notif.get("frequency") != "realtime":
                continue
            try:
                alerts = _evaluate_vc_conditions(notif)
                new_alerts = [
                    a for a in alerts
                    if _should_send_alert(notif["id"], a["alert_type"], a["app_seal"])
                ]
                if not new_alerts:
                    continue
                if notif["channels"].get("email") and notif["email_recipients"]:
                    subject = f'[Alert] {notif["name"]}: {len(new_alerts)} condition(s) detected'
                    html_body = _build_vc_alert_email(
                        notif_name=notif["name"], view_id=view_id, alerts=new_alerts,
                    )
                    await send_email_async(
                        notif["email_recipients"], subject, html_body,
                        f'Alert: {notif["name"]} - {len(new_alerts)} conditions detected',
                    )
                    for a in new_alerts:
                        _mark_alert_sent(notif["id"], a["alert_type"], a["app_seal"])
                    logger.info(
                        "VC alert sent: notif=%d view=%s alerts=%d recipients=%d",
                        notif["id"], view_id, len(new_alerts), len(notif["email_recipients"]),
                    )
            except Exception as exc:
                logger.error("VC notification eval error (notif=%d): %s", notif.get("id", -1), exc)


async def _vc_notification_loop():
    """Background loop that evaluates notification conditions and dispatches alerts."""
    logger.info("VC notification monitoring started (interval=%ds)", VC_CHECK_INTERVAL)
    while True:
        try:
            await asyncio.sleep(VC_CHECK_INTERVAL)
            await _evaluate_all_notifications()
        except asyncio.CancelledError:
            logger.info("VC notification monitoring stopped")
            break
        except Exception as exc:
            logger.error("VC notification loop error: %s", exc)


def start_vc_notification_loop():
    """Create the background task for VC notification monitoring.
    Call this from the FastAPI startup event."""
    asyncio.create_task(_vc_notification_loop())
