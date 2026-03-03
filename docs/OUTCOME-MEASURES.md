# SRE Outcome Measures — Telling the Story of Value

> **Purpose:** A structured report that demonstrates how SRE tooling (UOP, AURA, AIOps360, ZeroTouch, MCPs) delivers measurable business value — not by building new tools, but by showing the impact of what already exists under the AIOps360 umbrella.

> **Audience:** Technology leadership, CTO/LOB owners, SRE leads

> **Reporting cadence:** Monthly trend snapshots with quarterly narrative summaries

---

## Glossary

| Term | Definition |
|------|-----------|
| **SEAL** | Unique application identifier in the Product Catalog (e.g., SEAL 16649 = Morgan Money). Every application in UOP is tracked by its SEAL. |
| **CTO** | Chief Technology Officer — top-level technology leadership unit that groups applications. |
| **CBT** | Component Business Team — mid-level team responsible for a specific business/technical domain under a CTO. |
| **LOB** | Line of Business (e.g., AWM, CIB, CCB). Top of the business hierarchy. |
| **Sub-LOB** | Subdivision within a LOB (e.g., Asset Management, Global Private Bank under AWM). |
| **Incident Zero** | UOP's proactive pre-incident SLO management feature. Tracks error budget consumption, burn rate alerts, and breach ETAs to catch problems before they become incidents. |
| **Rapid Response (RR)** | Rapid Response process — the escalation workflow that creates incidents from critical alert patterns. |
| **Day 1 Deliverables** | The initial onboarding package for each application: Dynatrace instrumentation, Golden Signal configuration, UOP signal setup, and SLO definition. |
| **Knowledge Graph** | UOP's 5-layer dependency model (Health Indicators → Components → Platforms → Data Centers + Cross-SEAL dependencies) sourced from ERMA/V12. Powers blast radius analysis via BFS traversal. |
| **True Impact Duration** | Time from when a signal turns RED/AMBER to when it returns to GREEN, measured automatically from Dynatrace indicator data. Replaces manual MTTR for all severities. |

---

## Report Structure — The Five Sections

The report is organized as a **top-down story**: start with adoption proof, zoom into workstream impact, show SRE-specific outcomes, anchor it all to traditional support metrics, and establish coverage baselines.

```
┌─────────────────────────────────────────────────────────────┐
│                    OUTCOME MEASURES REPORT                   │
├─────────────────────────────────────────────────────────────┤
│  Section 1 │ Overall Usage & Adoption                       │
│  Section 2 │ Priority Workstream Effectiveness              │
│  Section 3 │ SRE Effectiveness                              │
│  Section 4 │ Traditional Support Measures                   │
│  Section 5 │ SRE Coverage — Baseline Roll-up                │
├─────────────────────────────────────────────────────────────┤
│  Day 2     │ Per-CTO Narratives & Leaderboards              │
└─────────────────────────────────────────────────────────────┘
```

Each section follows the pattern: **headline metric → trend graph → segmentation → narrative**.

**Segmentation standard:** All metrics should be filterable at four levels: **LOB → CTO → CBT → SEAL**. This matches UOP's native filter hierarchy and allows leadership to drill from portfolio-level down to individual application performance.

**Trend standard:** All trend graphs use a **12-month rolling window** to show seasonality and long-term trajectory.

---

## Section 1: Overall Usage & Adoption

> **Story:** "People are using our tools and adoption is growing."

This section proves the tools are being used before making any effectiveness claims. Without usage, effectiveness metrics are meaningless.

### 1.1 AI Code Assist (AIOpsmode in DevGPT)

| Metric | Definition | Calculation | Visual |
|--------|-----------|-------------|--------|
| Prompt Executions | Volume of AI-assisted code interactions | Count of prompt executions per period | Area chart, 12-month rolling trend |

### 1.2 UOP Platform

| Metric | Definition | Calculation | Visual |
|--------|-----------|-------------|--------|
| Chat Volume | AURA chat interactions within UOP | Count of user prompts to AURA per period | Area chart, 12-month rolling trend |
| Click Volume | User engagement with UOP dashboards | Count of meaningful clicks/actions per period | Area chart, 12-month rolling trend |

### 1.3 MCP Server Usage

| Metric | Definition | Calculation | Visual |
|--------|-----------|-------------|--------|
| Request Volume | API calls against each MCP server | Count of requests per MCP server per period | Stacked bar chart by MCP server |

### 1.4 Per-CTO/CBT/SEAL Segmentation & Leaderboards

| Metric | Definition | Calculation | Visual |
|--------|-----------|-------------|--------|
| Usage by Segment | Adoption volumes broken by LOB/CTO/CBT/SEAL | Sum of events per segment over selected period | Leaderboard table with sparklines |
| Share Mix | Proportional usage across segments | Percentage of total per LOB/CTO/CBT | Stacked 100% bar or treemap |

**Visual — Overall Usage Dashboard:**

