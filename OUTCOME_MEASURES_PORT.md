# Porting Outcome Measures

Files and changes needed to add the Outcome Measures tab to a clean UOP deployment.

## New files (copy wholesale)

| Repo | File | Description |
|------|------|-------------|
| uop-api | `app/mock_data/outcome_measures_data.py` | Mock data |
| uop-api | `app/routers/outcome_measures.py` | API endpoints |
| uop-ui | `src/pages/OutcomeMeasures.jsx` | Page component |
| uop-ui | `src/components/outcome-measures/ExecutiveKpiBar.jsx` | AURA insights + 3 hero cards (Adoption, SRE Coverage, Results) with baseline toggle |
| uop-ui | `src/components/outcome-measures/SectionTabs.jsx` | Tab bar for detail sections |
| uop-ui | `src/components/outcome-measures/SectionKpiCards.jsx` | Section-specific KPI card grid |
| uop-ui | `src/components/outcome-measures/OutcomeTrendChart.jsx` | 12-month trend line charts |

## Page structure

```
AURA Outcome Insights (auto-generated verbal summary per bucket + recommendations)

Executive Summary header + app count chip + baseline period toggle (3m/6m/12m/YTD)

Hero KPI Bar (3 cards — Adoption / SRE Coverage / Results)
  └── Each card: bucket subtitle (uppercase) + story title + KPI sub-cards
  └── Each KPI: label, value+unit, % change badge, baseline, sparkline (2-col grid)

Detail Metrics (collapsed by default, expand on click or tab select)
  └── Section Tabs (Adoption | SRE Coverage | Results)
  └── SectionKpiCards (detail metrics filtered from summary-only, same 2-col grid layout)
  └── OutcomeTrendChart (12-month multi-metric line chart with toggle buttons)
```

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/outcome-measures/summary` | Executive KPIs + section list + month labels |
| GET | `/api/outcome-measures/section/{id}` | Section-specific aggregated metrics |

## Edits to existing files

### uop-api — `app/routers/applications.py`

Add filter params to `/api/applications/enriched` so top-nav filters propagate to sidebar tree:

```python
from fastapi import APIRouter, Query
from app.services.enrichment import get_enriched_applications, _filter_dashboard_apps

@router.get("/api/applications/enriched")
def get_enriched(
    lob: list[str] | None = Query(None), sub_lob: list[str] | None = Query(None, alias="subLob"),
    cto: list[str] | None = Query(None), cbt: list[str] | None = Query(None),
    seal: list[str] | None = Query(None), status: list[str] | None = Query(None),
    search: str | None = Query(None),
):
    if any([lob, sub_lob, cto, cbt, seal, status, search]):
        return _filter_dashboard_apps(lob, sub_lob, cto, cbt, seal, status, search)
    return get_enriched_applications()
```

### uop-api — `app/main.py`

Add to router imports:

```python
from app.routers import (
    ...
    outcome_measures,
    ...
)
```

Register the router:

```python
app.include_router(outcome_measures.router)
```

### uop-ui — `src/App.jsx`

Add import:

```jsx
import OutcomeMeasures from './pages/OutcomeMeasures'
```

Add route (inside `<Routes>`):

```jsx
<Route path="/outcome-measures" element={<OutcomeMeasures />} />
```

### uop-ui — `src/components/TopNav.jsx`

Add icon import:

```jsx
import AssessmentIcon from '@mui/icons-material/Assessment'
```

Add entry to nav items array:

```js
{ label: 'Outcome Measures', path: '/outcome-measures', Icon: AssessmentIcon, desc: 'SRE outcome metrics & trends' },
```

### uop-ui — `src/components/BrochureModal.jsx`

Add icon import:

```jsx
import AssessmentIcon from '@mui/icons-material/Assessment'
```

Add entry to `FEATURES` array:

```js
{
  icon: AssessmentIcon,
  color: '#8b5cf6',
  title: 'Outcome Measures',
  gif: 'outcome-measures.gif',
  desc: 'SRE outcome metrics across 3 sections — 12-month trend charts, baseline comparisons, and hero KPI cards.',
},
```

## Filter architecture

```
TopNav SearchFilterPopover
  → updates FilterContext (LOB, Sub-LOB, CTO, CBT, search)
  → OutcomeMeasures page listens via useFilters()
  → buildFilterQueryString() creates ?lob=AWM&...
  → fetchApps(/api/applications/enriched?lob=AWM) returns filtered apps
  → AppTreeSidebar receives filtered apps as prop (passive consumer)
  → Tree selection further narrows via seal= params
