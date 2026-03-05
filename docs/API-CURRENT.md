# Current API Reference

All endpoints are served by the FastAPI backend (`uop-api/app/main.py`).
Base URL: `http://localhost:8080` (dev) or deployed host.

> **Mock Data**: All endpoints currently return deterministic mock data from in-memory Python data structures. No external services are called. See the [Mock Data](#mock-data-implementation) section at the end for details on how each endpoint generates its data and what to replace for live integration.

---

## Common Query Parameters

All dashboard endpoints accept these filter parameters. Filters use AND logic — all active filters are additive.

| Parameter | Type | Format | Description |
|---|---|---|---|
| `lob` | string[] | `?lob=AWM&lob=CIB` | Filter by Line of Business |
| `subLob` | string[] | `?subLob=Asset+Management` | Filter by Sub-LOB |
| `cto` | string[] | `?cto=Jon+Glennie` | Filter by CTO name |
| `cbt` | string[] | `?cbt=Kalpesh+Narkhede` | Filter by CBT name |
| `seal` | string[] | `?seal=16649&seal=35115` | Filter by application SEAL ID |
| `status` | string[] | `?status=critical&status=warning` | Filter by computed health status |
| `search` | string | `?search=Morgan` | Free-text search on name or SEAL (case-insensitive substring) |

Multi-value params use repeated keys: `?lob=AWM&lob=CIB` (not comma-separated).

---

## Dashboard Endpoints

### GET /api/health-summary

Aggregated health metrics across all (or filtered) applications.

**Response**:
```json
{
  "critical_issues": 5,
  "warnings": 12,
  "recurring_30d": 23,
  "incidents_today": 8,
  "trends": {
    "critical_issues": { "spark": [3, 4, 5, 4, 5], "pct": 12.5 },
    "warnings":        { "spark": [10, 11, 12, 11, 12], "pct": -3.2 },
    "recurring_30d":   { "spark": [20, 22, 23, 21, 23], "pct": 5.0 },
    "incidents_today": { "spark": [6, 7, 8, 7, 8], "pct": 8.1 }
  }
}
```

---

### GET /api/ai-analysis

AI-generated health analysis and recommendations.

**Response**:
```json
{
  "critical_alert": "Payment Gateway API experiencing elevated error rates...",
  "trend_analysis": "P1 incidents trending 15% higher than 30-day average...",
  "recommendations": [
    "Investigate payment gateway connection pool exhaustion",
    "Review email notification service SMTP configuration",
    "Schedule capacity review for Morgan Money NAV service"
  ]
}
```

---

### GET /api/regional-status

Health status aggregated by region. Always returns all 3 regions (NA, EMEA, APAC).

**Response**:
```json
[
  { "region": "NA",   "status": "critical", "sod_impacts": 2, "app_issues": 5 },
  { "region": "EMEA", "status": "warning",  "sod_impacts": 1, "app_issues": 3 },
  { "region": "APAC", "status": "healthy",  "sod_impacts": 0, "app_issues": 0 }
]
```

---

### GET /api/critical-apps

Applications currently in critical status.

**Response**:
```json
[
  {
    "id": "morgan-money",
    "name": "Morgan Money",
    "seal": "16649",
    "status": "critical",
    "current_issues": 2,
    "recurring_30d": 6,
    "last_incident": "25m ago",
    "recent_issues": [
      { "description": "NAV calculation timeout — downstream pricing feed delay", "severity": "critical", "time_ago": "25m ago" },
      { "description": "Memory pressure on liquidity aggregation service", "severity": "warning", "time_ago": "2h ago" }
    ]
  }
]
```

---

### GET /api/warning-apps

Applications currently in warning status. Same response schema as `/api/critical-apps`.

---

### GET /api/incident-trends

90-day incident frequency data for trend charts.

**Response**:
```json
{
  "data": [
    { "week": 1, "label": "Dec 2", "p1": 1, "p2": 36 },
    { "week": 2, "label": "Dec 9", "p1": 2, "p2": 38 }
  ],
  "summary": {
    "mttr_hours": 4.2,
    "mtta_minutes": 12,
    "resolution_rate": 94,
    "escalation_rate": 18
  }
}
```

---

### GET /api/active-incidents

Current active incident breakdown by priority.

**Response**:
```json
{
  "week_label": "Feb 24 – Mar 2",
  "p1": {
    "total": 3,
    "trend": -15,
    "breakdown": [
      { "label": "Resolved", "count": 1, "color": "#4caf50" },
      { "label": "In Progress", "count": 2, "color": "#f44336" }
    ]
  },
  "p2": {
    "total": 12,
    "trend": 5,
    "breakdown": [
      { "label": "Resolved", "count": 8, "color": "#4caf50" },
      { "label": "In Progress", "count": 4, "color": "#ff9800" }
    ]
  },
  "convey": { "total": 2, "breakdown": [] },
  "spectrum": { "total": 1, "breakdown": [] }
}
```

---

### GET /api/recent-activities

Activity feed grouped by category.

**Response**:
```json
{
  "categories": [
    {
      "category": "P1 Critical",
      "color": "#f44336",
      "items": [
        { "status": "critical", "description": "Morgan Money — NAV calculation timeout", "time_ago": "25m ago" }
      ]
    }
  ],
  "frequent": [
    { "app": "Morgan Money", "seal": "16649", "status": "critical", "description": "NAV timeout", "occurrences": 6, "last_seen": "25m ago" }
  ]
}
```

---

## Application Endpoints

### GET /api/applications/enriched

Full application catalog with computed health data. See `ARCHITECTURE.md` Section 3.4 for the enriched application schema.

---

### GET /api/indicator-types

Available health indicator types for exclusion filtering.

**Response**: `["Process Group", "Service", "Synthetic"]`

---

### PUT /api/applications/{app_id}/excluded-indicators

Exclude indicator types from health computation for an application.

`app_id` = slug format (lowercase, spaces to hyphens). Example: `morgan-money`

**Request**: `{ "excluded_indicators": ["Synthetic"] }`

**Response**: `{ "app_id": "morgan-money", "excluded_indicators": ["Synthetic"] }`

---

### PUT /api/applications/{app_id}/deployments/{dep_id}/excluded-indicators

Exclude indicator types at the deployment level. Same request/response format.

---

### GET /api/applications/{app_id}/teams

**Response**: `{ "team_ids": [1, 5, 12] }`

---

### PUT /api/applications/{app_id}/teams

**Request**: `{ "team_ids": [1, 5, 12] }`

---

## Knowledge Graph Endpoints

### GET /api/graph/nodes

All component nodes in the dependency graph.

**Response**:
```json
[
  { "id": "connect-portal", "label": "CONNECT-PORTAL", "status": "warning", "team": "Connect Platform", "sla": "99.9%", "incidents_30d": 3 }
]
```

---

### GET /api/graph/dependencies/{service_id}

Forward dependency traversal — what does this service depend on?

**Response**:
```json
{
  "root": { "id": "connect-portal", "label": "CONNECT-PORTAL", "status": "warning" },
  "dependencies": [],
  "edges": [ { "source": "connect-portal", "target": "connect-cloud-gw" } ]
}
```

---

### GET /api/graph/blast-radius/{service_id}

Reverse dependency traversal — what is impacted if this service fails?

**Response**:
```json
{
  "root": { "id": "payment-gateway" },
  "impacted": [],
  "edges": [ { "source": "mm-api", "target": "payment-gateway" } ]
}
```

---

### GET /api/graph/layer-seals

Application SEALs with knowledge graph data.

**Response**:
```json
[
  { "seal": "88180", "label": "Connect OS", "component_count": 6 },
  { "seal": "90176", "label": "Advisor Connect", "component_count": 10 }
]
```

---

### GET /api/graph/layers/{seal_id}

Complete multi-layer graph for a specific application SEAL. Returns five layers: components, platform, datacenter, indicators, and cross-SEAL external nodes.

**Response**:
```json
{
  "seal": "88180",
  "components": {
    "nodes": [
      { "id": "connect-portal", "label": "CONNECT-PORTAL", "status": "warning", "team": "Connect Platform", "sla": "99.9%", "incidents_30d": 3 }
    ],
    "edges": [
      { "source": "connect-portal", "target": "connect-cloud-gw", "direction": "uni" }
    ],
    "external_nodes": [
      {
        "id": "advisor-api-gateway",
        "label": "ADVISOR-API-GATEWAY",
        "status": "healthy",
        "external": true,
        "external_seal": "90176",
        "external_seal_label": "Advisor Connect",
        "cross_direction": "downstream"
      }
    ]
  },
  "platform": {
    "nodes": [ { "id": "gap-pool-na-01", "label": "NA-5S", "type": "gap", "subtype": "pool", "datacenter": "NA-NW-C02", "status": "healthy" } ],
    "edges": [ { "source": "connect-portal", "target": "gap-pool-na-01" } ]
  },
  "datacenter": {
    "nodes": [ { "id": "dc-na-nw-c02", "label": "NA-NW-C02", "region": "NA", "status": "healthy" } ],
    "edges": [ { "source": "gap-pool-na-01", "target": "dc-na-nw-c02" } ]
  },
  "indicators": {
    "nodes": [ { "id": "dt-syn-portal", "label": "connect-portal", "indicator_type": "Synthetic", "health": "amber", "component": "connect-portal" } ],
    "edges": [ { "source": "connect-portal", "target": "dt-syn-portal" } ]
  }
}
```

---

## Team Management Endpoints

### GET /api/teams
Returns all teams with members.

**Response**:
```json
[
  {
    "id": 1,
    "name": "Client Data",
    "emails": ["client-data@jpmchase.com", "client-data-oncall@jpmchase.com"],
    "teams_channels": ["#client-data-alerts", "#client-data-general"],
    "members": [
      { "sid": "A10042", "firstName": "John", "lastName": "Doe", "email": "john.doe@jpmchase.com", "role": "SRE" }
    ]
  }
]
```

### GET /api/teams/roles
Returns the list of available team member roles.

**Response**: `["SRE", "App Owner", "Dev Lead", "Engineering Manager", "Product Owner", "QA Lead", "Platform Engineer", "Scrum Master"]`

### GET /api/teams/{team_id}
Returns a single team (same schema as above).

### GET /api/teams/{team_id}/members
Returns members of a team. Supports optional `?role=` query param to filter by role.

**Query Params**: `role` (optional) — filter members by role name (e.g., `?role=SRE`)

**Response**:
```json
[
  { "sid": "A10042", "firstName": "John", "lastName": "Doe", "email": "john.doe@jpmchase.com", "role": "SRE" }
]
```

### POST /api/teams
Create a team. Request:
```json
{
  "name": "New Team",
  "emails": ["team@jpmchase.com"],
  "teams_channels": ["#new-team-alerts"],
  "members": [
    { "sid": "A10042", "firstName": "John", "lastName": "Doe", "email": "john.doe@jpmchase.com", "role": "SRE" }
  ]
}
```

### PUT /api/teams/{team_id}
Update a team. All fields optional (including `members`).

### DELETE /api/teams/{team_id}
Delete a team. Response: `{ "ok": true }`

---

## Directory Endpoints

### GET /api/directory/search
Search the corporate directory by name, SID, or email.

**Query Params**: `q` (required) — search query (case-insensitive substring match)

**Response** (top 20 matches):
```json
[
  { "sid": "A10042", "firstName": "John", "lastName": "Doe", "email": "john.doe@jpmchase.com", "department": "Technology", "title": "Senior Engineer" }
]
```

---

## Announcement Endpoints

### GET /api/announcements
Query params: `status` (open/closed), `channel` (teams/email/connect/banner), `search`

### GET /api/announcements/notifications
Returns open announcements marked for banner display.

### POST /api/announcements
Create announcement with multi-channel targeting.

**Request**:
```json
{
  "title": "Scheduled Maintenance",
  "status": "open",
  "severity": "warning",
  "impacted_apps": ["Morgan Money"],
  "description": "Planned maintenance window...",
  "channels": {
    "teams": { "enabled": true },
    "email": { "enabled": true, "recipients": ["team@example.com"] },
    "connect": { "enabled": false },
    "banner": { "enabled": true }
  },
  "regions": ["NA", "EMEA"]
}
```

### PUT /api/announcements/{id}
Update announcement.

### PATCH /api/announcements/{id}/status
Toggle status between open/closed.

### DELETE /api/announcements/{id}

---

## AURA AI Chat Endpoint

### POST /api/aura/chat

Streams responses via Server-Sent Events (SSE).

**Request**:
```json
{
  "message": "What is the current health status of Morgan Money?",
  "conversation_id": "conv-123",
  "context": { "current_page": "dashboard", "active_filters": { "lob": ["AWM"] } }
}
```

**SSE Event Protocol**:

| Event | Payload | Description |
|---|---|---|
| `meta` | `{ message_id, timestamp }` | Sent first — conversation metadata |
| `block` | `{ type, data }` | Content block (see types below) |
| `followups` | `["question1", "question2"]` | Suggested follow-up questions |
| `done` | `{}` | Stream complete signal |

**Content block types**: `"text"` (markdown string), `"metric_cards"` (KPI array), `"status_list"` (RAG items), `"chart"` (chart data), `"recommendations"` (action items).

---

## Outcome Measures Endpoints

### GET /api/outcome-measures/summary

Executive KPI bar and section list for all 5 outcome sections.

**Response**:
```json
{
  "app_count": 81,
  "sections": [
    { "id": 1, "key": "usage", "label": "Usage & Adoption", "short": "Usage" },
    { "id": 2, "key": "workstreams", "label": "Workstream Outcomes", "short": "Workstreams" }
  ],
  "executive_kpis": [
    { "label": "AI Prompts/App", "value": 42.5, "baseline": 13.9, "change_pct": 206.1, "good_direction": "up", "spark": [14, 18, 22, ...] }
  ],
  "month_labels": ["Apr'25", "May'25", ..., "Mar'26"]
}
```

---

### GET /api/outcome-measures/section/{section_id}

Section-specific KPI cards and trend data. `section_id` = 1-5.

**Response**:
```json
{
  "section": { "id": 1, "key": "usage", "label": "Usage & Adoption" },
  "metrics": [
    { "key": "prompts_per_app", "label": "AI Prompts / App / Month", "current": 42.5, "baseline": 13.9, "trend": [14, 18, ...] }
  ]
}
```

---

### GET /api/outcome-measures/leaderboard

CTO/CBT ranked table for a given section.

**Query Params**: `section_id` (required), `sort_by` (optional metric key)

**Response**:
```json
{
  "rows": [
    { "cto": "Lakith Leelasena", "cbt": "Kent Zheng", "app_count": 4, "metrics": { "prompts_per_app": 45.2, ... }, "spark": { ... } }
  ],
  "metric_keys": ["prompts_per_app", "click_through_rate"]
}
```

---

### GET /api/outcome-measures/coverage

Baselines and coverage data (section 5 only).

**Response**:
```json
{
  "coverages": [
    { "key": "slo_defined", "label": "SLO Defined", "covered": 68, "total": 81, "pct": 84.0 }
  ],
  "heatmap": [
    { "cto": "Lakith Leelasena", "cbt": "Kent Zheng", "app_count": 4, "coverage_pct": 87.5 }
  ]
}
```

---

## Essential Services Endpoints

### GET /api/essential-services/summary

All 15 Essential Services with RAG status, app counts, risk matrix, and KPIs. Accepts standard filter params.

**Response**:
```json
{
  "services": [
    { "id": "3213", "name": "Administer Sweep Functionality", "status": "healthy", "criticality": "high", "description": "...", "app_count": 8, "total_mapped": 8, "deployment_count": 12 }
  ],
  "kpis": { "total": 15, "healthy": 9, "degraded": 4, "down": 2 },
  "risk_matrix": { "critical_healthy": 3, "critical_degraded": 1, "high_down": 4, ... }
}
```

---

### GET /api/essential-services/{service_id}

Detail for one Essential Service — mapped apps with deployment info, CTO/CBT coverage.

**Response**:
```json
{
  "service": { "id": "3213", "name": "Administer Sweep Functionality", "status": "healthy", "criticality": "high", "app_count": 8 },
  "mapped_apps": [
    { "seal": "90556", "name": "Spectrum UI", "status": "healthy", "lob": "AWM", "cto": "Sheetal Gandhi", "cbt": "Alex Feinberg", "deploymentTypes": ["gap", "gkp"], "p1_30d": 0 }
  ],
  "cto_coverage": [{ "cto": "Lakith Leelasena", "app_count": 3, "status": "healthy" }],
  "cbt_coverage": [{ "cbt": "Kent Zheng", "app_count": 2, "status": "healthy" }]
}
```

---

### GET /api/essential-services/business-processes

Business processes with their ES dependencies and derived status. Accepts standard filter params.

**Response**:
```json
{
  "processes": [
    { "id": "bp1", "name": "NAV Calculation & Distribution", "description": "...", "status": "degraded", "steps": ["Application", "KYC/AML Check", ...], "services": [{ "id": "3208", "name": "Calculate and distribute Net Asset Values (NAVs) (AM)", "status": "healthy" }], "service_count": 4 }
  ]
}
```

---

### GET /api/essential-services/impact-graph/{service_id}

ReactFlow-compatible graph data showing ES → deployment types → apps.

**Response**:
```json
{
  "nodes": [
    { "id": "es-3213", "type": "service", "data": { "label": "Administer Sweep Functionality", "status": "healthy", "criticality": "high" } },
    { "id": "dep-gap", "type": "deployment", "data": { "label": "GAP", "type": "gap" } },
    { "id": "app-90556", "type": "app", "data": { "label": "Spectrum UI", "seal": "90556", "status": "healthy" } }
  ],
  "edges": [
    { "source": "es-3213", "target": "dep-gap" },
    { "source": "dep-gap", "target": "app-90556" }
  ]
}
```

---

### GET /api/essential-services/tree-mapping

How ES map to both Business and Technology organizational trees.

**Response**:
```json
{
  "business_tree": { "AWM": { "Asset Management": { "Client": [{ "id": "3213", "name": "Administer Sweep Functionality" }] } } },
  "technology_tree": { "AWM": { "Lakith Leelasena": { "Kent Zheng": [{ "id": "3213", "name": "Administer Sweep Functionality" }] } } }
}
```

---

## Situation Room Endpoints

### GET /api/situation-room/situations

List all situations (summary fields only).

**Response**:
```json
[
  { "id": 1, "incident_number": "INC0012345", "title": "Database failover event", "state": "Investigating", "priority": "P1 - Critical", "opened_time": "2026-03-03T...", "updated_at": "2026-03-03T..." }
]
```

---

### GET /api/situation-room/options

Return all dropdown options for Situation Room forms (timeline, next_update, state, priority).

**Response**:
```json
{
  "timeline_options": ["T0 - Detected", "T1 - Triaging", "T2 - Mitigating", "T3 - Monitoring", "T4 - Resolved"],
  "next_update_options": ["Every 15 min", "Every 30 min", "Every 1 hour"],
  "state_options": ["New", "Investigating", "Mitigating", "Resolved", "Closed"],
  "priority_options": ["P1 - Critical", "P2 - High", "P3 - Medium"]
}
```

---

### GET /api/situation-room/systems

Return all system definitions (logical groupings of apps by SEAL).

**Response**:
```json
[
  { "id": "sys-trading", "name": "Trading Platform", "seals": ["35206", "87082", "81884"], "description": "..." }
]
```

---

### GET /api/situation-room/systems/{system_id}/capabilities

Return all component labels for a system's apps.

**Response**:
```json
{ "system_id": "sys-trading", "capabilities": ["Order Router", "Matching Engine", "FIX Gateway"] }
```

---

### GET /api/situation-room/situations/{situation_id}

Full situation detail with computed systems table (health status, SRE leads, impacted capabilities).

**Response**:
```json
{
  "id": 1, "incident_number": "INC0012345", "title": "...", "state": "Investigating",
  "priority": "P1 - Critical", "system_overrides": {},
  "systems": [
    { "id": "sys-trading", "name": "Trading Platform", "status": "critical", "app_count": 3, "timeline": "T0 - Detected", "impacted_capabilities": [], "sre_leads": ["Jane Doe"] }
  ]
}
```

---

### GET /api/situation-room/situations/{situation_id}/report

Per-incident deep-dive report data for PDF export.

**Response**: Full situation with computed systems, app-level details, timeline events, and CTO/CBT coverage.

---

### POST /api/situation-room/situations

Create a new situation.

**Request**: `SituationCreate` schema — `{ "incident_number": "INC...", "title": "...", "state": "New", "priority": "P1 - Critical", "opened_time": "..." }`

**Response**: Created situation object with generated `id`.

---

### PUT /api/situation-room/situations/{situation_id}

Update situation fields (title, state, priority, etc.).

**Request**: `SituationUpdate` schema — any subset of situation fields.

**Response**: Updated situation object.

---

### PATCH /api/situation-room/situations/{situation_id}/systems/{system_id}

Update per-system overrides (timeline, impacted capabilities, SRE lead overrides, next update interval).

**Request**: `SystemOverrideUpdate` — `{ "timeline": "T2 - Mitigating", "impacted_capabilities": ["Order Router"], "next_update": "Every 30 min" }`

**Response**: Updated system override object.

---

### DELETE /api/situation-room/situations/{situation_id}

Delete a situation.

**Response**: `{ "deleted": 1 }`

---

## View Central Notification Endpoints

### GET /api/vc-notifications/{view_id}

Get all notification rules for a View Central dashboard.

**Response**:
```json
[
  { "id": 1, "view_id": "abc", "name": "Critical Alerts", "alert_types": ["critical"], "channels": {"email": true, "teams": false}, "email_recipients": ["user@example.com"], "frequency": "immediate", "enabled": true, "created_at": "...", "updated_at": "..." }
]
```

---

### POST /api/vc-notifications/{view_id}

Create a notification rule for a view.

**Request**: `VCNotificationCreate` — name, alert_types, channels, email_recipients, frequency, schedule fields, enabled, view_filters.

**Response**: Created notification object.

---

### PUT /api/vc-notifications/{view_id}/{notif_id}

Update a notification rule.

**Request**: `VCNotificationUpdate` — any subset of notification fields.

**Response**: Updated notification object.

---

### PATCH /api/vc-notifications/{view_id}/{notif_id}/toggle

Toggle a notification rule enabled/disabled.

**Response**: Updated notification with toggled `enabled` field.

---

### DELETE /api/vc-notifications/{view_id}/{notif_id}

Delete a notification rule.

**Response**: `{ "ok": true }`

---

### POST /api/vc-notifications/{view_id}/{notif_id}/test

Send a test email for a notification rule. Requires email channel and recipients configured.

**Response**: `{ "ok": true, "detail": "Test email queued to 1 recipients" }`

---

## Announcements Connect Endpoints

### GET /api/announcements/connect/weave-interfaces

Return available Weave interface entities for Connect-channel announcement targeting.

**Response**: Array of entity objects with names and regions.

---

### GET /api/announcements/connect/validate

Validate a Connect targeting selection and return estimated user reach.

**Query params**: `entities` (comma-separated), `regions` (comma-separated)

**Response**: `{ "message": "Announcement will be sent to 3,200 all Connect users" }`

---

## Teams Role Management Endpoints

### GET /api/teams/roles

List all available member roles.

**Response**: `["SRE Lead", "Platform Engineer", "Incident Commander", ...]`

---

### POST /api/teams/roles

Create a new role. Returns 409 if name already exists.

**Request**: `{ "name": "New Role Name" }`

**Response**: `{ "ok": true, "roles": [...] }`

---

### PUT /api/teams/roles/{role_name}

Rename a role. Cascades the rename to all team members using that role.

**Request**: `{ "name": "Updated Role Name" }`

**Response**: `{ "ok": true, "roles": [...] }`

---

### DELETE /api/teams/roles/{role_name}

Delete a role. Returns 409 if any team members are currently assigned.

**Response**: `{ "ok": true, "roles": [...] }`

---

## Contact Endpoint

### POST /api/contact/send

Send notification to teams/individuals.

**Request**: `{ "type": "teams|email", "recipients": ["team@example.com"], "subject": "Alert", "message": "...", "app_name": "Morgan Money" }`

**Response**: `{ "status": "sent", "type": "email", "recipients": [...], "message_preview": "..." }`

---

## Mock Data Implementation

Every endpoint above currently returns **deterministic mock data**. This section documents where each endpoint's data originates and what needs to change for live integration.

### Data Sources (Backend)

| Source | File | Description |
|---|---|---|
| `APPS_REGISTRY` | `app/mock_data/apps_registry.py` | 81 applications with business metadata + operational fields (incidents, region) |
| `NODES` | `app/mock_data/graph_data.py` | 90+ component service nodes with id, label, status, team, sla, incidents_30d |
| `EDGES_RAW` | `app/mock_data/graph_data.py` | 100+ component dependency edges (source, target) tuples |
| `SEAL_COMPONENTS` | `app/mock_data/graph_data.py` | Mapping: SEAL ID → component IDs (10 SEALs) |
| `INDICATOR_NODES` | `app/mock_data/graph_data.py` | 869 health indicators with type, health status, parent component |
| `PLATFORM_NODES` | `app/mock_data/graph_data.py` | 10 platform infrastructure nodes (GAP, GKP, ECS, EKS) |
| `DATA_CENTER_NODES` | `app/mock_data/graph_data.py` | 6 data center nodes (NA, EMEA, APAC) |
| `COMPONENT_PLATFORM_EDGES` | `app/mock_data/graph_data.py` | Component → Platform hosting mappings |
| `DEPLOYMENT_OVERRIDES` | `app/mock_data/graph_data.py` | Custom deployment definitions for 3 apps |
| `APP_SLO_DATA` | `app/mock_data/slo_data.py` | SLO targets/actuals for 26 apps (others use 99.0% default) |
| `INCIDENT_TRENDS` | `app/mock_data/dashboard_data.py` | 13-week hardcoded P1/P2 trend data |
| `_AURA_SCENARIOS` | `app/mock_data/aura_data.py` | Keyword → response handler mapping for 11 chat scenarios |
| `TEAMS` | `app/mock_data/teams_data.py` | 48 teams with role-based members |
| `DIRECTORY_ENTRIES` | `app/mock_data/directory_data.py` | 200 corporate directory entries |
| Outcome Measures | `app/mock_data/outcome_measures_data.py` | Deterministic per-SEAL metrics (5 sections, 12-month trends, baselines) via `hashlib.md5(seal)` |
| Essential Services | `app/mock_data/essential_services_data.py` | 15 ES definitions, curated SEAL mappings (3-8 apps each), 12 business processes |
| Situation Room | `app/mock_data/situation_room_data.py` | Systems, situations, timeline/state/priority options, system overrides |
| VC Notifications | `app/services/vc_monitor.py` | In-memory notification rules, alert state tracking, email templates |

### How Each Endpoint Uses Mock Data

| Endpoint | Mock Data Source | Replace With |
|---|---|---|
| `/api/health-summary` | Counts from `_get_enriched_apps()` + `APPS_REGISTRY` operational fields | ServiceNow incident API + enriched app status |
| `/api/ai-analysis` | Hardcoded text generated from filter scope | AURA AI streaming API |
| `/api/regional-status` | Aggregated from `_get_enriched_apps()` grouped by `region` | Same logic but with live app status data |
| `/api/critical-apps` | Filtered from `_get_enriched_apps()` where `status == "critical"` | Same filter but with live status + ServiceNow incidents |
| `/api/warning-apps` | Same, where `status == "warning"` | Same |
| `/api/incident-trends` | Static `INCIDENT_TRENDS` array, scaled proportionally by filter scope | ServiceNow incident data aggregated by week |
| `/api/active-incidents` | Derived from critical/warning app counts | ServiceNow active incident query |
| `/api/recent-activities` | Generated from critical/warning apps' `recent_issues` | ServiceNow recent activity feed |
| `/api/applications/enriched` | Full enrichment pipeline: `APPS_REGISTRY` → `SEAL_COMPONENTS` → status propagation | Product Catalog + ERMA/V12 + Dynatrace + ServiceNow |
| `/api/graph/*` | `NODES`, `EDGES_RAW`, `INDICATOR_NODES`, `PLATFORM_NODES` | ERMA/V12 Knowledge Graph + Dynatrace |
| `/api/aura/chat` | Keyword matching → hardcoded scenario responses | AURA AI streaming API |
| `/api/teams` | In-memory array of 48 teams with members from directory | Teams/directory service |
| `/api/teams/roles` | Static `MEMBER_ROLES` list (8 roles) | Role management service |
| `/api/teams/{id}/members` | Members from team data, filterable by role | Teams/directory service |
| `/api/directory/search` | 200 mock directory entries searched by name/SID/email | Corporate directory service |
| `/api/announcements` | In-memory array of 4 announcements | Persistent database |
| `/api/contact/send` | Returns mock "sent" response | Teams webhook + SMTP gateway |
| `/api/outcome-measures/*` | Deterministic per-SEAL metrics from `outcome_measures_data.py`, aggregated by filter scope | Metrics database / data lake |
| `/api/essential-services/*` | 15 ES with curated SEAL mappings from `essential_services_data.py`, status from enriched apps | ES Mapping API + enriched app status |
| `/api/situation-room/*` | Systems, situations, overrides from `situation_room_data.py` | ServiceNow major incident API + system registry |
| `/api/vc-notifications/*` | In-memory notification rules from `vc_monitor.py` | Persistent database + notification service |
| `/api/announcements/connect/*` | Hardcoded Weave interfaces and user counts | Connect platform API |

### Developer Guide: Replacing Mock Data

1. **Keep the same response schemas** — the frontend depends on the exact field names and shapes documented above
2. **Add environment variables** for external service URLs and credentials (see `ARCHITECTURE.md` Section 9.4)
3. **Replace data sources one at a time** — start with `APPS_REGISTRY` (Product Catalog), then incidents (ServiceNow), then graph data (ERMA/V12)
4. **Cache expensive computations** — `_get_enriched_apps()` is currently cached at module level; maintain a similar caching strategy with TTL for live data
5. **Filter logic stays the same** — `_filter_dashboard_apps()` works on any array of app objects matching the schema, regardless of whether data is mock or live
6. **Test with mock data first** — run the app locally to verify frontend behavior, then swap in live API calls behind the same endpoint routes