```
┌─────────────────────────────────────────────────────────────────┐
│  OVERALL USAGE & ADOPTION                          Period: ▾    │
├───────────────────┬───────────────────┬─────────────────────────┤
│ AI Code Assist    │ UOP Platform      │ MCP Servers             │
│ ┌───────────────┐ │ ┌───────────────┐ │ ┌─────────────────────┐ │
│ │  12,847       │ │ │  8,234 chats  │ │ │ ZeroTouch   ███░ 4k │ │
│ │  prompts      │ │ │  24,891 clicks│ │ │ AOComms     ██░░ 2k │ │
│ │  ▲ 18% MoM    │ │ │  ▲ 12% MoM   │ │ │ FinOps      █░░░ 1k │ │
│ └───────────────┘ │ └───────────────┘ │ └─────────────────────┘ │
├───────────────────┴───────────────────┴─────────────────────────┤
│  ADOPTION TREND (12-month rolling)                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │        ╱──────  AI Code Assist                             │ │
│  │   ╱───╱         ───── UOP                                  │ │
│  │  ╱  ╱╱          - - - MCP                                  │ │
│  │ ╱──╱                                                       │ │
│  │╱─╱                                                         │ │
│  ├────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┤ │
│  │ Apr│ May│ Jun│ Jul│ Aug│ Sep│ Oct│ Nov│ Dec│ Jan│ Feb│ Mar │ │
│  │         2025                                     2026      │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  LEADERBOARD — Per CTO / CBT                                   │
│  ┌────────────────────┬──────┬──────┬──────┬──────────────────┐ │
│  │ CTO / CBT           │ AIOps│  UOP │  MCP │ Trend            │ │
│  ├────────────────────┼──────┼──────┼──────┼──────────────────┤ │
│  │ AWM                │ 3.2k │ 8.1k │ 1.4k │ ▁▂▃▅▆▇ ▲ 22%    │ │
│  │  └ Client Data     │ 1.8k │ 4.2k │  820 │ ▁▂▃▅▆▇ ▲ 26%    │ │
│  │  └ Connect Platf.  │ 1.4k │ 3.9k │  580 │ ▁▂▃▄▅▆ ▲ 18%    │ │
│  │ Technology         │ 2.8k │ 6.4k │ 2.1k │ ▁▂▃▄▅▆ ▲ 18%    │ │
│  │ Global Banking     │ 1.9k │ 4.2k │  890 │ ▁▂▂▃▃▄ ▲ 11%    │ │
│  │ Consumer           │ 1.1k │ 2.8k │  420 │ ▁▁▂▂▃▃ ▲  8%    │ │
│  └────────────────────┴──────┴──────┴──────┴──────────────────┘ │
│                                                                 │
│  Drill-down: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 2: Priority Workstream Effectiveness

> **Story:** "Each workstream is delivering measurable outcomes — less toil, faster resolution, lower cost."

### 2.1 Zero Touch (M&O)

*Owners: Vamsi (Tech), Aarushi (Delivery), Mike (Owner)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Prompt Executions | Usage | Volume in DevGPT against Zero-Touch M&O MCP | Count per period |
| Dynatrace & Golden Signal Coverage | Coverage | Uplift on Day 1 Deliverables (Dynatrace instrumentation + Golden Signals) | % onboarded vs target; trend |
| Net $ Savings | Cost | Resource time saved through automation | Hours saved × blended rate |

### 2.2 SRE Telemetry

*Owners: Aarushi (Tech), Aarushi (Delivery), Jason (Owner)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Prompt Executions | Usage | Volume in DevGPT against SRE Telemetry MCP | Count per period |
| UOP Onboarding & SLOs | Coverage | Uplift on Day 1 Deliverables (UOP signal setup + SLO definition) | Apps onboarded vs target; trend |
| Net $ Savings | Cost | Resource time saved | Hours saved × blended rate |

### 2.3 Blast Radius & Knowledge Graph

*Owners: Eric D (Tech), Atziri (Delivery), Bhargav (Owner)*

The Knowledge Graph in UOP uses a **5-layer architecture** sourced from ERMA/V12:

```
Health Indicators (869 monitors: Process Group / Service / Synthetic)
    ↓ mapped to
Components (~90 services with status, SLA, incidents)
    ↔ cross-SEAL upstream/downstream dependencies
    ↓ deployed on
Platforms (GAP, GKP, ECS, EKS, AWS)
    ↓ located in