```

## Full Metric Coverage

All metrics mapped to the Outcome Measures Plan spreadsheet.

### Adoption (9 metrics)

| # | Spreadsheet Name | Metric Key | Unit | View |
|---|---|---|---|---|
| 1 | Total number of users by week | `total_users_week` | users/wk | Summary |
| 2 | Total volume of prompt executions | `mcp_requests` | req/mo | Summary |
| 3 | MCP: Volume of requests per MCP server / FinOps | `mcp_requests` | req/mo | Detail |
| 4 | UOP Chat volume of prompts | `uop_chat_prompts` | prompts/mo | Detail |
| 5 | Clicks by feature (Blast Radius, CUJ, SLO, AURA) | `clicks_*` | clicks/mo | Detail |
| 6 | Usage: Prompt executions in DevGPT (Zero-Touch M&O MCP) | `devgpt_executions` | exec/mo | Detail |
| 7 | Usage: Volume of simulations executed (AI Chaos Simulator) | `simulation_executions` | runs/mo | Detail |

### SRE Coverage (4 metrics)

| # | Spreadsheet Name | Metric Key | Unit | View |
|---|---|---|---|---|
| 1 | Dynatrace Coverage | `dynatrace_coverage` | % | Summary |
| 2 | Golden Signals Coverage | `golden_signals_coverage` | % | Summary |
| 3 | SRE Telemetry Coverage (SLOs) | `sre_telemetry_coverage` | % | Detail |
| 4 | UOP Coverage | `uop_coverage` | % | Detail |

### Results (23 metrics)

| # | Spreadsheet Name | Metric Key | Unit | View |
|---|---|---|---|---|
| 1 | Incidents avoided -> Code Updates in DevGPT | `incidents_avoided` | count | Detail |
| 2 | Incidents avoided — UAT | `incidents_avoided_uat` | count | Detail |
| 3 | Incidents avoided — Prod | `incidents_avoided_prod` | count | Detail |
| 4 | Anomalies detected per 100 changes | `anomaly_rate` | /100 chg | Summary |
| 5 | Change Aware Anomaly Rate | `change_aware_anomaly_rate` | /100 chg | Detail |
| 6 | AI Driven Impact Duration | `ai_impact_duration` | min | Summary |
| 7 | Alert Response Time | `alert_response_time` | min | Summary |
| 8 | Response Type: AIOpsmode/UOP/AURA | `response_type_breakdown` | count | Detail |
| 9 | Response Time by Type | `response_time_by_type` | min | Summary |
| 10 | Incident/Tickets Trending | `p1_incidents` | count | Summary |
| 11 | Incidents by P1/P2/P3/P4/P5 | `p1_incidents`..`p5_incidents` | count | Detail |
| 12 | MTTR by P1/P2/P3 | `mttr_p1`..`mttr_p3` | min | Detail |
| 13 | % of P1/P2 detected by alerts | `pct_p1p2_detected_by_alerts` | % | Detail |
| 14 | Actionable Alerts / Escalation Reduction | `actionable_alerts_reduction` | count | Detail |
| 15 | Total Cost Reduction | `cost_reduction_zero_touch` + `cost_reduction_techsupport` | $ | Summary |
| 16 | Cost Reduction by Workstream | `cost_reduction_zero_touch`, `cost_reduction_techsupport` | $ | Detail |
| 17 | Alert Noise Reduction | `alert_noise_reduction` | count | Detail |
| 18 | Suppression Rate | `suppression_rate` | % | Detail |
