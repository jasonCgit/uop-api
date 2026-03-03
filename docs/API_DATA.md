# API_DATA.md — Comprehensive API Specification

> **Unified Observability Portal** — Full endpoint inventory, response schemas, file mappings, and database schemas for connecting the UI to real data.

---

## Table of Contents

- [1. Common Query Parameters](#1-common-query-parameters)
- [2. Dashboard Endpoints](#2-dashboard-endpoints)
  - [2.1 GET /api/health-summary](#21-get-apihealth-summary)
  - [2.2 GET /api/ai-analysis](#22-get-apiai-analysis)
  - [2.3 GET /api/regional-status](#23-get-apiregional-status)
  - [2.4 GET /api/critical-apps](#24-get-apicritical-apps)
  - [2.5 GET /api/warning-apps](#25-get-apiwarning-apps)
  - [2.6 GET /api/incident-trends](#26-get-apiincident-trends)
  - [2.7 GET /api/frequent-incidents](#27-get-apifrequent-incidents)
  - [2.8 GET /api/active-incidents](#28-get-apiactive-incidents)
  - [2.9 GET /api/recent-activities](#29-get-apirecent-activities)
- [3. Application Endpoints](#3-application-endpoints)
  - [3.1 GET /api/applications/enriched](#31-get-apiapplicationsenriched)
  - [3.2 GET /api/indicator-types](#32-get-apiindicator-types)
  - [3.3 PUT /api/applications/{app_id}/excluded-indicators](#33-put-apiapplicationsapp_idexcluded-indicators)
  - [3.4 PUT /api/applications/{app_id}/deployments/{dep_id}/excluded-indicators](#34-put-apiapplicationsapp_iddeploymentsdep_idexcluded-indicators)
  - [3.5 GET /api/applications/{app_id}/teams](#35-get-apiapplicationsapp_idteams)
  - [3.6 PUT /api/applications/{app_id}/teams](#36-put-apiapplicationsapp_idteams)
- [4. Knowledge Graph Endpoints](#4-knowledge-graph-endpoints)
  - [4.1 GET /api/graph/nodes](#41-get-apigraphnodes)
  - [4.2 GET /api/graph/dependencies/{service_id}](#42-get-apigraphdependenciesservice_id)
  - [4.3 GET /api/graph/blast-radius/{service_id}](#43-get-apigraphblast-radiusservice_id)
  - [4.4 GET /api/graph/layer-seals](#44-get-apigraphlayer-seals)
  - [4.5 GET /api/graph/layers/{seal_id}](#45-get-apigraphlayersseal_id)
- [5. Team Management Endpoints](#5-team-management-endpoints)
- [6. Announcement Endpoints](#6-announcement-endpoints)
- [7. View Central Notification Endpoints](#7-view-central-notification-endpoints)
- [8. AURA AI Chat Endpoint](#8-aura-ai-chat-endpoint)
- [9. Contact / Messaging Endpoint](#9-contact--messaging-endpoint)
- [10. Future Endpoints (Not Yet Built)](#10-future-endpoints-not-yet-built)
  - [10.1 Incident Zero Endpoints](#101-incident-zero-endpoints)
  - [10.2 Customer Journey Endpoints](#102-customer-journey-endpoints)
  - [10.3 SLO Agent Endpoints](#103-slo-agent-endpoints)
  - [10.4 Search & Filter Endpoints](#104-search--filter-endpoints)
- [11. File Mapping](#11-file-mapping)
- [12. Database Schemas](#12-database-schemas)

---

## 1. Common Query Parameters

All dashboard endpoints (Sections 2.1–2.9) accept these filter parameters. Filters use **AND logic** — all active filters are additive. Multi-value params use repeated keys (not comma-separated).

| Parameter | Type | Format | Description |
|-----------|------|--------|-------------|
| `lob` | string[] | `?lob=AWM&lob=CIB` | Filter by Line of Business |
| `subLob` | string[] | `?subLob=Asset+Management` | Filter by Sub-LOB |
| `cto` | string[] | `?cto=Jon+Glennie` | Filter by CTO name |
| `cbt` | string[] | `?cbt=Kalpesh+Narkhede` | Filter by CBT name |
| `seal` | string[] | `?seal=16649&seal=35115` | Filter by application SEAL ID |
| `status` | string[] | `?status=critical&status=warning` | Filter by computed health status |
| `search` | string | `?search=Morgan` | Free-text search on app name/SEAL (case-insensitive substring) |

**Query String Building** (frontend → backend):

```
// Input: activeFilters = { lob: ["AWM", "CIB"], seal: ["16649"] }, searchText = "Morgan"
// Output: ?lob=AWM&lob=CIB&seal=16649&search=Morgan

```

---

## 2. Dashboard Endpoints

### 2.1 GET /api/health-summary

Aggregated health metrics across all (or filtered) applications.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/health-summary` |
| **Purpose** | Provides KPI counts for the SummaryCards dashboard widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
{
  "critical_issues": 5,
  "warnings": 12,
  "recurring_30d": 23,
  "incidents_today": 8,
  "trends": {
    "critical_issues": { "spark": [7, 6, 6, 5, 6, 5, 5], "pct": -33 },
    "warnings":        { "spark": [24, 23, 22, 12, 13, 12, 12], "pct": -50 },
    "recurring_30d":   { "spark": [19, 20, 20, 21, 22, 22, 23], "pct": 21 },
    "incidents_today": { "spark": [13, 12, 12, 8, 9, 8, 8], "pct": -38 }
  }
}

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `critical_issues` | integer | Count of apps with `status = "critical"` |
| `warnings` | integer | Count of apps with `status = "warning"` |
| `recurring_30d` | integer | Sum of `recurring_30d` across filtered apps |
| `incidents_today` | integer | Sum of `incidents_today` across filtered apps |
| `trends` | object | Trend data per metric |
| `trends.*.spark` | integer[] | 7-point sparkline array for mini-chart |
| `trends.*.pct` | number | Percentage change trend (negative = improving) |

---

### 2.2 GET /api/ai-analysis

AI-generated health analysis and actionable recommendations.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/ai-analysis` |
| **Purpose** | Powers the AIHealthPanel dashboard widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
{
  "critical_alert": "Currently tracking 2 critical applications in AWM. Morgan Money and Quantum are experiencing active incidents requiring immediate attention.",
  "trend_analysis": "45 incidents recorded across 24 applications in the last 30 days.",
  "recommendations": [
    "Investigate Morgan Money — NAV calculation timeout — downstream pricing feed delay",
    "Investigate Quantum — Portfolio service memory pressure detected",
    "Monitor PANDA — Cache invalidation storm recurring every 6 hours"
  ]
}

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `critical_alert` | string | Primary alert text (contextual to filter scope) |
| `trend_analysis` | string | Incident trend summary text |
| `recommendations` | string[] | Actionable items (max 4), prioritized by severity |

---

### 2.3 GET /api/regional-status

Health status aggregated by geographic region. Always returns all 3 regions.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/regional-status` |
| **Purpose** | Powers the RegionalStatus dashboard widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
[
  { "region": "NA",   "status": "critical", "sod_impacts": 2, "app_issues": 5 },
  { "region": "EMEA", "status": "warning",  "sod_impacts": 1, "app_issues": 3 },
  { "region": "APAC", "status": "healthy",  "sod_impacts": 0, "app_issues": 0 }
]

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `region` | string | Region code: `"NA"`, `"EMEA"`, `"APAC"` |
| `status` | string | Worst health across region's apps: `"critical"` \| `"warning"` \| `"healthy"` |
| `sod_impacts` | integer | Count of critical apps (Start-of-Day impacting) |
| `app_issues` | integer | Sum of `incidents_today` in that region |

---

### 2.4 GET /api/critical-apps

Applications currently in critical status with their recent issues.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/critical-apps` |
| **Purpose** | Powers the CriticalApps dashboard widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
[
  {
    "id": "16649",
    "name": "Morgan Money",
    "seal": "SEAL - 16649",
    "status": "critical",
    "current_issues": 2,
    "recurring_30d": 6,
    "last_incident": "25m ago",
    "recent_issues": [
      {
        "description": "NAV calculation timeout — downstream pricing feed delay",
        "severity": "critical",
        "time_ago": "25m ago"
      },
      {
        "description": "Memory pressure on liquidity aggregation service",
        "severity": "warning",
        "time_ago": "2h ago"
      }
    ]
  }
]

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | SEAL ID |
| `name` | string | Application display name |
| `seal` | string | Formatted as `"SEAL - {id}"` |
| `status` | string | Always `"critical"` for this endpoint |
| `current_issues` | integer | Count of `recent_issues` |
| `recurring_30d` | integer | Recurring issue count over 30 days |
| `last_incident` | string | Relative timestamp (e.g., `"25m ago"`, `"2h ago"`, `"—"`) |
| `recent_issues` | object[] | Array of issue objects |
| `recent_issues[].description` | string | Issue description text |
| `recent_issues[].severity` | string | `"critical"` \| `"warning"` |
| `recent_issues[].time_ago` | string | Relative timestamp |

---

### 2.5 GET /api/warning-apps

Applications currently in warning status. **Same response schema as `/api/critical-apps`** with `status = "warning"`.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/warning-apps` |
| **Purpose** | Powers the WarningApps dashboard widget |
| **Status Codes** | `200 OK` |

---

### 2.6 GET /api/incident-trends

90-day incident frequency data aggregated into weekly buckets, with summary statistics.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/incident-trends` |
| **Purpose** | Powers the IncidentTrends chart widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
{
  "data": [
    { "week": "2025-12-01", "label": "Dec 01", "p1": 1, "p2": 36 },
    { "week": "2025-12-08", "label": "Dec 08", "p1": 0, "p2": 42 },
    { "week": "2025-12-15", "label": "Dec 15", "p1": 2, "p2": 38 },
    { "week": "2025-12-22", "label": "Dec 22", "p1": 1, "p2": 28 },
    { "week": "2025-12-29", "label": "Dec 29", "p1": 0, "p2": 45 }
  ],
  "summary": {
    "mttr_hours": 2.4,
    "mtta_minutes": 8,
    "resolution_rate": 94.2,
    "escalation_rate": 12
  }
}

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `data` | object[] | Weekly incident counts (~13 weeks) |
| `data[].week` | string | ISO date of week start (Monday) |
| `data[].label` | string | Display label (e.g., `"Dec 01"`) |
| `data[].p1` | integer | P1 incidents that week |
| `data[].p2` | integer | P2 incidents that week |
| `summary.mttr_hours` | number | Mean Time To Resolve (hours) |
| `summary.mtta_minutes` | number | Mean Time To Acknowledge (minutes) |
| `summary.resolution_rate` | number | Percentage of incidents resolved |
| `summary.escalation_rate` | number | Percentage of incidents escalated |

---

### 2.7 GET /api/frequent-incidents

Top recurring incidents derived from enriched app data.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/frequent-incidents` |
| **Purpose** | Powers the FrequentIncidents dashboard widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
[
  {
    "app": "Morgan Money",
    "seal": "16649",
    "status": "critical",
    "description": "NAV calculation timeout — downstream pricing feed delay",
    "occurrences": 8,
    "last_seen": "25m ago"
  },
  {
    "app": "Quantum",
    "seal": "91001",
    "status": "critical",
    "description": "Portfolio service memory pressure detected",
    "occurrences": 6,
    "last_seen": "1h ago"
  }
]

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `app` | string | Application name |
| `seal` | string | SEAL ID |
| `status` | string | App health status |
| `description` | string | Issue description |
| `occurrences` | integer | Recurrence count (recurring_30d + incidents_today) |
| `last_seen` | string | Relative timestamp of last occurrence |

---

### 2.8 GET /api/active-incidents

Current active incident breakdown by priority with resolved/unresolved splits.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/active-incidents` |
| **Purpose** | Powers the ActiveIncidentsPanel (donut charts) |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
{
  "week_label": "Last 7 Days",
  "p1": {
    "total": 3,
    "trend": -33,
    "breakdown": [
      { "label": "Unresolved", "count": 2, "color": "#f44336" },
      { "label": "Resolved",   "count": 1, "color": "#4ade80" }
    ]
  },
  "p2": {
    "total": 12,
    "trend": -20,
    "breakdown": [
      { "label": "Unresolved", "count": 4, "color": "#ffab00" },
      { "label": "Resolved",   "count": 8, "color": "#4ade80" }
    ]
  },
  "convey": {
    "total": 5,
    "trend": -20,
    "breakdown": [
      { "label": "Unresolved", "count": 2, "color": "#60a5fa" },
      { "label": "Resolved",   "count": 3, "color": "#4ade80" }
    ]
  },
  "spectrum": {
    "total": 4,
    "trend": 0,
    "breakdown": [
      { "label": "Info", "count": 3, "color": "#60a5fa" },
      { "label": "High", "count": 1, "color": "#f44336" }
    ]
  }
}

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `week_label` | string | Display label for the time range |
| `p1` / `p2` / `convey` / `spectrum` | object | Incident category data |
| `*.total` | integer | Total count in category |
| `*.trend` | number | Week-over-week percentage change |
| `*.breakdown` | object[] | Segment breakdowns for donut chart |
| `*.breakdown[].label` | string | Segment label |
| `*.breakdown[].count` | integer | Segment count |
| `*.breakdown[].color` | string | Hex color for chart rendering |

---

### 2.9 GET /api/recent-activities

Activity feed grouped by category. Includes P1/P2 incidents (filter-scoped) and global platform categories (always shown).

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/recent-activities` |
| **Purpose** | Powers the RecentActivities dashboard widget |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
[
  {
    "category": "P1 INCIDENTS",
    "color": "#f44336",
    "items": [
      { "status": "CRITICAL", "description": "Morgan Money — NAV calculation timeout", "time_ago": "25m ago" }
    ]
  },
  {
    "category": "P2 INCIDENTS",
    "color": "#ff9800",
    "items": [
      { "status": "UNRESOLVED", "description": "PANDA — Cache invalidation storm", "time_ago": "4h ago" }
    ]
  },
  {
    "category": "CONVEY NOTIFICATIONS",
    "color": "#60a5fa",
    "items": [
      { "status": "UNRESOLVED", "description": "Starting Feb 26, all Flipper tasks targeting Production Load Balancers will be blocked.", "time_ago": "22h ago" },
      { "status": "RESOLVED", "description": "Rest of the NAMR alerts are ready to review.", "time_ago": "23h ago" }
    ]
  },
  {
    "category": "SPECTRUM ALERTS",
    "color": "#a78bfa",
    "items": [
      { "status": "WARNING", "description": "Elevated login failure rate on User Authentication service (SEAL-92156)", "time_ago": "4h ago" }
    ]
  },
  {
    "category": "DEPLOYMENTS",
    "color": "#4ade80",
    "items": [
      { "status": "SUCCESS", "description": "Connect OS v3.14.2 deployed to production (SEAL-88180)", "time_ago": "22m ago" }
    ]
  }
]

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `category` | string | Category header text |
| `color` | string | Hex color for category accent |
| `items` | object[] | Activity items (max 3 per category) |
| `items[].status` | string | `"CRITICAL"` \| `"WARNING"` \| `"UNRESOLVED"` \| `"RESOLVED"` \| `"SUCCESS"` \| `"INFO"` \| `"OK"` |
| `items[].description` | string | Activity description |
| `items[].time_ago` | string | Relative timestamp |

---

## 3. Application Endpoints

### 3.1 GET /api/applications/enriched

Full application catalog with computed health, deployments, components, SLO data, and completeness scores.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/applications/enriched` |
| **Purpose** | Powers the Applications page (table/card/tree views) |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK` (single app, abbreviated):

```
[
  {
    "id": "morgan-money",
    "name": "Morgan Money",
    "seal": "16649",
    "team": "Client Data",
    "sla": "99.9%",
    "incidents": 8,
    "last": "25m ago",
    "lob": "AWM",
    "subLob": "Asset Management",
    "cto": "Jon Glennie",
    "cbt": "Kalpesh Narkhede",
    "appOwner": "Sarah Mitchell",
    "cpof": "Yes",
    "riskRanking": "Critical",
    "classification": "In House",
    "state": "Operate",
    "investmentStrategy": "Invest",
    "rto": "4",
    "productLine": "Liquidity Solutions",
    "product": "Morgan Money Platform",
    "status": "critical",
    "incidents_30d": 8,
    "components": [
      {
        "id": "mm-ui",
        "label": "MORGAN-MONEY-UI",
        "status": "healthy",
        "incidents_30d": 0,
        "indicator_type": "Synthetic",
        "slo": 99.85
      },
      {
        "id": "mm-api",
        "label": "MORGAN-MONEY-API",
        "status": "warning",
        "incidents_30d": 3,
        "indicator_type": "Service",
        "slo": 99.35
      },
      {
        "id": "mm-data-svc",
        "label": "MORGAN-MONEY-DATA-SERVICE",
        "status": "critical",
        "incidents_30d": 8,
        "indicator_type": "Service",
        "slo": 97.76
      }
    ],
    "deployments": [
      {
        "id": "gkp-cluster-na-01",
        "label": "NA-K8S-01",
        "type": "gkp",
        "datacenter": "NA-NW-C02",
        "status": "critical",
        "slo": 97.76,
        "excluded_indicators": [],
        "components": [
          {
            "id": "mm-api",
            "label": "MORGAN-MONEY-API",
            "status": "warning",
            "incidents_30d": 3,
            "indicator_type": "Service",
            "slo": 99.35
          },
          {
            "id": "mm-data-svc",
            "label": "MORGAN-MONEY-DATA-SERVICE",
            "status": "critical",
            "incidents_30d": 8,
            "indicator_type": "Service",
            "slo": 97.76
          }
        ]
      },
      {
        "id": "gap-pool-na-01",
        "label": "NA-5S",
        "type": "gap",
        "datacenter": "NA-NW-C02",
        "status": "healthy",
        "slo": 99.85,
        "excluded_indicators": [],
        "components": [
          {
            "id": "mm-ui",
            "label": "MORGAN-MONEY-UI",
            "status": "healthy",
            "incidents_30d": 0,
            "indicator_type": "Synthetic",
            "slo": 99.85
          }
        ]
      }
    ],
    "slo": {
      "target": 99.9,
      "current": 97.76,
      "error_budget": 12,
      "trend": "down",
      "burn_rate": "4.2x",
      "breach_eta": "6h",
      "status": "critical"
    },
    "completeness": {
      "has_owner": true,
      "has_sla": true,
      "has_slo": true,
      "has_rto": true,
      "has_cpof": true,
      "has_blast_radius": true,
      "score": 100
    },
    "team_ids": [1],
    "excluded_indicators": []
  }
]

```

**Top-Level App Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Slug format of app name (e.g., `"morgan-money"`) |
| `name` | string | yes | Display name |
| `seal` | string | yes | Unique SEAL identifier |
| `team` | string | yes | Primary team name |
| `sla` | string | yes | SLA target (e.g., `"99.9%"`) |
| `incidents` | integer | yes | Total incidents (30d) |
| `last` | string | yes | Last incident relative time |
| `lob` | string | yes | Line of Business |
| `subLob` | string | no | Sub-LOB (only AWM, CIB) |
| `cto` | string | yes | CTO name |
| `cbt` | string | yes | CBT name |
| `appOwner` | string | yes | Application owner |
| `cpof` | string | yes | `"Yes"` \| `"No"` — Critical Path of Failure |
| `riskRanking` | string | yes | `"Critical"` \| `"High"` \| `"Medium"` \| `"Low"` |
| `classification` | string | yes | `"In House"` \| `"Third Party"` |
| `state` | string | yes | `"Operate"` \| `"Build"` \| `"Sunset"` |
| `investmentStrategy` | string | yes | `"Invest"` \| `"Maintain"` \| `"Retire"` |
| `rto` | string | yes | Recovery Time Objective (hours) |
| `productLine` | string | yes | Product line name |
| `product` | string | yes | Product name |
| `status` | string | yes | Computed: `"critical"` \| `"warning"` \| `"healthy"` \| `"no_data"` |
| `incidents_30d` | integer | yes | Same as `incidents` |
| `components` | object[] | yes | Flat list of all components |
| `deployments` | object[] | yes | Deployment objects with nested components |
| `slo` | object | yes | SLO metrics |
| `completeness` | object | yes | Metadata completeness score |
| `team_ids` | integer[] | yes | Assigned team IDs |
| `excluded_indicators` | string[] | yes | Excluded indicator types |

**Component Object**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Component ID (e.g., `"mm-api"`) |
| `label` | string | Display label (e.g., `"MORGAN-MONEY-API"`) |
| `status` | string | Effective status (dependency-propagated) |
| `incidents_30d` | integer | Incident count |
| `indicator_type` | string | `"Process Group"` \| `"Service"` \| `"Synthetic"` |
| `slo` | number \| null | Current SLO percentage, null if no_data |

**Deployment Object**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Platform node ID or deployment override ID |
| `label` | string | Display label |
| `type` | string | Platform type: `"gap"` \| `"gkp"` \| `"ecs"` \| `"eks"` |
| `datacenter` | string | Data center identifier |
| `status` | string | Worst health of active components |
| `slo` | number \| null | Minimum SLO of active components |
| `components` | object[] | Nested component objects |
| `excluded_indicators` | string[] | Excluded indicator types at deployment level |
| `deployment_id` | string | (Override only) Deployment ID |
| `cpof` | boolean | (Override only) Critical Path of Failure |
| `rto` | number \| null | (Override only) RTO in hours |

**SLO Object**:

| Field | Type | Description |
|-------|------|-------------|
| `target` | number | SLO target percentage (e.g., `99.9`) |
| `current` | number | Current uptime percentage |
| `error_budget` | number | Remaining error budget (0-100%) |
| `trend` | string | `"up"` \| `"down"` \| `"stable"` |
| `burn_rate` | string | Error budget burn rate (e.g., `"4.2x"`) |
| `breach_eta` | string \| null | Time until SLO breach, null if safe |
| `status` | string | `"critical"` \| `"warning"` \| `"healthy"` |

---

### 3.2 GET /api/indicator-types

Available health indicator types for exclusion filtering.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/indicator-types` |
| **Purpose** | Populates indicator exclusion checkboxes in AppDetailModal |
| **Status Codes** | `200 OK` |

**Sample Response**:

```
["Process Group", "Service", "Synthetic"]

```

---

### 3.3 PUT /api/applications/{app_id}/excluded-indicators

Exclude health indicator types from status computation at the application level.

| | |
|---|---|
| **Method** | `PUT` |
| **URL** | `/api/applications/{app_id}/excluded-indicators` |
| **Purpose** | User can exclude indicator types to customize health rollup |
| **Path Params** | `app_id` — slug format (e.g., `"morgan-money"`) |
| **Status Codes** | `200 OK`, `404 Not Found` |

**Sample Request**:

```
{ "excluded_indicators": ["Synthetic"] }

```

**Sample Response** — `200 OK`:

```
{ "excluded_indicators": ["Synthetic"] }

```

---

### 3.4 PUT /api/applications/{app_id}/deployments/{dep_id}/excluded-indicators

Exclude indicator types at the deployment level.

| | |
|---|---|
| **Method** | `PUT` |
| **URL** | `/api/applications/{app_id}/deployments/{dep_id}/excluded-indicators` |
| **Purpose** | Deployment-level indicator exclusion |
| **Path Params** | `app_id` — slug, `dep_id` — deployment ID |
| **Status Codes** | `200 OK` |
| **Request/Response** | Same schema as Section 3.3. |

---

### 3.5 GET /api/applications/{app_id}/teams

Get team assignments for an application.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/applications/{app_id}/teams` |
| **Purpose** | Load assigned teams in AppDetailModal |
| **Status Codes** | `200 OK` |

**Sample Response**:

```
{ "team_ids": [1, 5, 12] }

```

---

### 3.6 PUT /api/applications/{app_id}/teams

Assign teams to an application (multi-team).

| | |
|---|---|
| **Method** | `PUT` |
| **URL** | `/api/applications/{app_id}/teams` |
| **Purpose** | Save team assignments from AppDetailModal |
| **Status Codes** | `200 OK` |

**Sample Request**:

```
{ "team_ids": [1, 5, 12] }

```

**Sample Response** — `200 OK`:

```
{ "team_ids": [1, 5, 12] }

```

---

## 4. Knowledge Graph Endpoints

### 4.1 GET /api/graph/nodes

All component service nodes in the dependency graph.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/graph/nodes` |
| **Purpose** | Provides node data for DependencyFlow graph visualization |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
[
  {
    "id": "api-gateway",
    "label": "API-GATEWAY",
    "status": "healthy",
    "team": "Platform",
    "sla": "99.99%",
    "incidents_30d": 0
  },
  {
    "id": "meridian-query",
    "label": "MERIDIAN~~SERVICE-QUERY~V1",
    "status": "critical",
    "team": "Trading",
    "sla": "99.5%",
    "incidents_30d": 7
  }
]

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique node identifier |
| `label` | string | Display label (uses `~~` for line breaks) |
| `status` | string | `"critical"` \| `"warning"` \| `"healthy"` \| `"no_data"` |
| `team` | string | Owning team name |
| `sla` | string | SLA target percentage |
| `incidents_30d` | integer | Incident count over 30 days |

---

### 4.2 GET /api/graph/dependencies/{service_id}

Forward dependency traversal — what does this service depend on?

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/graph/dependencies/{service_id}` |
| **Purpose** | Downstream dependency visualization |
| **Status Codes** | `200 OK`, `404 Not Found` |

**Sample Response** — `200 OK`:

```
{
  "root": {
    "id": "connect-portal",
    "label": "CONNECT-PORTAL",
    "status": "healthy",
    "team": "Connect Platform",
    "sla": "99.9%",
    "incidents_30d": 0
  },
  "dependencies": [
    {
      "id": "connect-cloud-gw",
      "label": "CONNECT-CLOUD-GATEWAY",
      "status": "warning",
      "team": "Connect Platform",
      "sla": "99.99%",
      "incidents_30d": 1
    }
  ],
  "edges": [
    { "source": "connect-portal", "target": "connect-cloud-gw" }
  ]
}

```

---

### 4.3 GET /api/graph/blast-radius/{service_id}

Reverse dependency traversal — what is impacted if this service fails?

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/graph/blast-radius/{service_id}` |
| **Purpose** | Blast radius impact analysis |
| **Status Codes** | `200 OK`, `404 Not Found` |

**Sample Response** — `200 OK`:

```
{
  "root": {
    "id": "payment-gateway",
    "label": "PAYMENT-GATEWAY-API",
    "status": "critical",
    "team": "Payments",
    "sla": "99.99%",
    "incidents_30d": 8
  },
  "impacted": [
    {
      "id": "meridian-order",
      "label": "MERIDIAN~~SERVICE-ORDER~V1",
      "status": "warning",
      "team": "Trading",
      "sla": "99.5%",
      "incidents_30d": 3
    }
  ],
  "edges": [
    { "source": "meridian-order", "target": "payment-gateway" }
  ]
}

```

---

### 4.4 GET /api/graph/layer-seals

Application SEALs that have knowledge graph data.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/graph/layer-seals` |
| **Purpose** | Populates the SEAL selector in GraphLayers page |
| **Status Codes** | `200 OK` |

**Sample Response** — `200 OK`:

```
[
  { "seal": "16649", "label": "Morgan Money", "component_count": 3 },
  { "seal": "35115", "label": "PANDA", "component_count": 4 },
  { "seal": "88180", "label": "Connect OS", "component_count": 6 },
  { "seal": "90176", "label": "Advisor Connect", "component_count": 10 },
  { "seal": "90215", "label": "Spectrum Portfolio Mgmt", "component_count": 14 },
  { "seal": "91001", "label": "Quantum", "component_count": 7 },
  { "seal": "81884", "label": "Order Decision Engine", "component_count": 8 },
  { "seal": "45440", "label": "Credit Card Processing Engine", "component_count": 11 },
  { "seal": "102987", "label": "AWM Entitlements (WEAVE)", "component_count": 12 },
  { "seal": "62100", "label": "Real-Time Payments Gateway", "component_count": 15 }
]

```

---

### 4.5 GET /api/graph/layers/{seal_id}

Complete multi-layer graph for a specific application SEAL. Returns four layers: components, platform, datacenter, and indicators. Includes cross-SEAL external nodes.

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/graph/layers/{seal_id}` |
| **Purpose** | Powers the LayeredDependencyFlow multi-layer graph visualization |
| **Status Codes** | `200 OK`, `404 Not Found` |

**Sample Response** — `200 OK` (abbreviated):

```
{
  "seal": "88180",
  "components": {
    "nodes": [
      {
        "id": "connect-portal",
        "label": "CONNECT-PORTAL",
        "status": "healthy",
        "team": "Connect Platform",
        "sla": "99.9%",
        "incidents_30d": 0
      }
    ],
    "edges": [
      { "source": "connect-portal", "target": "connect-cloud-gw", "direction": "bi" }
    ],
    "external_nodes": [
      {
        "id": "connect-profile-svc",
        "label": "CONNECT-SERVICE-PROFILE-SERVICE",
        "status": "warning",
        "team": "Connect Identity",
        "sla": "99.5%",
        "incidents_30d": 2,
        "external": true,
        "external_seal": "90176",
        "external_seal_label": "Advisor Connect",
        "cross_direction": "upstream"
      }
    ]
  },
  "platform": {
    "nodes": [
      {
        "id": "gap-pool-na-01",
        "label": "NA-5S",
        "type": "gap",
        "subtype": "pool",
        "datacenter": "NA-NW-C02",
        "status": "healthy"
      }
    ],
    "edges": [
      { "source": "connect-portal", "target": "gap-pool-na-01", "layer": "platform" }
    ]
  },
  "datacenter": {
    "nodes": [
      { "id": "dc-na-nw-c02", "label": "NA-NW-C02", "region": "NA", "status": "healthy" }
    ],
    "edges": [
      { "source": "gap-pool-na-01", "target": "dc-na-nw-c02", "layer": "datacenter" }
    ]
  },
  "indicators": {
    "nodes": [
      {
        "id": "dt-pg-cloud-gw",
        "label": "connect-cloud-gateway",
        "indicator_type": "Process Group",
        "health": "amber",
        "component": "connect-cloud-gw"
      }
    ],
    "edges": [
      { "source": "connect-cloud-gw", "target": "dt-pg-cloud-gw", "layer": "indicator" }
    ]
  }
}

```

**Component Edge Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Source node ID |
| `target` | string | Target node ID |
| `direction` | string | `"uni"` (one-way) or `"bi"` (bidirectional) |
| `cross_seal` | string | (Cross-SEAL edges only) Target SEAL ID |

**External Node Extra Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `external` | boolean | Always `true` |
| `external_seal` | string | SEAL ID of the external app |
| `external_seal_label` | string | Display name of external app |
| `cross_direction` | string | `"upstream"` \| `"downstream"` \| `"both"` |

| | |
|---|---|
| **Indicator Health Values** | `"green"` \| `"amber"` \| `"red"` \| `"no_data"` |

---

## 5. Team Management Endpoints

### GET /api/teams

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/teams` |
| **Purpose** | List all teams |
| **Status Codes** | `200 OK` |

```
[
  {
    "id": 1,
    "name": "Client Data",
    "emails": ["client-data@jpmchase.com", "client-data-oncall@jpmchase.com"],
    "teams_channels": ["#client-data-alerts", "#client-data-general"]
  }
]

```

### GET /api/teams/{team_id}

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/teams/{team_id}` |
| **Purpose** | Get single team |
| **Status Codes** | `200 OK`, `404 Not Found` |

### POST /api/teams

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `/api/teams` |
| **Purpose** | Create a team |
| **Status Codes** | `200 OK` |

**Sample Request**:

```
{
  "name": "New Team",
  "emails": ["team@jpmchase.com"],
  "teams_channels": ["#new-team-alerts"]
}

```

### PUT /api/teams/{team_id}

| | |
|---|---|
| **Method** | `PUT` |
| **URL** | `/api/teams/{team_id}` |
| **Purpose** | Update a team (all fields optional) |
| **Status Codes** | `200 OK`, `404 Not Found` |

### DELETE /api/teams/{team_id}

| | |
|---|---|
| **Method** | `DELETE` |
| **URL** | `/api/teams/{team_id}` |
| **Purpose** | Delete a team |
| **Status Codes** | `200 OK`, `404 Not Found` |
| **Sample Response** | `{ "ok": true }` |

**Team Object Schema**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-incrementing ID |
| `name` | string | Team display name |
| `emails` | string[] | Contact email addresses |
| `teams_channels` | string[] | MS Teams channel names |

---

## 6. Announcement Endpoints

### GET /api/announcements

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/announcements` |
| **Query Params** | `status` (open/closed), `channel` (teams/email/connect/banner), `search` |
| **Purpose** | List/filter announcements |
| **Status Codes** | `200 OK` |

### GET /api/announcements/notifications

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/announcements/notifications` |
| **Purpose** | Banner-enabled open announcements (for TopNav notification badge) |
| **Status Codes** | `200 OK` |

### GET /api/announcements/connect/weave-interfaces

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/announcements/connect/weave-interfaces` |
| **Purpose** | Available WEAVE interface targets for Connect channel |
| **Status Codes** | `200 OK` |

```
[
  { "id": 0, "ui_title": "Docusign eSign", "ui_name": "ConnectHomeEmbedDocusignWindow", "weave_function": "GWMConnectHomeView", "seal_id": "103845" }
]

```

### GET /api/announcements/connect/validate

| | |
|---|---|
| **Method** | `GET` |
| **URL** | `/api/announcements/connect/validate` |
| **Query Params** | `entities` (comma-separated), `regions` (comma-separated) |
| **Purpose** | Preview recipient count for Connect channel |
| **Status Codes** | `200 OK` |

```
{ "message": "Announcement will be sent to 2,140 EMEA Connect users" }

```

### POST /api/announcements

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `/api/announcements` |
| **Purpose** | Create announcement |
| **Status Codes** | `200 OK` |

**Sample Request**:

```
{
  "title": "Scheduled Maintenance — Morgan Money",
  "status": "ongoing",
  "severity": "standard",
  "impacted_apps": ["Morgan Money (16649)"],
  "start_time": "2026-03-01 02:00 UTC",
  "end_time": "2026-03-01 06:00 UTC",
  "description": "Planned maintenance for database migration.",
  "latest_updates": "",
  "incident_number": "CHG-2026-1200",
  "impact_type": "Planned Maintenance",
  "impact_description": "Full outage during maintenance window.",
  "header_message": "Planned downtime — Morgan Money",
  "email_recipients": ["mm-ops@jpmchase.com"],
  "category": "Maintenance",
  "region": "Global",
  "next_steps": "No action required.",
  "help_info": "Contact support on ServiceNow",
  "email_body": "<p>Planned maintenance notification.</p>",
  "channels": { "teams": true, "email": true, "connect": false, "banner": true },
  "pinned": false,
  "teams_channels": ["#mm-announcements"],
  "email_source": "Operations",
  "email_hide_status": false,
  "connect_dont_send_notification": false,
  "connect_banner_position": "in_ui",
  "connect_target_entities": [],
  "connect_target_regions": [],
  "connect_weave_interfaces": []
}

```

**Announcement Object Schema**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | integer | auto | Auto-incrementing ID |
| `title` | string | yes | Announcement title |
| `status` | string | yes | `"ongoing"` \| `"resolved"` \| `"closed"` |
| `severity` | string | yes | `"none"` \| `"standard"` \| `"major"` |
| `impacted_apps` | string[] | no | Affected applications |
| `start_time` | string | no | Start time (UTC format) |
| `end_time` | string | no | End time (UTC format) |
| `description` | string | no | Detailed description (supports HTML) |
| `latest_updates` | string | no | Most recent update text |
| `incident_number` | string | no | INC or CHG number |
| `impact_type` | string | no | Impact category |
| `impact_description` | string | no | User-facing impact description |
| `header_message` | string | no | Banner header text |
| `email_recipients` | string[] | no | Email addresses |
| `category` | string | no | `"Infrastructure"` \| `"Application"` \| `"Security"` \| `"Maintenance"` etc. |
| `region` | string | no | `"Global"` \| `"US-East"` \| `"US-West"` \| `"EU-West"` \| `"APAC"` etc. |
| `next_steps` | string | no | Next actions text |
| `help_info` | string | no | Contact/help information |
| `email_body` | string | no | HTML email body |
| `channels` | object | yes | `{ teams: bool, email: bool, connect: bool, banner: bool }` |
| `pinned` | boolean | no | Pin to top of list |
| `teams_channels` | string[] | no | MS Teams channel targets |
| `email_source` | string | no | Sender department label |
| `email_hide_status` | boolean | no | Hide status badge in email |
| `connect_dont_send_notification` | boolean | no | Suppress Connect push |
| `connect_banner_position` | string | no | `"in_ui"` \| `"top"` |
| `connect_target_entities` | string[] | no | Connect entity codes |
| `connect_target_regions` | string[] | no | Connect region filters |
| `connect_weave_interfaces` | integer[] | no | WEAVE interface IDs |
| `ann_status` | string | auto | `"open"` \| `"closed"` |
| `author` | string | auto | Creator display name |
| `date` | string | auto | Creation timestamp |

### PUT /api/announcements/{id}

| | |
|---|---|
| **Method** | `PUT` |
| **Purpose** | Update announcement (all fields optional) |
| **Status Codes** | `200 OK`, `404 Not Found` |

### PATCH /api/announcements/{id}/status

| | |
|---|---|
| **Method** | `PATCH` |
| **Purpose** | Toggle `ann_status` between open/closed |
| **Status Codes** | `200 OK`, `404 Not Found` |

### DELETE /api/announcements/{id}

| | |
|---|---|
| **Method** | `DELETE` |
| **Purpose** | Delete announcement |
| **Status Codes** | `200 OK`, `404 Not Found` |
| **Response** | `{ "ok": true }` |

---

## 7. View Central Notification Endpoints

### GET /api/vc-notifications/{view_id}

| | |
|---|---|
| **Method** | `GET` |
| **Purpose** | List notifications for a View Central dashboard |
| **Status Codes** | `200 OK` |

### POST /api/vc-notifications/{view_id}

| | |
|---|---|
| **Method** | `POST` |
| **Purpose** | Create a notification rule |
| **Status Codes** | `200 OK` |

**Sample Request**:

```
{
  "name": "Critical App Alert",
  "alert_types": ["critical", "warning"],
  "channels": { "teams": false, "email": true },
  "teams_channels": [],
  "email_recipients": ["ops@jpmchase.com"],
  "frequency": "realtime",
  "days_of_week": ["Mon", "Tue", "Wed", "Thu", "Fri"],
  "start_time": "08:00",
  "end_time": "18:00",
  "enabled": true,
  "view_filters": { "seal": ["16649"] }
}

```

**VC Notification Object Schema**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Auto-incrementing ID |
| `view_id` | string | Parent View Central ID |
| `name` | string | Notification rule name |
| `alert_types` | string[] | `"critical"` \| `"warning"` \| `"slo"` \| `"change"` \| `"deployment"` |
| `channels` | object | `{ teams: bool, email: bool }` |
| `teams_channels` | string[] | MS Teams channel targets |
| `email_recipients` | string[] | Email addresses |
| `frequency` | string | `"realtime"` \| `"daily"` \| `"weekly"` |
| `days_of_week` | string[] | Active days |
| `start_time` | string | Active window start (HH:MM) |
| `end_time` | string | Active window end (HH:MM) |
| `enabled` | boolean | Notification active state |
| `view_filters` | object | Scoping filters (same keys as dashboard filters) |
| `created_at` | string | ISO 8601 timestamp |
| `updated_at` | string | ISO 8601 timestamp |

### PUT /api/vc-notifications/{view_id}/{notif_id}

| | |
|---|---|
| **Method** | `PUT` |
| **Purpose** | Update a notification rule |
| **Status Codes** | `200 OK`, `404 Not Found` |

### PATCH /api/vc-notifications/{view_id}/{notif_id}/toggle

| | |
|---|---|
| **Method** | `PATCH` |
| **Purpose** | Toggle enabled/disabled |
| **Status Codes** | `200 OK`, `404 Not Found` |

### DELETE /api/vc-notifications/{view_id}/{notif_id}

| | |
|---|---|
| **Method** | `DELETE` |
| **Purpose** | Delete a notification rule |
| **Status Codes** | `200 OK`, `404 Not Found` |
| **Response** | `{ "ok": true }` |

### POST /api/vc-notifications/{view_id}/{notif_id}/test

| | |
|---|---|
| **Method** | `POST` |
| **Purpose** | Send test email immediately |
| **Status Codes** | `200 OK`, `400 Bad Request`, `404 Not Found` |
| **Response** | `{ "ok": true, "detail": "Test email queued to 1 recipients" }` |

---

## 8. AURA AI Chat Endpoint

### POST /api/aura/chat

Streams AI-generated responses via **Server-Sent Events (SSE)**.

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `/api/aura/chat` |
| **Purpose** | AURA AI assistant chat interface |
| **Status Codes** | `200 OK` (SSE stream) |

**Sample Request**:

```
{
  "message": "What is the current health status of Morgan Money?",
  "conversation_id": "conv-abc123",
  "attachments": [],
  "context": {
    "current_page": "dashboard",
    "active_filters": { "lob": ["AWM"] }
  }
}

```

**SSE Event Protocol**:

| Event | Payload | Description |
|-------|---------|-------------|
| `meta` | `{ message_id, timestamp }` | Sent first — conversation metadata |
| `block` | `{ type, data }` | Content block (see types below) |
| `followups` | `["question1", "question2"]` | Suggested follow-up prompts |
| `done` | `{}` | Stream complete signal |

**Content Block Types**:

| Type | Data Schema | Description |
|------|------------|-------------|
| `text` | `string` | Markdown-formatted text response |
| `metric_cards` | `[{ label, value, color, trend, icon, sparkline }]` | KPI card array |
| `status_list` | `{ title, data: [{ name, status, detail, seal }] }` | RAG status list |
| `table` | `{ title, data: { columns, rows } }` | Tabular data |
| `bar_chart` | `{ title, data: { bars, xKey, yKey, unit } }` | Bar chart |
| `line_chart` | `{ title, data: { series, stats, points } }` | Line/trend chart |
| `pie_chart` | `{ title, data: { slices, trend } }` | Pie/donut chart |
| `recommendations` | `[{ priority, text, impact }]` | Action items (priority: high/medium/low) |

**Sample SSE Response**:

```
event: meta
data: {"message_id":"abc-123","timestamp":"2026-03-02T10:30:00Z"}

event: block
data: {"type":"text","data":"Here's the current incident analysis."}

event: block
data: {"type":"metric_cards","data":[{"label":"Active P1s","value":2,"color":"#f44336","trend":-33,"icon":"error","sparkline":[5,4,6,3,4,3,2]}]}

event: block
data: {"type":"recommendations","data":[{"priority":"high","text":"Scale database connection pool","impact":"Reduces timeouts by ~60%"}]}

event: followups
data: ["What is the blast radius?","Show me MTTR trends"]

event: done
data: {}

```

---

## 9. Contact / Messaging Endpoint

### POST /api/contact/send

Send notification messages to teams/individuals via configured channels.

| | |
|---|---|
| **Method** | `POST` |
| **URL** | `/api/contact/send` |
| **Purpose** | Contact team owners from AppDetailModal |
| **Status Codes** | `200 OK` |

**Sample Request**:

```
{
  "channels": { "email": true, "teams": false },
  "email_recipients": ["client-data@jpmchase.com", "client-data-oncall@jpmchase.com"],
  "teams_channels": [],
  "subject": "[Morgan Money] Contact Message",
  "email_body": "<p>Please investigate the NAV calculation timeout.</p>",
  "message": "Please investigate the NAV calculation timeout.",
  "app_name": "Morgan Money"
}

```

**Sample Response** — `200 OK`:

```
{
  "status": "sent",
  "channels_sent": ["email"],
  "message_preview": "Please investigate the NAV calculation timeout.",
  "email_status": { "status": "sent" }
}

```

**Field Definitions**:

| Field | Type | Description |
|-------|------|-------------|
| `channels` | object | `{ email: bool, teams: bool }` |
| `email_recipients` | string[] | Target email addresses |
| `teams_channels` | string[] | MS Teams channel targets |
| `subject` | string | Email subject line |
| `email_body` | string | HTML email body |
| `message` | string | Plain text message |
| `app_name` | string | Application context for subject |

---

## 10. Future Endpoints (Not Yet Built)

These endpoints need to be created to replace hardcoded frontend data.

### 10.1 Incident Zero Endpoints

| Method | URL | Purpose | Currently Mocked In |
|--------|-----|---------|---------------------|
| GET | `/api/incident-zero/error-budgets` | Error budget status for monitored services | `IncidentZero.jsx` — `ERROR_BUDGET_SERVICES` |
| GET | `/api/incident-zero/burn-rate-alerts` | Active burn rate alerts | `IncidentZero.jsx` — `BURN_RATE_ALERTS` |
| GET | `/api/incident-zero/timeline` | Prevention activity timeline | `IncidentZero.jsx` — `TIMELINE` |
| GET | `/api/incident-zero/scorecard` | Prevention effectiveness metrics | `IncidentZero.jsx` — `PREVENTION_SCORECARD` |

**GET /api/incident-zero/error-budgets** — Sample Response:

```
[
  {
    "label": "PAYMENT-GATEWAY-API",
    "budget": 12,
    "burnRate": "4.2x",
    "breachEta": "6h",
    "status": "critical",
    "sla": "99.99%",
    "incidents30d": 8
  }
]

```

**GET /api/incident-zero/scorecard** — Sample Response:

```
{
  "p1s_prevented": 7,
  "avg_lead_time": "4h",
  "auto_mitigated": 12,
  "budget_saved": "34%"
}

```

### 10.2 Customer Journey Endpoints

| Method | URL | Purpose | Currently Mocked In |
|--------|-----|---------|---------------------|
| GET | `/api/journeys` | List available customer journeys | `CustomerJourney.jsx` — `JOURNEYS` |
| GET | `/api/journeys/{journey_id}/steps` | Step-by-step health for a journey | `CustomerJourney.jsx` — `JOURNEYS` |

**GET /api/journeys** — Sample Response:

```
[
  {
    "id": "trade-execution",
    "name": "Trade Execution",
    "status": "critical",
    "step_count": 6,
    "critical_steps": 3,
    "warning_steps": 2
  }
]

```

**GET /api/journeys/{journey_id}/steps** — Sample Response:

```
{
  "id": "trade-execution",
  "name": "Trade Execution",
  "status": "critical",
  "steps": [
    {
      "step": "Authentication",
      "service": "AUTH-SERVICE-V2",
      "status": "healthy",
      "latency": "42ms",
      "errorRate": "0.0%"
    },
    {
      "step": "Market Data Fetch",
      "service": "MERIDIAN SERVICE-QUERY V1",
      "status": "critical",
      "latency": "3200ms",
      "errorRate": "12.4%"
    }
  ]
}

```

### 10.3 SLO Agent Endpoints

| Method | URL | Purpose | Currently Mocked In |
|--------|-----|---------|---------------------|
| GET | `/api/slo-agent/services` | SLO health table | `SloAgent.jsx` — `SERVICES` |
| GET | `/api/slo-agent/actions` | Pending AI remediation actions | `SloAgent.jsx` — `AGENT_ACTIONS` |
| POST | `/api/slo-agent/actions/{id}/approve` | Approve action | Frontend-only |
| POST | `/api/slo-agent/actions/{id}/dismiss` | Dismiss action | Frontend-only |
| GET | `/api/slo-agent/activity` | Agent activity log | `SloAgent.jsx` — `AGENT_ACTIVITY` |
| GET | `/api/slo-agent/scorecard` | Agent performance metrics | `SloAgent.jsx` — `SCORECARD` |

**GET /api/slo-agent/services** — Sample Response:

```
[
  {
    "id": "payment-gateway",
    "label": "PAYMENT-GATEWAY-API",
    "target": 99.99,
    "current": 99.84,
    "budget": 12,
    "trend": "down",
    "status": "critical"
  }
]

```

**GET /api/slo-agent/actions** — Sample Response:

```
[
  {
    "id": 1,
    "service": "PAYMENT-GATEWAY-API",
    "action": "Scale database connection pool from 50 → 100 connections",
    "reason": "Error budget at 12% with accelerating burn rate.",
    "risk": "low",
    "status": "pending_approval",
    "time": "2m ago"
  }
]

```

### 10.4 Search & Filter Endpoints

| Method | URL | Purpose | Currently Mocked In |
|--------|-----|---------|---------------------|
| GET | `/api/apps` | Full application inventory | `appData.js` — `APPS` |
| GET | `/api/filters` | Filter field definitions and options | `appData.js` — `FILTER_FIELDS` |

**GET /api/filters** — Sample Response:

```
{
  "fields": [
    { "key": "seal", "label": "App" },
    { "key": "lob", "label": "LOB" },
    { "key": "subLob", "label": "Sub LOB" },
    { "key": "cto", "label": "CTO" },
    { "key": "cbt", "label": "CBT" }
  ],
  "groups": [
    { "label": "Taxonomy", "keys": ["lob", "subLob", "seal"] },
    { "label": "People", "keys": ["cto", "cbt", "appOwner"] }
  ],
  "options": {
    "lob": ["AWM", "CCB", "CDAO", "CIB", "CT", "EP", "IP"],
    "cpof": ["Yes", "No"],
    "riskRanking": ["Critical", "High", "Medium", "Low"]
  },
  "subLobMap": {
    "AWM": ["Asset Management", "AWM Shared", "Global Private Bank"],
    "CIB": ["Digital Platform and Services", "Global Banking", "Markets", "Payments"]
  },
  "sealDisplay": {
    "16649": "Morgan Money - 16649",
    "90176": "Advisor Connect - 90176"
  }
}

```

---

## 11. File Mapping

### Frontend Components → API Endpoints

| Component File | Endpoint(s) Called | Trigger |
|----------------|-------------------|---------|
| `pages/Dashboard.jsx` | All Section 2 endpoints | On page load + filter change + auto-refresh |
| `components/SummaryCards.jsx` | `/api/health-summary` | Props from Dashboard |
| `components/AIHealthPanel.jsx` | `/api/ai-analysis` | Props from Dashboard |
| `components/RegionalStatus.jsx` | `/api/regional-status` | Props from Dashboard |
| `components/CriticalApps.jsx` | `/api/critical-apps` | Props from Dashboard |
| `components/WarningApps.jsx` | `/api/warning-apps` | Props from Dashboard |
| `components/IncidentTrends.jsx` | `/api/incident-trends` | Props from Dashboard |
| `components/ActiveIncidentsPanel.jsx` | `/api/active-incidents` | Props from Dashboard |
| `components/FrequentIncidents.jsx` | `/api/frequent-incidents` | Props from Dashboard |
| `components/RecentActivities.jsx` | `/api/recent-activities` | Props from Dashboard |
| `pages/Applications.jsx` | `/api/applications/enriched`, `/api/teams` | On page load |
| `components/AppDetailModal.jsx` | `/api/applications/{id}/teams` (PUT), `/api/applications/{id}/excluded-indicators` (PUT) | Button click (Save) |
| `components/DeploymentDetailModal.jsx` | `/api/applications/{id}/deployments/{depId}/excluded-indicators` (PUT) | Button click (Save) |
| `components/ContactModal.jsx` | `/api/contact/send` (POST) | Form submission |
| `pages/GraphLayers.jsx` | `/api/graph/layer-seals`, `/api/graph/layers/{seal_id}` | On load + SEAL selection |
| `components/DependencyFlow.jsx` | `/api/graph/dependencies/{id}`, `/api/graph/blast-radius/{id}` | Node click |
| `pages/Announcements.jsx` | `/api/announcements` (GET/POST/PUT/PATCH/DELETE), `/api/announcements/notifications`, `/api/announcements/connect/weave-interfaces`, `/api/announcements/connect/validate` | Page load, form submission |
| `pages/Teams.jsx` | `/api/teams` (GET/POST/PUT/DELETE) | Page load, CRUD actions |
| `aura/AuraChatContext.jsx` | `/api/aura/chat` (POST) | User sends message |
| `view-central/ViewCentralDashboard.jsx` | `/api/vc-notifications/{viewId}` (GET/POST/PUT/DELETE) | Notification management |
| `pages/IncidentZero.jsx` | *(No API yet — hardcoded data)* | — |
| `pages/CustomerJourney.jsx` | *(No API yet — hardcoded data)* | — |
| `pages/SloAgent.jsx` | *(No API yet — hardcoded data)* | — |

### Frontend Utilities → Data Functions

| Utility File | Purpose | Used By |
|-------------|---------|---------|
| `utils/buildFilterQueryString.js` | Converts `activeFilters` → query string | All API-calling components |
| `FilterContext.jsx` | Global filter state, cascading logic, search suggestions | SearchFilterPopover, ScopeBar, Dashboard |
| `AuthContext.jsx` | Role-based access (admin/viewer) | TopNav, Announcements, Admin, Links |
| `RefreshContext.jsx` | Auto-refresh interval (30s–5m) | Dashboard, Applications |
| `ThemeContext.jsx` | Dark/light mode toggle | All components |
| `tenant/TenantContext.jsx` | Multi-tenant switching + defaults | TopNav, FilterContext, Profile |
| `utils/profileStorage.js` | User profile persistence (localStorage) | Profile, AuthContext |
| `utils/linksStorage.js` | Custom links persistence (localStorage) | Links page |
| `tenant/tenantStorage.js` | Tenant config persistence (localStorage) | Admin, TenantContext |
| `view-central/viewCentralStorage.js` | View Central persistence (localStorage) | ViewCentralListing, ViewCentralDashboard |
| `view-central/widgetRegistry.js` | Widget component registry (13 widgets) | ViewCentralDashboard |
| `data/appData.js` | Static app data, filter fields, helpers | FilterContext, SearchFilterPopover |

### Backend Files

| File | Purpose | Key Exports |
|------|---------|-------------|
| `backend/main.py` | FastAPI app — all endpoints, mock data, AURA scenarios | All API routes |
| `backend/apps_registry.py` | 81-app registry with full metadata | `APPS_REGISTRY` list |

---

## 12. Database Schemas

The following schemas represent the data models needed to replace the current in-memory mock data with a persistent database.

### applications

Primary application catalog — source of truth for all app metadata.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `seal` | VARCHAR(10) | PK | NO | Unique SEAL identifier |
| `name` | VARCHAR(255) | | NO | Application display name |
| `team` | VARCHAR(100) | | NO | Primary team name |
| `sla` | VARCHAR(10) | | NO | SLA target (e.g., "99.9%") |
| `incidents` | INTEGER | | NO | 30-day incident count |
| `last_incident` | VARCHAR(20) | | YES | Relative last incident time |
| `lob` | VARCHAR(10) | | NO | Line of Business code |
| `sub_lob` | VARCHAR(50) | | YES | Sub-LOB (AWM, CIB only) |
| `cto` | VARCHAR(100) | | NO | CTO name |
| `cbt` | VARCHAR(100) | | NO | CBT name |
| `app_owner` | VARCHAR(100) | | NO | Application owner |
| `cpof` | VARCHAR(3) | | NO | "Yes" or "No" |
| `risk_ranking` | VARCHAR(10) | | NO | Critical/High/Medium/Low |
| `classification` | VARCHAR(20) | | NO | In House/Third Party |
| `state` | VARCHAR(10) | | NO | Operate/Build/Sunset |
| `investment_strategy` | VARCHAR(10) | | NO | Invest/Maintain/Retire |
| `rto` | VARCHAR(10) | | NO | RTO in hours |
| `product_line` | VARCHAR(100) | | NO | Product line name |
| `product` | VARCHAR(100) | | NO | Product name |
| `region` | VARCHAR(10) | | YES | Default: "NA" |
| `incidents_today` | INTEGER | | YES | Today's incident count |
| `recurring_30d` | INTEGER | | YES | 30-day recurring count |
| `p1_30d` | INTEGER | | YES | 30-day P1 count |
| `p2_30d` | INTEGER | | YES | 30-day P2 count |
| `created_at` | TIMESTAMP | | NO | Record creation time |
| `updated_at` | TIMESTAMP | | NO | Last update time |

**Sample Row**:

| seal | name | lob | sub_lob | cto | status | sla | rto |
|------|------|-----|---------|-----|--------|-----|-----|
| 16649 | Morgan Money | AWM | Asset Management | Jon Glennie | critical | 99.9% | 4 |
| 90176 | Advisor Connect | AWM | Global Private Bank | Gitanjali Nistala | warning | 99.9% | 4 |

---

### components

Service components in the knowledge graph.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | VARCHAR(50) | PK | NO | Unique component ID |
| `label` | VARCHAR(100) | | NO | Display label |
| `status` | VARCHAR(10) | | NO | healthy/warning/critical/no_data |
| `team` | VARCHAR(100) | | NO | Owning team |
| `sla` | VARCHAR(10) | | NO | SLA target |
| `incidents_30d` | INTEGER | | NO | 30-day incident count |
| `indicator_type` | VARCHAR(20) | | NO | Process Group/Service/Synthetic |

**Sample Rows**:

| id | label | status | team | sla | incidents_30d | indicator_type |
|----|-------|--------|------|-----|---------------|----------------|
| mm-ui | MORGAN-MONEY-UI | healthy | Client Data | 99.9% | 0 | Synthetic |
| mm-api | MORGAN-MONEY-API | warning | Client Data | 99.5% | 3 | Service |
| mm-data-svc | MORGAN-MONEY-DATA-SERVICE | critical | Client Data | 99.9% | 8 | Service |

---

### component_dependencies

Directed edges between components (source DEPENDS ON target).

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `source_id` | VARCHAR(50) | PK, FK → components.id | NO | Source component |
| `target_id` | VARCHAR(50) | PK, FK → components.id | NO | Target component |
| `bidirectional` | BOOLEAN | | NO | True if communication flows both ways |

**Sample Rows**:

| source_id | target_id | bidirectional |
|-----------|-----------|---------------|
| mm-ui | mm-api | false |
| mm-api | mm-data-svc | false |
| connect-portal | connect-cloud-gw | true |

---

### seal_components

Maps applications (SEALs) to their component nodes.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `seal` | VARCHAR(10) | PK, FK → applications.seal | NO | Application SEAL ID |
| `component_id` | VARCHAR(50) | PK, FK → components.id | NO | Component ID |

**Sample Rows**:

| seal | component_id |
|------|-------------|
| 16649 | mm-ui |
| 16649 | mm-api |
| 16649 | mm-data-svc |
| 88180 | connect-portal |
| 88180 | connect-cloud-gw |

---

### deployments

Deployment overrides for applications with known deployment data.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | VARCHAR(20) | PK | NO | Deployment ID |
| `app_slug` | VARCHAR(100) | FK → applications (derived) | NO | Application slug |
| `seal` | VARCHAR(10) | FK → applications.seal | NO | Application SEAL |
| `label` | VARCHAR(200) | | NO | Deployment display name |
| `cpof` | BOOLEAN | | NO | Critical Path of Failure |
| `rto` | INTEGER | | YES | RTO in hours (null = N/A) |

**Sample Rows**:

| id | app_slug | seal | label | cpof | rto |
|----|----------|------|-------|------|-----|
| 112224 | connect-os | 88180 | Connect OS Critical Apps AWS - Global | true | 4 |
| 111848 | connect-os | 88180 | Connect OS Mobile AWS - Global | false | 8 |
| 64958 | spectrum-portfolio-management-(equities) | 90215 | Spectrum PI - Equities Deployment | true | 4 |

---

### deployment_components

Maps deployments to their component nodes.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `deployment_id` | VARCHAR(20) | PK, FK → deployments.id | NO | Deployment ID |
| `component_id` | VARCHAR(50) | PK, FK → components.id | NO | Component ID |

**Sample Rows**:

| deployment_id | component_id |
|--------------|-------------|
| 112224 | connect-cloud-gw |
| 112224 | connect-auth-svc |
| 112224 | connect-portal |
| 64958 | spieq-ui-service |
| 64958 | spieq-api-gateway |

---

### platform_nodes

Infrastructure platform resources.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | VARCHAR(30) | PK | NO | Platform node ID |
| `label` | VARCHAR(20) | | NO | Display label |
| `type` | VARCHAR(5) | | NO | gap/gkp/ecs/eks |
| `subtype` | VARCHAR(10) | | NO | pool/cluster/service |
| `datacenter` | VARCHAR(20) | FK → data_centers.label | NO | Data center code |
| `status` | VARCHAR(10) | | NO | healthy/warning/critical |

**Sample Rows**:

| id | label | type | subtype | datacenter | status |
|----|-------|------|---------|------------|--------|
| gap-pool-na-01 | NA-5S | gap | pool | NA-NW-C02 | healthy |
| gkp-cluster-na-01 | NA-K8S-01 | gkp | cluster | NA-NW-C02 | critical |
| ecs-na-01 | NA-ECS-01 | ecs | service | NA-NW-C02 | healthy |

---

### data_centers

Geographic data center locations.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | VARCHAR(20) | PK | NO | Data center ID |
| `label` | VARCHAR(20) | UNIQUE | NO | Display label |
| `region` | VARCHAR(5) | | NO | NA/EMEA/APAC |
| `status` | VARCHAR(10) | | NO | healthy/warning/critical |

**Sample Rows**:

| id | label | region | status |
|----|-------|--------|--------|
| dc-na-nw-c02 | NA-NW-C02 | NA | healthy |
| dc-ap-hk-c02 | AP-HK-C02 | APAC | healthy |
| dc-em-ch-lausanne | EM-CH-Lausanne | EMEA | healthy |

---

### component_platform_edges

Maps components to their hosting platform nodes.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `component_id` | VARCHAR(50) | PK, FK → components.id | NO | Component ID |
| `platform_id` | VARCHAR(30) | PK, FK → platform_nodes.id | NO | Platform node ID |

---

### health_indicators

Health monitoring indicators from Dynatrace or similar.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | VARCHAR(50) | PK | NO | Indicator ID |
| `label` | VARCHAR(50) | | NO | Display name |
| `indicator_type` | VARCHAR(20) | | NO | Process Group/Service/Synthetic |
| `health` | VARCHAR(10) | | NO | green/amber/red/no_data |
| `component_id` | VARCHAR(50) | FK → components.id | NO | Parent component |

**Sample Rows**:

| id | label | indicator_type | health | component_id |
|----|-------|----------------|--------|-------------|
| dt-pg-mm-ui | morgan-money-ui | Process Group | green | mm-ui |
| dt-svc-mm-api | MorganMoneyAPI | Service | amber | mm-api |
| dt-pg-mm-data | morgan-money-data | Process Group | red | mm-data-svc |
| dt-syn-mm-data | Data Lookup | Synthetic | red | mm-data-svc |

---

### teams

Support team definitions.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | SERIAL | PK | NO | Auto-increment ID |
| `name` | VARCHAR(100) | UNIQUE | NO | Team display name |
| `emails` | TEXT[] | | YES | Contact email addresses |
| `teams_channels` | TEXT[] | | YES | MS Teams channel names |

**Sample Rows**:

| id | name | emails | teams_channels |
|----|------|--------|----------------|
| 1 | Client Data | {client-data@jpmchase.com} | {#client-data-alerts} |
| 2 | Spectrum Core | {spectrum-core@jpmchase.com} | {#spectrum-core-alerts} |

---

### app_team_assignments

Many-to-many: applications to teams.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `app_slug` | VARCHAR(100) | PK | NO | Application slug |
| `team_id` | INTEGER | PK, FK → teams.id | NO | Team ID |

---

### app_excluded_indicators

Indicator types excluded from health computation at app level.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `app_slug` | VARCHAR(100) | PK | NO | Application slug |
| `indicator_type` | VARCHAR(20) | PK | NO | Process Group/Service/Synthetic |

---

### deployment_excluded_indicators

Indicator types excluded at deployment level.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `app_slug` | VARCHAR(100) | PK | NO | Application slug |
| `deployment_id` | VARCHAR(20) | PK | NO | Deployment ID |
| `indicator_type` | VARCHAR(20) | PK | NO | Indicator type |

---

### announcements

Multi-channel notification announcements.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | SERIAL | PK | NO | Auto-increment ID |
| `title` | VARCHAR(255) | | NO | Announcement title |
| `status` | VARCHAR(10) | | NO | ongoing/resolved/closed |
| `severity` | VARCHAR(10) | | NO | none/standard/major |
| `impacted_apps` | TEXT[] | | YES | Affected application names |
| `start_time` | VARCHAR(30) | | YES | Start time string |
| `end_time` | VARCHAR(30) | | YES | End time string |
| `description` | TEXT | | YES | Full description (HTML) |
| `latest_updates` | TEXT | | YES | Latest update text |
| `incident_number` | VARCHAR(20) | | YES | INC/CHG reference |
| `impact_type` | VARCHAR(50) | | YES | Impact category |
| `impact_description` | TEXT | | YES | Impact description |
| `header_message` | VARCHAR(255) | | YES | Banner header text |
| `email_recipients` | TEXT[] | | YES | Email addresses |
| `category` | VARCHAR(30) | | YES | Category label |
| `region` | VARCHAR(20) | | YES | Region label |
| `next_steps` | TEXT | | YES | Next actions |
| `help_info` | TEXT | | YES | Contact/help info |
| `email_body` | TEXT | | YES | HTML email body |
| `channels` | JSONB | | NO | `{teams, email, connect, banner}` |
| `pinned` | BOOLEAN | | NO | Pin to top |
| `teams_channels` | TEXT[] | | YES | MS Teams channels |
| `email_source` | VARCHAR(50) | | YES | Sender department |
| `email_hide_status` | BOOLEAN | | YES | Hide status in email |
| `connect_dont_send_notification` | BOOLEAN | | YES | Suppress Connect push |
| `connect_banner_position` | VARCHAR(10) | | YES | in_ui/top |
| `connect_target_entities` | TEXT[] | | YES | Entity codes |
| `connect_target_regions` | TEXT[] | | YES | Region filters |
| `connect_weave_interfaces` | INTEGER[] | | YES | WEAVE interface IDs |
| `ann_status` | VARCHAR(10) | | NO | open/closed |
| `author` | VARCHAR(100) | | NO | Creator name |
| `created_at` | TIMESTAMP | | NO | Creation time |

---

### vc_notifications

View Central notification rules.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | SERIAL | PK | NO | Auto-increment ID |
| `view_id` | VARCHAR(50) | | NO | Parent View Central ID |
| `name` | VARCHAR(100) | | NO | Rule name |
| `alert_types` | TEXT[] | | NO | critical/warning/slo/change/deployment |
| `channels` | JSONB | | NO | `{teams, email}` |
| `teams_channels` | TEXT[] | | YES | MS Teams channels |
| `email_recipients` | TEXT[] | | YES | Email addresses |
| `frequency` | VARCHAR(10) | | NO | realtime/daily/weekly |
| `days_of_week` | TEXT[] | | YES | Active days |
| `start_time` | VARCHAR(5) | | YES | HH:MM start |
| `end_time` | VARCHAR(5) | | YES | HH:MM end |
| `enabled` | BOOLEAN | | NO | Active state |
| `view_filters` | JSONB | | YES | Scoping filters |
| `created_at` | TIMESTAMP | | NO | Creation time |
| `updated_at` | TIMESTAMP | | NO | Last update |

---

### vc_alert_log

Alert dispatch tracking for deduplication.

| Column | Type | PK/FK | Nullable | Description |
|--------|------|-------|----------|-------------|
| `id` | SERIAL | PK | NO | Auto-increment ID |
| `notification_id` | INTEGER | FK → vc_notifications.id | NO | Notification rule |
| `alert_type` | VARCHAR(10) | | NO | critical/warning/slo |
| `app_seal` | VARCHAR(10) | | NO | Application SEAL |
| `sent_at` | TIMESTAMP | | NO | Alert dispatch time |

---

### Entity Relationship Diagram

```
applications (seal PK)
    │
    ├── 1:N ── seal_components ──── N:1 ── components (id PK)
    │                                         │
    │                                         ├── 1:N ── component_dependencies (source_id, target_id)
    │                                         ├── 1:N ── component_platform_edges ── N:1 ── platform_nodes (id PK)
    │                                         │                                                │
    │                                         │                                                └── N:1 ── data_centers (id PK)
    │                                         └── 1:N ── health_indicators (id PK)
    │
    ├── 1:N ── deployments (id PK)
    │              └── 1:N ── deployment_components ── N:1 ── components
    │
    ├── N:M ── app_team_assignments ── N:1 ── teams (id PK)
    │
    ├── 1:N ── app_excluded_indicators
    │
    └── 1:N ── deployment_excluded_indicators

announcements (id PK)   [standalone]

vc_notifications (id PK)
    └── 1:N ── vc_alert_log (id PK)

```

---

*Generated for the Unified Observability Portal — `obs-dashboard`*