Data Centers (NA, EMEA, APAC regions)
```

**Blast radius** is computed via BFS traversal: given a failing component, the graph identifies all transitively dependent components and propagates effective status (worst-of-dependencies) up through deployments to applications.

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Application Graph Coverage | Coverage | % of onboarded applications with component-level mappings in the Knowledge Graph | (SEALs with component mappings / total onboarded SEALs) × 100; currently 10 of 81 apps |
| Dependency Completeness | Coverage | Component-to-component dependency edges mapped per application | Count of edges per SEAL; track trend as new dependencies are discovered and mapped |
| Cross-SEAL Dependencies Mapped | Coverage | Cross-application upstream/downstream relationships captured | Count of external/cross-SEAL dependency edges; trend |
| Blast Radius Queries | Usage | Number of blast radius and dependency lookups performed by users | Count of `/api/graph/blast-radius/` and `/api/graph/dependencies/` requests per period |
| Impact Prediction Accuracy | Effectiveness | When an incident occurs, did the blast radius correctly predict impacted components? | % of incident-affected components that were in the blast radius path of the root cause component |

### 2.4 Alert Severity Solution

*Owners: Eric D (Tech), Atziri (Delivery), Bhargav (Owner)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Open Incident Duration | Effectiveness | Track open incident duration vs baseline | RCA summaries into Rapid Response-created incidents; compare against avg baseline |
| RED Alert Reduction | Effectiveness | Reduction in RED alerts for apps in scope | Count RED alerts vs pre-period baseline |
| RED Alert Accuracy | Effectiveness | Do RED alerts correspond to real P1/P2 incidents? | % of RED alerts with matching P1/P2; % of P1/P2s with matching RED alert |
| Net $ Savings | Cost | Resource time saved from alert noise reduction | Hours saved × blended rate |
| AURA Noise Filtering Rate | Effectiveness | Suppression rate = suppressed / total raw alerts | Count of alerts suppressed by AURA ÷ raw alert count per period; report by app and aggregate |
| UOP Precision Trend | Effectiveness | % of UOP alerts that lead to action (click, AIOps inquiry, incident linkage) | Alerts with any correlated action ÷ total UOP alerts per period |
| SRE Toil Reduction | Operational | Actionable alerts per on-call per week + after-hours pages per week | Count of actionable alerts/pages allocated to on-call schedules |
| P1/P2 Incident Reduction | Effectiveness | Reduction in P1 and P2 incidents for apps in scope | Count of P1/P2 incidents per period vs baseline; sourced from ServiceNow `p1_30d` and `p2_30d` fields; report by LOB/CTO/CBT/SEAL |
| Service Request Reduction | Effectiveness | Reduction in ESD service requests for apps in scope | Count of service requests per period vs baseline; segmented by request type and LOB/CTO/CBT/SEAL |

### 2.5 AURA — Central Orchestration Engine

*Owners: Shravan (Tech), Jose (AIOpsmode) / Atziri (UOP) (Delivery), Bhargav (Owner)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Anomalies & RCAs Produced | Productivity | Volume of automated analysis outputs | Count per period |
| AIOpsmode Prompts | Usage | Prompts + code updates in DevGPT | Volume per period |
| UOP Requests | Usage | User requests to AURA (Chat and non-Chat) | Count per period |
| Incidents Avoided | Effectiveness | Proactive catches that prevented production impact | Number of code updates correlated to anomaly detection |
| Anomaly Trends | Effectiveness | Volume trend of anomalies detected | Count per period; trend line |
| Change-Aware Anomaly Rate | Effectiveness | Anomalies per 100 changes — contextualizes stability vs pace of change | (Total anomalies ÷ total code changes or deployments in same period) × 100 |

### 2.6 Resiliency AI Chaos Simulator

*Owners: Jose (Tech), Jose (Delivery), Eric V/Adam (Owners)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Simulations Executed | Usage | Volume of chaos simulations run | Count per period |
| Issues Identified | Effectiveness | Issues found & remediated in UAT and Prod | Count; UAT vs Prod breakdown |
| Team Adoption | Effectiveness | Teams running actual chaos engineering | Count of teams with executions in UAT & Prod |

### 2.7 Individual AO Comms Actionable Insights

*Owners: Animesh (Tech), Jose (Delivery), Bhargav/Ray (Owners)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Prompt Executions | Usage | Volume in DevGPT against AOComms MCP | Count per period |
| Net $ Savings | Cost | Resource time saved | Hours saved × blended rate |

### 2.8 FinOps Cost Optimization

*Owners: Vamsi (Tech), Atziri (Delivery), Mike/Ray (Owners)*

| Metric | Type | Definition | Calculation |
|--------|------|-----------|-------------|
| Prompt Executions | Usage | Volume in DevGPT against FinOps MCP | Count per period |
| Savings Identified | Cost | Potential $ savings surfaced by tool | Total $ save identified |
| Savings Executed | Cost | Actual $ savings realized | Total $ save executed |

**Visual — Workstream Effectiveness Dashboard:**

```
┌─────────────────────────────────────────────────────────────────┐
│  PRIORITY WORKSTREAM EFFECTIVENESS                 Period: ▾    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─ Zero Touch ──────┐  ┌─ SRE Telemetry ────┐                 │
│  │ Usage    12.4k ▲18%│  │ Usage     8.2k ▲22%│                 │
│  │ Coverage   72% ▲8% │  │ Coverage   64% ▲12%│                 │
│  │ Savings  $142k     │  │ Savings   $98k     │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                 │
│  ┌─ Alert Severity ──┐  ┌─ AURA Engine ──────┐                 │
│  │ RED Alerts  -31%   │  │ Anomalies   1,247  │                 │
│  │ Precision    78%   │  │ RCAs          892  │                 │
│  │ P1s        -28%   │  │ Change Rate  3.2%  │                 │
│  │ P2s        -18%   │  │ Incidents     -18  │                 │
│  │ Svc Reqs   -12%   │  │                     │                 │
│  │ Noise Filt.  84%   │  │                     │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                 │
│  ┌─ Blast Radius ────┐  ┌─ FinOps ───────────┐                 │
│  │ Graph Cov.  12%    │  │ Identified  $1.2M  │                 │
│  │ Deps Mapped 247    │  │ Executed     $840k │                 │
│  │ X-SEAL Deps  34    │  │                     │                 │
│  │ Queries    1,820   │  │                     │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                 │
│  ALERT SEVERITY — NOISE REDUCTION TREND (12-month rolling)      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Raw Alerts   ████████████████████████████████  12,400      │ │
│  │ After AURA   ████████████░░░░░░░░░░░░░░░░░░░   4,200      │ │
│  │ Actioned     ██████░░░░░░░░░░░░░░░░░░░░░░░░░   2,100      │ │
│  │                                                            │ │
│  │              66% suppressed          50% actioned          │ │
│  │              ──────────── filtering ────────────            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  P1/P2 INCIDENT REDUCTION (12-month rolling)                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Count   40 │                                              │ │
│  │          30 │╲          P2                                 │ │
│  │          20 │ ╲___╱╲___╱╲___                               │ │
│  │          10 │╲  P1           ╲___╱╲___                     │ │
│  │           5 │ ╲───────────────────────╲___                 │ │
│  │           0 ├────┬────┬────┬────┬────┬────┬────┬────┬────┬ │ │
│  │              Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec   │ │
│  │              Jan  Feb  Mar                                 │ │
│  │              2025                                    2026  │ │
│  │                                                            │ │
│  │  P1: 12 this period (▼ 28% vs baseline)                   │ │
│  │  P2: 47 this period (▼ 18% vs baseline)                   │ │
│  │  Svc Requests: 184 (▼ 12% vs baseline)                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  AURA — CHANGE-AWARE ANOMALY RATE (12-month rolling)            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Anomalies                                                 │ │
│  │  per 100     5 │     ╲                                     │ │
│  │  changes     4 │      ╲___                                 │ │
│  │              3 │          ╲___╱╲                            │ │
│  │              2 │                ╲___                        │ │
│  │              1 │                    ╲___                    │ │
│  │              0 ├────┬────┬────┬────┬────┬────┬────┬────┬── │ │
│  │                 Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec │ │
│  │                 Jan  Feb  Mar                               │ │
│  │                 2025                                  2026  │ │
│  │                                                            │ │
│  │  ↓ Fewer anomalies per change = platform getting stabler   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Drill-down: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 3: SRE Effectiveness

