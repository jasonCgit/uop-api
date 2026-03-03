import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, LOG_LEVEL
from app.routers import (
    dashboard,
    applications,
    graph,
    teams,
    announcements,
    vc_notifications,
    contact,
    aura,
    directory,
)
from app.services.vc_monitor import start_vc_notification_loop

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger("uop-api")

app = FastAPI(title="UOP API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(dashboard.router)
app.include_router(applications.router)
app.include_router(graph.router)
app.include_router(teams.router)
app.include_router(announcements.router)
app.include_router(vc_notifications.router)
app.include_router(contact.router)
app.include_router(aura.router)
app.include_router(directory.router)


@app.on_event("startup")
async def startup():
    logger.info("UOP API starting up")
    start_vc_notification_loop()


@app.get("/")
def root():
    return {"service": "uop-api", "status": "running"}
