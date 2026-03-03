import asyncio
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor

from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM, SMTP_USE_TLS

logger = logging.getLogger("uop-api")

_smtp_configured = bool(SMTP_HOST)
if not _smtp_configured:
    logger.warning(
        "SMTP_HOST not set — email sending is disabled. "
        "Set SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM to enable."
    )

_email_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="smtp")


def _send_email_sync(
    recipients: list[str],
    subject: str,
    html_body: str,
    plain_body: str = "",
) -> dict:
    """Send an email via SMTP (blocking). Called from a thread pool."""
    if not _smtp_configured:
        logger.info("SMTP not configured — skipping email to %s", recipients)
        return {"status": "sent", "detail": "smtp_not_configured"}

    if not recipients:
        logger.warning("No recipients provided — skipping email")
        return {"status": "sent", "detail": "no_recipients"}

    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_FROM
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    if plain_body:
        msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            if SMTP_USE_TLS:
                server.ehlo()
                server.starttls()
                server.ehlo()
            if SMTP_USER:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, recipients, msg.as_string())

        logger.info("Email sent to %s (subject: %s)", recipients, subject)
        return {"status": "sent"}
    except smtplib.SMTPException as exc:
        logger.error("SMTP error sending to %s: %s", recipients, exc)
        return {"status": "error", "detail": str(exc)}
    except Exception as exc:
        logger.error("Unexpected error sending email to %s: %s", recipients, exc)
        return {"status": "error", "detail": str(exc)}


async def send_email_async(
    recipients: list[str],
    subject: str,
    html_body: str,
    plain_body: str = "",
) -> dict:
    """Non-blocking wrapper that runs _send_email_sync in a thread pool."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        _email_executor,
        _send_email_sync,
        recipients,
        subject,
        html_body,
        plain_body,
    )