> **Story:** "Signals are being seen, acted on faster, and problems are resolving quicker — without relying solely on MTTR."

This is the heart of the report. These metrics answer the question leadership really cares about: *Are SRE teams actually more effective because of these tools?*

### 3.1 Time to Signal Disappearance (True Impact Duration)

> Better than manual MTTR — this is measured automatically from Dynatrace indicator data.

**Definition:** Duration from when a health indicator turns RED/AMBER until it returns to GREEN. Measured per indicator, reported as distribution bands and medians. UOP tracks 869 health indicators across ~90 components, making this metric comprehensive across all severities.

**Why this matters:** MTTR is manually tracked and only accurate for P1s. True Impact Duration is automatically measured from real signal data across all severities. It tells us with precision when alerts started (impact begin) and when they stopped (impact end).

**Calculation:** For each signal:
- `impact_duration = timestamp(signal returns GREEN) - timestamp(signal turned RED/AMBER)`
- Report distribution bands and medians

**Distribution Bands** (avoid misleading averages):

| Band | Definition | Target | Visual |
|------|-----------|--------|--------|
| Fast resolvers | Resolved 20%+ faster than baseline | 50% of signals | Green bar |
| Improving | Resolved 5-20% faster | 20% of signals | Light green bar |
| Neutral | Within ±5% of baseline | 20% of signals | Gray bar |
| Slower | Resolved slower than baseline | ≤10% of signals | Red bar |

**Visual — Time to Signal Disappearance:**

