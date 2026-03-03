"""Mock data package — centralises all static/seed data for the UOP API.

Each submodule carries a ``# REAL: Replace with …`` comment describing
the production data-source that should eventually supersede it.
"""

from .apps_registry import APPS_REGISTRY

from .graph_data import (
    NODES,
    INDICATOR_TYPES,
    COMPONENT_INDICATOR_MAP,
    EDGES_RAW,
    SEAL_COMPONENTS,
    INDICATOR_NODES,
    PLATFORM_NODES,
    PLATFORM_NODE_MAP,
    COMPONENT_PLATFORM_EDGES,
    DATA_CENTER_NODES,
    DC_LOOKUP,
    COMP_TO_SEAL,
    SEAL_LABELS,
    BIDIRECTIONAL_PAIRS,
)

from .dashboard_data import (
    INCIDENT_TRENDS,
    INCIDENT_TREND_SUMMARY,
    _GLOBAL_ACTIVITY_CATEGORIES,
    _FREQUENT_ISSUE_TEMPLATES,
)

from .slo_data import (
    DEPLOYMENT_OVERRIDES,
    APP_SLO_DATA,
)

from .announcements_data import (
    WEAVE_INTERFACES,
    ANNOUNCEMENTS,
    _next_announcement_id,
)

from .directory_data import DIRECTORY

from .teams_data import (
    TEAMS,
    MEMBER_ROLES,
)

from .situation_room_data import (
    SYSTEMS as SR_SYSTEMS,
    SITUATIONS,
    TIMELINE_OPTIONS,
    NEXT_UPDATE_OPTIONS,
)

from .aura_data import (
    _aura_incident_analysis,
    _aura_slo_report,
    _aura_blast_radius,
    _aura_mttr_analysis,
    _aura_executive_summary,
    _aura_capacity_planning,
    _aura_deployment_status,
    _aura_alert_analysis,
    _aura_regional_comparison,
    _aura_trend_forecast,
    _aura_team_performance,
    _aura_default_response,
    _AURA_SCENARIOS,
)

__all__ = [
    # apps_registry
    "APPS_REGISTRY",
    # graph_data
    "NODES",
    "INDICATOR_TYPES",
    "COMPONENT_INDICATOR_MAP",
    "EDGES_RAW",
    "SEAL_COMPONENTS",
    "INDICATOR_NODES",
    "PLATFORM_NODES",
    "PLATFORM_NODE_MAP",
    "COMPONENT_PLATFORM_EDGES",
    "DATA_CENTER_NODES",
    "DC_LOOKUP",
    "COMP_TO_SEAL",
    "SEAL_LABELS",
    "BIDIRECTIONAL_PAIRS",
    # dashboard_data
    "INCIDENT_TRENDS",
    "INCIDENT_TREND_SUMMARY",
    "_GLOBAL_ACTIVITY_CATEGORIES",
    "_FREQUENT_ISSUE_TEMPLATES",
    # slo_data
    "DEPLOYMENT_OVERRIDES",
    "APP_SLO_DATA",
    # announcements_data
    "WEAVE_INTERFACES",
    "ANNOUNCEMENTS",
    "_next_announcement_id",
    # directory_data
    "DIRECTORY",
    # teams_data
    "TEAMS",
    "MEMBER_ROLES",
    # aura_data
    "_aura_incident_analysis",
    "_aura_slo_report",
    "_aura_blast_radius",
    "_aura_mttr_analysis",
    "_aura_executive_summary",
    "_aura_capacity_planning",
    "_aura_deployment_status",
    "_aura_alert_analysis",
    "_aura_regional_comparison",
    "_aura_trend_forecast",
    "_aura_team_performance",
    "_aura_default_response",
    "_AURA_SCENARIOS",
    # situation_room_data
    "SR_SYSTEMS",
    "SITUATIONS",
    "TIMELINE_OPTIONS",
    "NEXT_UPDATE_OPTIONS",
]
