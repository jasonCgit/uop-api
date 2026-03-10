# Porting Outcome Measures

Files and changes needed to add the Outcome Measures tab to a clean UOP deployment.

## New files (copy wholesale)

| Repo | File | Description |
|------|------|-------------|
| uop-api | `app/mock_data/outcome_measures_data.py` | Mock data |
| uop-api | `app/routers/outcome_measures.py` | API endpoints |
| uop-ui | `src/pages/OutcomeMeasures.jsx` | Page component |
| uop-ui | `src/components/outcome-measures/ExecutiveKpiBar.jsx` | Top-level KPI bar (Adoption, SRE Coverage, Results) |
| uop-ui | `src/components/outcome-measures/ExecutiveSummary.jsx` | Making a Dent / Needs Focus / Workstream Effectiveness |
| uop-ui | `src/components/outcome-measures/OutcomeTrendChart.jsx` | 12-month trend sparkline charts |
| uop-ui | `src/components/outcome-measures/SectionKpiCards.jsx` | Section-specific KPI card grid |

## Edits to existing files

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
  desc: 'SRE outcome metrics across 5 sections — 12-month trend charts, baseline comparisons, CTO/CBT leaderboards, and workstream tracking.',
},
```

## Full Metric Coverage

All metrics mapped to the Outcome Measures Plan spreadsheet.

### Adoption (9 metrics)

| # | Spreadsheet Name | Metric Key | Unit |
|---|---|---|---|
| 1 | Total number of users by week | `total_users_week` | users/wk |
| 2 | Total volume of prompt executions | `mcp_requests` | req/mo |
| 3 | MCP: Volume of requests per MCP server / FinOps | `mcp_requests` | req/mo |
| 4 | UOP Chat volume of prompts | `uop_chat_prompts` | prompts/mo |
| 5 | Clicks by feature — Blast Radius | `clicks_blast_radius` | clicks/mo |
| 6 | Clicks by feature — CUJ | `clicks_cuj` | clicks/mo |
| 7 | Clicks by feature — SLO Agent | `clicks_slo_agent` | clicks/mo |
| 8 | Clicks by feature — AURA | `clicks_aura` | clicks/mo |
| 9 | Usage: Prompt executions in DevGPT (Zero-Touch M&O MCP) | `devgpt_executions` | exec/mo |
| 10 | Usage: Volume of simulations executed (AI Chaos Simulator) | `simulation_executions` | runs/mo |

### SRE Coverage (4 metrics)

| # | Spreadsheet Name | Metric Key | Unit |
|---|---|---|---|
| 1 | Dynatrace Coverage | `dynatrace_coverage` | % |
| 2 | Golden Signals Coverage | `golden_signals_coverage` | % |
| 3 | SRE Telemetry Coverage (SLOs) | `sre_telemetry_coverage` | % |
| 4 | UOP Coverage | `uop_coverage` | % |

### Results (23 metrics)

| # | Spreadsheet Name | Metric Key | Unit |
|---|---|---|---|
| 1 | Incidents avoided → Code Updates in DevGPT | `incidents_avoided` | count |
| 2 | Incidents avoided — UAT | `incidents_avoided_uat` | count |
| 3 | Incidents avoided — Prod | `incidents_avoided_prod` | count |
| 4 | Anomalies detected per 100 changes | `anomaly_rate` | /100 chg |
| 5 | Change Aware Anomaly Rate | `change_aware_anomaly_rate` | /100 chg |
| 6 | AI Driven Impact Duration | `ai_impact_duration` | min |
| 7 | Alert Response Time | `alert_response_time` | min |
| 8 | Response Type: AIOpsmode/UOP/AURA | `response_type_breakdown` | count |
| 9 | Response Time by Type | `response_time_by_type` | min |
| 10 | Incident/Tickets Trending | `p1_incidents` (headline) | count |
| 11 | P1 Incidents | `p1_incidents` | count |
| 12 | P2 Incidents | `p2_incidents` | count |
| 13 | P3 Incidents | `p3_incidents` | count |
| 14 | P4 Incidents | `p4_incidents` | count |
| 15 | P5 Incidents | `p5_incidents` | count |
| 16 | MTTR — P1 | `mttr_p1` | min |
| 17 | MTTR — P2 | `mttr_p2` | min |
| 18 | MTTR — P3 | `mttr_p3` | min |
| 19 | % of P1/P2 detected by alerts | `pct_p1p2_detected_by_alerts` | % |
| 20 | Actionable Alerts / Escalation Reduction | `actionable_alerts_reduction` | count |
| 21 | Total Cost Reduction | `cost_reduction_zero_touch` + `cost_reduction_techsupport` | $ |
| 22 | Alert Noise Reduction | `alert_noise_reduction` | count |
| 23 | Suppression Rate | `suppression_rate` | % |

### Workstream Details (8 workstreams)

Golden Signal Monitoring, SLO Management, Incident Zero, Blast Radius Analysis, Zero-Touch M&O, SRE Telemetry, AURA AI Assistant, Knowledge Graph — each with adoption %, maturity, and value scores.