```
┌─────────────────────────────────────────────────────────────────┐
│  TIME TO SIGNAL DISAPPEARANCE                                   │
│  "How quickly are real problems being resolved?"                │
│                                                                 │
│  ┌─ Distribution Bands ─────────────────────────────────────┐   │
│  │                                                          │   │
│  │  Resolved 20%+ faster  ████████████████████████░░  54%   │   │
│  │  Resolved 5-20% faster ██████████░░░░░░░░░░░░░░░  21%   │   │
│  │  Neutral (±5%)         ████████░░░░░░░░░░░░░░░░░  17%   │   │
│  │  Resolved slower       ███░░░░░░░░░░░░░░░░░░░░░░   8%   │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ Median Duration Trend (12-month rolling) ─────────────┐    │
│  │                                                          │   │
│  │  Minutes   120 │ ╲                                       │   │
│  │            100 │  ╲                                      │   │
│  │             80 │   ╲___                                  │   │
│  │             60 │       ╲___                              │   │
│  │             40 │           ╲___╱╲___                     │   │
│  │             20 │                    ╲___                  │   │
│  │              0 ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──     │   │
│  │                 A  M  J  J  A  S  O  N  D  J  F  M      │   │
│  │                 2025                           2026      │   │
│  │                                                          │   │
│  │  Median: 42 min     Baseline: 98 min    ▼ 57% faster    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Segmented by: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]            │
│                [All Severities ▾]                                │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Are Signals Being Accessed & Addressed?

**Definition:** Measure the gap between when a signal appears and when someone engages with it. Tracks engagement across multiple channels.

| Channel | What to Measure | Calculation |
|---------|----------------|-------------|
| UOP | Signal appeared in UOP → user clicked on it | `timestamp(first UOP click) - timestamp(signal created)` |
| AIOps/IDE | Signal appeared → first AIOps or IDE inquiry about it | `timestamp(first IDE inquiry) - timestamp(signal created)` |
| Incident Zero | Signal has a corresponding Incident Zero entry by SRE (error budget / burn rate tracked) | % of signals with matching Incident Zero record; median time from signal to entry |

#### 3.2a Time from Signal to First Action (Latency to Engagement)

**Definition:** Time from signal appearance to first user action (UOP click) or first AIOps/IDE inquiry.

**Reporting:** Medians and bands (% within 5m / 30m / 2h / 8h), segmented by LOB/CTO/CBT/SEAL.

| Band | Meaning |
|------|---------|
| < 5 min | Immediate response — signal was caught in real-time |
| 5 – 30 min | Fast response — likely active monitoring |
| 30 min – 2 hr | Moderate — picked up within shift |
| 2 – 8 hr | Delayed — likely found on next check |
| > 8 hr | Stale — signal may have been missed |

#### 3.2b Incident Zero Correlation

**Definition:** % of signals with a corresponding Incident Zero entry and median time from signal to entry.

**Calculation:** Correlate signal IDs/timestamps with Incident Zero records; report % coverage and latency distribution.

**Visual — Signal Engagement:**

```
┌─────────────────────────────────────────────────────────────────┐
│  SIGNAL ENGAGEMENT — "Are signals being seen and acted on?"     │
│                                                                 │
│  ┌─ Latency to First Action ────────────────────────────────┐   │
│  │                                                          │   │
│  │         UOP Click              AIOps/IDE Inquiry         │   │
│  │  ┌──────────────────┐    ┌──────────────────┐            │   │
│  │  │  Median: 8 min   │    │  Median: 22 min  │            │   │
│  │  │  ▼ 34% from base │    │  ▼ 41% from base │            │   │
│  │  └──────────────────┘    └──────────────────┘            │   │
│  │                                                          │   │
│  │  < 5 min   ██████████████████████████████░░░░░  62%      │   │
│  │  5-30 min  █████████░░░░░░░░░░░░░░░░░░░░░░░░░  22%      │   │
│  │  30m-2hr   ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10%      │   │
│  │  2-8hr     ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4%      │   │
│  │  > 8hr     █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2%      │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ Incident Zero Correlation ──────────────────────────────┐   │
│  │                                                          │   │
│  │  72% of signals have a corresponding Incident Zero entry │   │
│  │  Median time from signal → IZ entry: 14 min              │   │
│  │                                                          │   │
│  │  ████████████████████████████████████░░░░░░░░░░░  72%    │   │
│  │  ▲ from 58% baseline                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Segmented by: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]            │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Who Is Using Our Tools?

Tracks unique users and sessions by tool, segmented by LOB/CTO/CBT/SEAL. While Section 1 measures raw volume, this section measures breadth of adoption — how many distinct people are engaging.

| Tool | Metric | Calculation |
|------|--------|-------------|
| AIOpsmode | Unique users & sessions | Count distinct users and sessions per period |
| MCPs | Unique users & sessions per MCP | Count distinct users and sessions per MCP per period |
| UOP | Unique users & sessions | Count distinct users and sessions per period |

**Per-CTO/CBT/SEAL Segmentation**: Show adoption and active-use rates. Funnel view: awareness → trial → active use.

**Visual — Tool Adoption Funnel:**

