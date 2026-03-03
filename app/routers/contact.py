from fastapi import APIRouter

from app.schemas import ContactSendRequest
from app.services.email import send_email_async

router = APIRouter()


@router.post("/api/contact/send")
async def send_contact_message(payload: ContactSendRequest):
    result = {
        "status": "sent",
        "channels_sent": [],
        "message_preview": payload.message[:100] if payload.message else "",
    }

    if payload.channels.get("email") and payload.email_recipients:
        subject = payload.subject or (
            f"[{payload.app_name}] Contact Message" if payload.app_name
            else "Message from UOP Dashboard"
        )
        html_body = payload.email_body or f"<p>{payload.message}</p>"

        email_result = await send_email_async(
            recipients=payload.email_recipients,
            subject=subject,
            html_body=html_body,
            plain_body=payload.message,
        )
        result["channels_sent"].append("email")
        result["email_status"] = email_result

    return result
