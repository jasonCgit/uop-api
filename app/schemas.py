from pydantic import BaseModel
from typing import Optional, List


class AnnouncementCreate(BaseModel):
    title: str
    status: str = "ongoing"  # ongoing, resolved, closed
    severity: str = "none"  # none, standard, major
    impacted_apps: list[str] = []
    start_time: str = ""
    end_time: str = ""
    description: str = ""
    latest_updates: str = ""
    incident_number: str = ""
    impact_type: str = ""
    impact_description: str = ""
    header_message: str = ""
    email_recipients: list[str] = []
    category: str = ""
    region: str = ""
    next_steps: str = ""
    help_info: str = ""
    email_body: str = ""
    channels: dict = {"teams": False, "email": False, "connect": False, "banner": False}
    pinned: bool = False
    # Teams channel config
    teams_channels: list[str] = []
    # Email channel config
    email_source: str = ""
    email_hide_status: bool = False
    # Connect channel config
    connect_dont_send_notification: bool = False
    connect_banner_position: str = "in_ui"
    connect_target_entities: list[str] = []
    connect_target_regions: list[str] = []
    connect_weave_interfaces: list[int] = []


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    impacted_apps: Optional[list[str]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    description: Optional[str] = None
    latest_updates: Optional[str] = None
    incident_number: Optional[str] = None
    impact_type: Optional[str] = None
    impact_description: Optional[str] = None
    header_message: Optional[str] = None
    email_recipients: Optional[list[str]] = None
    category: Optional[str] = None
    region: Optional[str] = None
    next_steps: Optional[str] = None
    help_info: Optional[str] = None
    email_body: Optional[str] = None
    channels: Optional[dict] = None
    pinned: Optional[bool] = None
    teams_channels: Optional[list[str]] = None
    email_source: Optional[str] = None
    email_hide_status: Optional[bool] = None
    connect_dont_send_notification: Optional[bool] = None
    connect_banner_position: Optional[str] = None
    connect_target_entities: Optional[list[str]] = None
    connect_target_regions: Optional[list[str]] = None
    connect_weave_interfaces: Optional[list[int]] = None


class TeamCreate(BaseModel):
    name: str
    emails: list[str] = []
    teams_channels: list[str] = []


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    emails: Optional[list[str]] = None
    teams_channels: Optional[list[str]] = None


class VCNotificationCreate(BaseModel):
    name: str
    alert_types: list[str] = ["critical"]
    channels: dict = {"teams": False, "email": False}
    teams_channels: list[str] = []
    email_recipients: list[str] = []
    frequency: str = "realtime"
    days_of_week: list[str] = []
    start_time: str = "08:00"
    end_time: str = "18:00"
    enabled: bool = True
    view_filters: dict = {}


class VCNotificationUpdate(BaseModel):
    name: Optional[str] = None
    alert_types: Optional[list[str]] = None
    channels: Optional[dict] = None
    teams_channels: Optional[list[str]] = None
    email_recipients: Optional[list[str]] = None
    frequency: Optional[str] = None
    days_of_week: Optional[list[str]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    enabled: Optional[bool] = None
    view_filters: Optional[dict] = None


class ContactSendRequest(BaseModel):
    channels: dict = {"email": False, "teams": False}
    email_recipients: list[str] = []
    teams_channels: list[str] = []
    subject: Optional[str] = None
    email_body: Optional[str] = None
    message: str = ""
    app_name: Optional[str] = None


class AuraChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    attachments: Optional[list] = None
    context: Optional[dict] = None


class IndicatorExclusion(BaseModel):
    excluded_indicators: list[str]


class AppTeamAssignment(BaseModel):
    team_ids: list[int]