```
┌─────────────────────────────────────────────────────────────────┐
│  TOOL ADOPTION — Per CTO/CBT                                    │
│                                                                 │
│  AWM — Client Data (CBT: Kalpesh Narkhede)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Aware (onboarded)  ████████████████████████████████  142│   │
│  │  Trial (1-3 uses)   ██████████████████████░░░░░░░░░░   98│   │
│  │  Active (weekly)    ██████████████░░░░░░░░░░░░░░░░░░   64│   │
│  │                                              45% active  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  AWM — Connect Platform (CBT: Jon Glennie)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Aware (onboarded)  ████████████████████████████████  128│   │
│  │  Trial (1-3 uses)   ████████████████████████░░░░░░░░  108│   │
│  │  Active (weekly)    █████████████████░░░░░░░░░░░░░░░   82│   │
│  │                                              64% active  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Drill-down: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 4: Traditional Support Measures

> **Story:** "The traditional metrics are trending in the right direction too — fewer incidents, faster resolution."

These metrics are already available today and provide the familiar benchmarks leadership expects. They complement (but shouldn't replace) the SRE-specific measures above.

### 4.1 Incidents Trending

**Definition:** Count of incidents per severity per period for pilot apps.

**Calculation:** Time series by P-level (P1/P2/P3/P4/P5) plus ESD service requests as a separate series. Include normalized rate per 100 services if needed. Sourced from ServiceNow (`p1_30d`, `p2_30d` per application in UOP).

**What to show:**
- Baseline on incidence for 2025 for all applications onboarded to AIOps360
- P1/P2 reduction trend tells the proactive prevention story
- Service request reduction tells the TechSupport agent scope story
- Segment by LOB/CTO/CBT/SEAL to show which teams are driving improvement

### 4.2 MTTR by Severity

**Definition:** Mean time to resolve per severity, per period.

**Calculation:** Average incident resolution time by severity; show distribution and medians. Sourced from ServiceNow (MTTR, MTTA, resolution_rate, escalation_rate already tracked in UOP dashboard data).

**Caveats to communicate:**
- MTTR is manually tracked and is only accurate for P1s
- For other priorities it is less reliable
- Ticket MTTR (resolution time - opening time) can supplement but doesn't tell the full story
- **True Impact Duration (Section 3.1) is the recommended primary metric** for measuring actual resolution speed

### 4.3 Proactive Incidence Prevention (AIOps360-Triggered)

**Definition:** JIRAs (fixes) going to production on the back of an AIOps360 trigger should carry an `AIOps360 triggered` label.

**Calculation:** Count of JIRAs with `AIOps360 triggered` label per period. Link anomalies to PRs/fixes. Segment by LOB/CTO/CBT/SEAL.

### 4.4 Service Request Volume & Reduction

**Definition:** Count of ESD service requests per period for onboarded applications.

**Calculation:** Time series of service request volume by request type. Compare against pre-AIOps360 baseline to show self-service deflection.

**What to show:**
- Total service request volume trend (12-month rolling)
- Breakdown by request type (password resets, access provisioning, configuration changes, etc.)
- Reduction % vs baseline, segmented by LOB/CTO/CBT/SEAL

**Visual — Traditional Support Measures:**

```
┌─────────────────────────────────────────────────────────────────┐
│  TRADITIONAL SUPPORT MEASURES                                   │
│                                                                 │
│  ┌─ Incidents Trending (12-month rolling) ────────────────┐     │
│  │                                                          │   │
│  │  Count   200 │ ╲                                         │   │
│  │          150 │  ╲  P3+                                   │   │
│  │          100 │   ╲___╱╲___                               │   │
│  │           50 │  ╲  P2       ╲___                         │   │
│  │           25 │───╲──────────────── P1                    │   │
│  │            0 ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──       │   │
│  │               A  M  J  J  A  S  O  N  D  J  F  M        │   │
│  │               2025                           2026        │   │
│  │                                                          │   │
│  │  P1: 12 (▼ 28%)   P2: 47 (▼ 18%)   P3+: 124 (▼ 8%)    │   │
│  │  Svc Requests: 184 (▼ 12%)                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ MTTR by Severity ───────────────────────────────────────┐   │
│  │                                                          │   │
│  │  P1  ████████████████░░░░░░░░░░░░░░░  42 min (▼ 22%)    │   │
│  │  P2  ██████████████████████░░░░░░░░░  68 min (▼ 14%)    │   │
│  │  P3  ████████████████████████████░░░  118 min (▼ 6%)    │   │
│  │                                                          │   │
│  │  ⚠ P1 MTTR is manually tracked; P2+ less reliable       │   │
│  │  → See "True Impact Duration" for automated measurement  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ AIOps360-Triggered Fixes ───────────────────────────────┐   │
│  │                                                          │   │
│  │  48 JIRAs with AIOps360 label this period                │   │
│  │  ████████████████████████████████████████████████  ▲ 62% │   │
│  │  ███████████████████████████████░░░░░░░░░░░░░░░░  prev   │   │
│  │                                                          │   │
│  │  "Proactive fixes going to prod before customer impact"  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Drill-down: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 5: SRE Coverage — Baseline Roll-up

> **Story:** "We are building a foundation — here is exactly where we stand on coverage, and where the gaps are."

This section establishes the baseline. Without coverage, effectiveness metrics only apply to a subset of the portfolio. This tells leadership how much ground is covered and what remains.

### 5.1 Dynatrace Coverage

**Definition:** % of pilot apps onboarded to Dynatrace with Golden Signals configured.

**Calculation:** (Apps onboarded with Golden Signals / total pilot apps) × 100; show trend and count.

**Segmentation:** By LOB/CTO/CBT/SEAL.

### 5.2 SRE Telemetry Coverage

**Definition:** % of pilot apps with SRE telemetry integrated into agreed dashboards/data pipelines.

**Calculation:** (Apps with SRE telemetry live / total pilot apps) × 100.

**Segmentation:** By LOB/CTO/CBT; show gaps and target dates.

### 5.3 UOP Coverage

**Definition:** % of pilot apps with UOP signals and SLOs configured and active.

**Calculation:** (Apps with UOP signals & SLOs / total pilot apps) × 100. Measurable from UOP's completeness score (`has_slo`, `has_sla`, `has_blast_radius` fields).

**Segmentation:** By LOB/CTO/CBT/SEAL; include SLOs defined vs. in-progress.

### 5.4 Knowledge Graph Coverage

**Definition:** % of pilot apps with component-level mappings in the Knowledge Graph.

**Calculation:** (SEALs with component mappings / total pilot apps) × 100. Currently 10 of 81 applications have component data mapped. This is the foundation for blast radius analysis — apps without graph data cannot benefit from dependency-aware alerting.

**Segmentation:** By LOB/CTO/CBT; show gap count and target dates.

**Visual — Coverage Baseline:**

```
┌─────────────────────────────────────────────────────────────────┐
│  SRE COVERAGE — BASELINE ROLL-UP                                │
│  "Where do we stand today?"                                     │
│                                                                 │
│  ┌─ Coverage Summary ───────────────────────────────────────┐   │
│  │                                                          │   │
│  │      Dynatrace     SRE Telemetry    UOP     K. Graph     │   │
│  │     ┌────────┐     ┌────────┐    ┌────────┐ ┌────────┐   │   │
│  │     │        │     │        │    │        │ │        │   │   │
│  │     │  78%   │     │  64%   │    │  52%   │ │  12%   │   │   │
│  │     │        │     │        │    │        │ │        │   │   │
│  │     │ 142/182│     │ 116/182│    │ 95/182 │ │ 10/81  │   │   │
│  │     └────────┘     └────────┘    └────────┘ └────────┘   │   │
│  │     ▲ 12% QoQ     ▲ 18% QoQ    ▲ 22% QoQ  baseline     │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ Coverage by CTO/CBT ─────────────────────────────────┐     │
│  │                                                          │   │
│  │  CTO / CBT          │ Dyna  │ Telem │  UOP  │ Graph│ Gap │   │
│  │  ────────────────────┼───────┼───────┼───────┼──────┼─────   │
│  │  AWM                │  88%  │  72%  │  68%  │  18% │ 12  │   │
│  │   └ Client Data     │  92%  │  78%  │  74%  │  22% │  4  │   │
│  │   └ Connect Platf.  │  84%  │  66%  │  62%  │  14% │  8  │   │
│  │  Technology         │  82%  │  70%  │  58%  │  10% │ 18  │   │
│  │  Global Banking     │  74%  │  58%  │  42%  │   8% │ 24  │   │
│  │  Consumer           │  62%  │  48%  │  34%  │   6% │ 31  │   │
│  │                                                          │   │
│  │  Cells: ■ >75% green  ■ 50-75% amber  ■ <50% red        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ Coverage Trend (12-month rolling) ────────────────────┐     │
│  │                                                          │   │
│  │  %     100 │                          ╱── Dynatrace      │   │
│  │  covered 80│                    ╱────╱                    │   │
│  │          60│              ╱────╱  ╱── SRE Telemetry      │   │
│  │          40│        ╱────╱  ╱────╱                        │   │
│  │          20│  ╱────╱  ╱────╱  ╱── UOP                    │   │
│  │          10│─╱───────╱──────╱── K. Graph                  │   │
│  │           0├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──          │   │
│  │             A  M  J  J  A  S  O  N  D  J  F  M           │   │
│  │             2025                           2026           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Drill-down: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Day 2 Enhancements

### MCP/AURA Use Case Narratives with Measured Outcomes

> **Story:** "Here is a real before-and-after for each CTO — not just metrics, but narratives."

For each CTO, document a before/after story with metrics:

**Template:**

| Field | Description |
|-------|------------|
| **Problem Statement** | What was the pain point before AIOps360 intervention? |
| **Intervention** | Which tool + workflow was applied (AURA, MCP, UOP, ZeroTouch)? |
| **Metrics Impact** | Usage, time-to-action, anomalies per 100 changes, incidents avoided, toil reduction |
| **Time Horizon** | Measurement period |
| **Owners** | CTO, delivery lead, tech lead |

**Example Narrative:**

```
┌─────────────────────────────────────────────────────────────────┐
│  USE CASE: AWM — Automated Anomaly Detection                    │
│                                                                 │
│  BEFORE                          AFTER                          │
│  ┌─────────────────────┐         ┌─────────────────────┐        │
│  │ Manual alert triage  │         │ AURA auto-triage    │        │
│  │ 45 min avg response  │   →     │ 8 min avg response  │        │
│  │ 12 P1s per quarter   │         │ 4 P1s per quarter   │        │
│  │ 340 raw alerts/week  │         │ 82 actionable/week  │        │
│  └─────────────────────┘         └─────────────────────┘        │
│                                                                 │
│  Tool: AURA + UOP Signals    Period: Q3 2025 → Q1 2026         │
│  Owner: AWM CTO              Delivery: Atziri                   │
│                                                                 │
│  Key Outcome: 82% reduction in alert noise, 67% fewer P1s      │
└─────────────────────────────────────────────────────────────────┘
```

### Expanded Per-CTO/CBT Dashboards

Leaderboards and funnels (awareness → trial → active use) by tool and workstream. Each CTO gets a dedicated view showing their portfolio's coverage, effectiveness, and usage trends, drillable to CBT and individual SEAL level.

---

## How the Sections Tell the Story Together

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  "People are using the tools"          ← Section 1: Usage       │
│          │                                                      │
│          ▼                                                      │
│  "Each workstream is delivering"       ← Section 2: Workstreams │
│          │                                                      │
│          ▼                                                      │
│  "SREs are faster and more effective"  ← Section 3: SRE Effect. │
│          │                                                      │
│          ▼                                                      │
│  "Traditional metrics confirm it"      ← Section 4: Support     │
│          │                                                      │
│          ▼                                                      │
│  "And we're growing the foundation"    ← Section 5: Coverage    │
│                                                                 │
│  Together: "Adoption is up, tools are working, SREs are faster, │
│   incidents are down, and coverage is expanding."               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Principles

1. **Show value, don't build new tools.** Everything here uses existing AIOps360 capabilities. The report should demonstrate ROI of what we have.

2. **Avoid misleading averages.** Use distribution bands and medians instead of means. A single outlier P1 can distort an average; bands tell the real story.

3. **Trend over snapshot.** Every metric should be a 12-month rolling trend graph wherever possible. A single number is a data point; a trend is a narrative.

4. **Segment everything by LOB/CTO/CBT/SEAL.** Leadership wants to see their portfolio at every level — from LOB-wide down to individual application. Leaderboards drive healthy competition; SEAL-level drill-down enables targeted action.

5. **True Impact Duration over MTTR.** MTTR is manually tracked and unreliable beyond P1s. True Impact Duration is automatic, precise, and covers all severities. Position MTTR as a supporting data point, not the headline.

6. **Link signals to actions.** The "Are signals being addressed?" metrics (Section 3.2) are arguably the most important. They answer: *does anyone care when UOP shows a problem?*

7. **Scope to pilot apps.** Outcome measures scope is the list of pilot applications where applicable. Don't dilute metrics with apps that aren't onboarded yet.

---

## Metric Ownership

| Section | Report Owners | Data Sources |
|---------|--------------|--------------|
| Overall Usage | Atziri, Souhel, Eric V | DevGPT logs, UOP analytics, MCP request logs |
| Priority Workstreams | Each workstream tech lead | Per-workstream tooling and tracking |
| SRE Effectiveness | Atziri, Souhel, Eric V | UOP signal data (Dynatrace indicators), AIOpsmode logs, Incident Zero |
| Traditional Support | Atziri, Souhel, Eric V | ServiceNow (incidents, MTTR, MTTA, service requests), JIRA |
| SRE Coverage | Atziri, Souhel, Eric V | Dynatrace, SRE telemetry pipelines, UOP config, ERMA/V12 Knowledge Graph |

---

## Next Steps

1. **Data validation:** Confirm data sources exist for each metric — Mike should have AURA/MCP data per CTO/CBT
2. **Baseline establishment:** Pull 2025 baselines for incidents, MTTR, signal counts, and service request volumes for all onboarded applications
3. **JIRA labeling:** Ensure `AIOps360 triggered` label is being applied to relevant JIRAs
4. **Knowledge Graph coverage push:** Prioritize mapping the remaining 71 applications (of 81 total) with component-level data in ERMA/V12 to unlock blast radius analysis
5. **Wireframes:** Use the visuals above as the basis for UOP dashboard wireframes
6. **Day 2 narratives:** Begin collecting before/after stories from each CTO for the first quarterly narrative report
