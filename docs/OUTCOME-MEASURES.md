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
│  Section 5 │ Baselines & Coverage Roll-up                   │
├─────────────────────────────────────────────────────────────┤
│  Day 2     │ Per-CTO Narratives & Leaderboards              │
└─────────────────────────────────────────────────────────────┘
```

Each section follows the pattern: **headline metric → baseline → trend graph → segmentation → narrative**.

### Report Standards

**Segmentation:** All metrics should be filterable at four levels: **LOB → CTO → CBT → SEAL**. This matches UOP's native filter hierarchy and allows leadership to drill from portfolio-level down to individual application performance.

**Trend:** All trend graphs use a **12-month rolling window** to show seasonality and long-term trajectory.

**Baseline:** Every metric must have a defined baseline — the "before" measurement that all progress is measured against. Baselines are captured from 2025 H1 (pre-AIOps360 full rollout) or from the point of onboarding for each application. Without a baseline, a metric is a data point; with one, it becomes a story of improvement. Section 5 provides the consolidated baseline roll-up across all sections.

---

## Section 1: Overall Usage & Adoption

> **Story:** "People are using our tools and adoption is growing."

This section proves the tools are being used before making any effectiveness claims. Without usage, effectiveness metrics are meaningless.

### 1.1 AI Code Assist (AIOpsmode in DevGPT)

| Metric | Definition | Calculation | Baseline | Visual |
|--------|-----------|-------------|----------|--------|
| Prompt Executions | Volume of AI-assisted code interactions | Count of prompt executions per period | 2025 H1 monthly avg | Area chart, 12-month rolling trend |

### 1.2 UOP Platform

| Metric | Definition | Calculation | Baseline | Visual |
|--------|-----------|-------------|----------|--------|
| Chat Volume | AURA chat interactions within UOP | Count of user prompts to AURA per period | 2025 H1 monthly avg | Area chart, 12-month rolling trend |
| Click Volume | User engagement with UOP dashboards | Count of meaningful clicks/actions per period | 2025 H1 monthly avg | Area chart, 12-month rolling trend |

### 1.3 MCP Server Usage

| Metric | Definition | Calculation | Baseline | Visual |
|--------|-----------|-------------|----------|--------|
| Request Volume | API calls against each MCP server | Count of requests per MCP server per period | First full month per MCP server | Stacked bar chart by MCP server |

### 1.4 Per-CTO/CBT/SEAL Segmentation & Leaderboards

| Metric | Definition | Calculation | Baseline | Visual |
|--------|-----------|-------------|----------|--------|
| Usage by Segment | Adoption volumes broken by LOB/CTO/CBT/SEAL | Sum of events per segment over selected period | 2025 H1 avg per segment | Leaderboard table with sparklines |
| Share Mix | Proportional usage across segments | Percentage of total per LOB/CTO/CBT | 2025 H1 share distribution | Stacked 100% bar or treemap |

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
│ │  base: 4,200  │ │ │  base: 3,800  │ │ │                     │ │
│ └───────────────┘ │ └───────────────┘ │ └─────────────────────┘ │
├───────────────────┴───────────────────┴─────────────────────────┤
│  ADOPTION TREND (12-month rolling)                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │        ╱──────  AI Code Assist                             │ │
│  │   ╱───╱         ───── UOP                                  │ │
│  │  ╱  ╱╱          - - - MCP                                  │ │
│  │ ╱──╱             · · · Baseline                            │ │
│  │╱─╱ ··········································              │ │
│  ├────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┤ │
│  │ Apr│ May│ Jun│ Jul│ Aug│ Sep│ Oct│ Nov│ Dec│ Jan│ Feb│ Mar │ │
│  │         2025                                     2026      │ │
│  └────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────┤
│  LEADERBOARD — Per CTO / CBT                                   │
│  ┌────────────────────┬──────┬──────┬──────┬──────────────────┐ │
│  │ CTO / CBT           │ AIOps│  UOP │  MCP │ Trend vs Base    │ │
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

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Prompt Executions | Usage | Volume in DevGPT against Zero-Touch M&O MCP | Count per period | First full month of MCP availability |
| Dynatrace & Golden Signal Coverage | Coverage | Uplift on Day 1 Deliverables (Dynatrace instrumentation + Golden Signals) | % onboarded vs target; trend | % at program kickoff (2025 H1) |
| Net $ Savings | Cost | Resource time saved through automation | Hours saved × blended rate | $0 (pre-automation manual effort as reference) |

### 2.2 SRE Telemetry

*Owners: Aarushi (Tech), Aarushi (Delivery), Jason (Owner)*

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Prompt Executions | Usage | Volume in DevGPT against SRE Telemetry MCP | Count per period | First full month of MCP availability |
| UOP Onboarding & SLOs | Coverage | Uplift on Day 1 Deliverables (UOP signal setup + SLO definition) | Apps onboarded vs target; trend | App count at program kickoff |
| Net $ Savings | Cost | Resource time saved | Hours saved × blended rate | $0 (pre-automation manual effort as reference) |

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

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Application Graph Coverage | Coverage | % of onboarded applications with component-level mappings in the Knowledge Graph | (SEALs with component mappings / total onboarded SEALs) × 100 | 10 of 81 apps (12%) at initial measurement |
| Dependency Completeness | Coverage | Component-to-component dependency edges mapped per application | Count of edges per SEAL; track trend as new dependencies are discovered and mapped | Edge count at initial graph load from ERMA/V12 |
| Cross-SEAL Dependencies Mapped | Coverage | Cross-application upstream/downstream relationships captured | Count of external/cross-SEAL dependency edges; trend | Count at initial graph load |
| Blast Radius Queries | Usage | Number of blast radius and dependency lookups performed by users | Count of `/api/graph/blast-radius/` and `/api/graph/dependencies/` requests per period | First full month of feature availability |
| Impact Prediction Accuracy | Effectiveness | When an incident occurs, did the blast radius correctly predict impacted components? | % of incident-affected components that were in the blast radius path of the root cause component | First quarter of measured incidents post-launch |

### 2.4 Alert Severity Solution

*Owners: Eric D (Tech), Atziri (Delivery), Bhargav (Owner)*

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Open Incident Duration | Effectiveness | Track open incident duration vs baseline | Rapid Response-created incidents; compare against avg baseline | 2025 H1 avg open duration per severity |
| RED Alert Reduction | Effectiveness | Reduction in RED alerts for apps in scope | Count RED alerts vs pre-period baseline | 2025 H1 monthly avg RED alerts |
| RED Alert Accuracy | Effectiveness | Do RED alerts correspond to real P1/P2 incidents? | % of RED alerts with matching P1/P2; % of P1/P2s with matching RED alert | First quarter of correlation measurement |
| Net $ Savings | Cost | Resource time saved from alert noise reduction | Hours saved × blended rate | $0 (pre-filtering manual triage effort as reference) |
| AURA Noise Filtering Rate | Effectiveness | Suppression rate = suppressed / total raw alerts | Count of alerts suppressed by AURA ÷ raw alert count per period; report by app and aggregate | 0% (pre-AURA: no suppression) |
| UOP Precision Trend | Effectiveness | % of UOP alerts that lead to action (click, AIOps inquiry, incident linkage) | Alerts with any correlated action ÷ total UOP alerts per period | First full month of action tracking |
| SRE Toil Reduction | Operational | Actionable alerts per on-call per week + after-hours pages per week | Count of actionable alerts/pages allocated to on-call schedules | 2025 H1 avg alerts per on-call per week |
| P1/P2 Incident Reduction | Effectiveness | Reduction in P1 and P2 incidents for apps in scope | Count of P1/P2 incidents per period vs baseline; sourced from ServiceNow `p1_30d` and `p2_30d` fields; report by LOB/CTO/CBT/SEAL | 2025 H1 monthly avg P1/P2 counts per SEAL |
| Service Request Reduction | Effectiveness | Reduction in ESD service requests for apps in scope | Count of service requests per period vs baseline; segmented by request type and LOB/CTO/CBT/SEAL | 2025 H1 monthly avg service requests per SEAL |

### 2.5 AURA — Central Orchestration Engine

*Owners: Shravan (Tech), Jose (AIOpsmode) / Atziri (UOP) (Delivery), Bhargav (Owner)*

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Anomalies & RCAs Produced | Productivity | Volume of automated analysis outputs | Count per period | First full month of AURA production |
| AIOpsmode Prompts | Usage | Prompts + code updates in DevGPT | Volume per period | First full month of AIOpsmode availability |
| UOP Requests | Usage | User requests to AURA (Chat and non-Chat) | Count per period | First full month of AURA in UOP |
| Incidents Avoided | Effectiveness | Proactive catches that prevented production impact | Number of code updates correlated to anomaly detection | 0 (pre-AURA: no proactive detection) |
| Anomaly Trends | Effectiveness | Volume trend of anomalies detected | Count per period; trend line | First full month of anomaly detection |
| Change-Aware Anomaly Rate | Effectiveness | Anomalies per 100 changes — contextualizes stability vs pace of change | (Total anomalies ÷ total code changes or deployments in same period) × 100 | First quarter of combined anomaly + deployment data |

### 2.6 Resiliency AI Chaos Simulator

*Owners: Jose (Tech), Jose (Delivery), Eric V/Adam (Owners)*

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Simulations Executed | Usage | Volume of chaos simulations run | Count per period | First full month of simulator availability |
| Issues Identified | Effectiveness | Issues found & remediated in UAT and Prod | Count; UAT vs Prod breakdown | First quarter of simulation results |
| Team Adoption | Effectiveness | Teams running actual chaos engineering | Count of teams with executions in UAT & Prod | 0 teams (pre-launch) |

### 2.7 Individual AO Comms Actionable Insights

*Owners: Animesh (Tech), Jose (Delivery), Bhargav/Ray (Owners)*

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Prompt Executions | Usage | Volume in DevGPT against AOComms MCP | Count per period | First full month of MCP availability |
| Net $ Savings | Cost | Resource time saved | Hours saved × blended rate | $0 (pre-automation manual effort as reference) |

### 2.8 FinOps Cost Optimization

*Owners: Vamsi (Tech), Atziri (Delivery), Mike/Ray (Owners)*

| Metric | Type | Definition | Calculation | Baseline |
|--------|------|-----------|-------------|----------|
| Prompt Executions | Usage | Volume in DevGPT against FinOps MCP | Count per period | First full month of MCP availability |
| Savings Identified | Cost | Potential $ savings surfaced by tool | Total $ save identified | $0 (pre-tool: no automated identification) |
| Savings Executed | Cost | Actual $ savings realized | Total $ save executed | $0 (pre-tool) |

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
│  │ base: 0% / $0     │  │ base: 0% / $0     │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                 │
│  ┌─ Alert Severity ──┐  ┌─ AURA Engine ──────┐                 │
│  │ RED Alerts  -31%   │  │ Anomalies   1,247  │                 │
│  │ Precision    78%   │  │ RCAs          892  │                 │
│  │ P1s        -28%   │  │ Change Rate  3.2%  │                 │
│  │ P2s        -18%   │  │ Incidents     -18  │                 │
│  │ Svc Reqs   -12%   │  │                     │                 │
│  │ Noise Filt.  84%   │  │ (all vs baseline)  │                 │
│  │ (all vs baseline)  │  │                     │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                 │
│  ┌─ Blast Radius ────┐  ┌─ FinOps ───────────┐                 │
│  │ Graph Cov.  12%    │  │ Identified  $1.2M  │                 │
│  │ Deps Mapped 247    │  │ Executed     $840k │                 │
│  │ X-SEAL Deps  34    │  │ base: $0 / $0     │                 │
│  │ Queries    1,820   │  │                     │                 │
│  │ base: 10 apps/12% │  │                     │                 │
│  └────────────────────┘  └────────────────────┘                 │
│                                                                 │
│  ALERT SEVERITY — NOISE REDUCTION TREND (12-month rolling)      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Raw Alerts   ████████████████████████████████  12,400      │ │
│  │ After AURA   ████████████░░░░░░░░░░░░░░░░░░░   4,200      │ │
│  │ Actioned     ██████░░░░░░░░░░░░░░░░░░░░░░░░░   2,100      │ │
│  │                                                            │ │
│  │              66% suppressed          50% actioned          │ │
│  │              base: 0% suppressed     base: N/A             │ │
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
│  │  ··········· baseline P2 ·······························   │ │
│  │  ··········· baseline P1 ·······························   │ │
│  │              Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec   │ │
│  │              Jan  Feb  Mar                                 │ │
│  │              2025                                    2026  │ │
│  │                                                            │ │
│  │  P1: 12 this period (▼ 28% vs baseline 17)               │ │
│  │  P2: 47 this period (▼ 18% vs baseline 57)               │ │
│  │  Svc Requests: 184 (▼ 12% vs baseline 209)               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  AURA — CHANGE-AWARE ANOMALY RATE (12-month rolling)            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Anomalies                                                 │ │
│  │  per 100     5 │     ╲                                     │ │
│  │  changes     4 │      ╲___                                 │ │
│  │              3 │ ·········· baseline (4.8) ·············   │ │
│  │              2 │          ╲___╱╲                            │ │
│  │              1 │                ╲___                        │ │
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

**Baseline:** 2025 H1 median impact duration per severity, per LOB/CTO/CBT/SEAL. This is the reference point for all "faster" claims.

**Distribution Bands** (measured against baseline):

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
│  ┌─ Distribution Bands (vs 2025 H1 baseline) ────────────┐     │
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
│  │            100 │  ╲  ······ baseline: 98 min ·········   │   │
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

**Baseline:** 2025 H1 median latency per channel, per LOB/CTO/CBT/SEAL.

| Channel | What to Measure | Calculation | Baseline |
|---------|----------------|-------------|----------|
| UOP | Signal appeared in UOP → user clicked on it | `timestamp(first UOP click) - timestamp(signal created)` | 2025 H1 median click latency |
| AIOps/IDE | Signal appeared → first AIOps or IDE inquiry about it | `timestamp(first IDE inquiry) - timestamp(signal created)` | 2025 H1 median inquiry latency |
| Incident Zero | Signal has a corresponding Incident Zero entry by SRE (error budget / burn rate tracked) | % of signals with matching Incident Zero record; median time from signal to entry | 2025 H1 % coverage and median latency |

#### 3.2a Time from Signal to First Action (Latency to Engagement)

**Definition:** Time from signal appearance to first user action (UOP click) or first AIOps/IDE inquiry.

**Reporting:** Medians and bands (% within 5m / 30m / 2h / 8h), segmented by LOB/CTO/CBT/SEAL. Compare band distribution against baseline to show shift toward faster response.

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

**Baseline:** 2025 H1 % of signals with Incident Zero entries and median latency.

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
│  │  │  base:  12 min   │    │  base:   37 min  │            │   │
│  │  │  ▼ 34% from base │    │  ▼ 41% from base │            │   │
│  │  └──────────────────┘    └──────────────────┘            │   │
│  │                                                          │   │
│  │  < 5 min   ██████████████████████████████░░░░░  62%      │   │
│  │  5-30 min  █████████░░░░░░░░░░░░░░░░░░░░░░░░░  22%      │   │
│  │  30m-2hr   ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10%      │   │
│  │  2-8hr     ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   4%      │   │
│  │  > 8hr     █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2%      │   │
│  │            (base: 38% / 28% / 18% / 10% / 6%)           │   │
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

| Tool | Metric | Calculation | Baseline |
|------|--------|-------------|----------|
| AIOpsmode | Unique users & sessions | Count distinct users and sessions per period | 2025 H1 monthly avg unique users |
| MCPs | Unique users & sessions per MCP | Count distinct users and sessions per MCP per period | First full month per MCP |
| UOP | Unique users & sessions | Count distinct users and sessions per period | 2025 H1 monthly avg unique users |

**Per-CTO/CBT/SEAL Segmentation**: Show adoption and active-use rates. Funnel view: awareness → trial → active use. Compare funnel conversion rates against baseline.

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
│  │                                 45% active (base: 28%)  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  AWM — Connect Platform (CBT: Jon Glennie)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Aware (onboarded)  ████████████████████████████████  128│   │
│  │  Trial (1-3 uses)   ████████████████████████░░░░░░░░  108│   │
│  │  Active (weekly)    █████████████████░░░░░░░░░░░░░░░   82│   │
│  │                                 64% active (base: 41%)  │   │
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

**Baseline:** 2025 H1 monthly avg incident count per severity, per LOB/CTO/CBT/SEAL. This is the "before AIOps360" reference for all applications onboarded at that time; apps onboarded later use their first full month.

**What to show:**
- Baseline reference line on every incident trend chart
- P1/P2 reduction trend vs baseline tells the proactive prevention story
- Service request reduction vs baseline tells the TechSupport agent scope story
- Segment by LOB/CTO/CBT/SEAL to show which teams are driving improvement

### 4.2 MTTR by Severity

**Definition:** Mean time to resolve per severity, per period.

**Calculation:** Average incident resolution time by severity; show distribution and medians. Sourced from ServiceNow (MTTR, MTTA, resolution_rate, escalation_rate already tracked in UOP dashboard data).

**Baseline:** 2025 H1 median MTTR per severity, per LOB/CTO/CBT/SEAL.

**Caveats to communicate:**
- MTTR is manually tracked and is only accurate for P1s
- For other priorities it is less reliable
- Ticket MTTR (resolution time - opening time) can supplement but doesn't tell the full story
- **True Impact Duration (Section 3.1) is the recommended primary metric** for measuring actual resolution speed

### 4.3 Proactive Incidence Prevention (AIOps360-Triggered)

**Definition:** JIRAs (fixes) going to production on the back of an AIOps360 trigger should carry an `AIOps360 triggered` label.

**Calculation:** Count of JIRAs with `AIOps360 triggered` label per period. Link anomalies to PRs/fixes. Segment by LOB/CTO/CBT/SEAL.

**Baseline:** 0 JIRAs (pre-AIOps360: no automated triggers existed).

### 4.4 Service Request Volume & Reduction

**Definition:** Count of ESD service requests per period for onboarded applications.

**Calculation:** Time series of service request volume by request type. Compare against baseline to show self-service deflection.

**Baseline:** 2025 H1 monthly avg service request volume per request type, per LOB/CTO/CBT/SEAL.

**What to show:**
- Total service request volume trend (12-month rolling) with baseline reference line
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
│  │           50 │  ╲  P2  ····· P2 baseline (57) ·······   │   │
│  │           25 │───╲──────────────── P1                    │   │
│  │           15 │ ·········· P1 baseline (17) ···········   │   │
│  │            0 ├──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──       │   │
│  │               A  M  J  J  A  S  O  N  D  J  F  M        │   │
│  │               2025                           2026        │   │
│  │                                                          │   │
│  │  P1: 12 (▼ 28% vs base 17)  P2: 47 (▼ 18% vs base 57) │   │
│  │  P3+: 124 (▼ 8%)   Svc Requests: 184 (▼ 12% vs 209)   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─ MTTR by Severity (vs baseline) ───────────────────────┐     │
│  │                                                          │   │
│  │  P1  ████████████████░░░░░░░░░░░░░░░  42 min (▼ 22%)    │   │
│  │      base: 54 min                                        │   │
│  │  P2  ██████████████████████░░░░░░░░░  68 min (▼ 14%)    │   │
│  │      base: 79 min                                        │   │
│  │  P3  ████████████████████████████░░░  118 min (▼ 6%)    │   │
│  │      base: 126 min                                       │   │
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
│  │  baseline: 0 (pre-AIOps360)                              │   │
│  │                                                          │   │
│  │  "Proactive fixes going to prod before customer impact"  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Drill-down: [LOB ▾]  [CTO ▾]  [CBT ▾]  [SEAL ▾]              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Section 5: Baselines & Coverage Roll-up

> **Story:** "Here is exactly where we started, where we stand on coverage, and the foundation everything else is measured against."

This section serves two purposes: (1) it consolidates all baselines from Sections 1–4 into one reference view so leadership can see the "before" picture at a glance, and (2) it tracks coverage — because without coverage, effectiveness metrics only apply to a subset of the portfolio.

### 5.1 Baseline Summary

Every metric in Sections 1–4 has a defined baseline. This table provides the consolidated view:

| Section | Metric | Baseline Value | Baseline Period | Source |
|---------|--------|---------------|-----------------|--------|
| 1.1 | AI Code Assist Prompts | Monthly avg | 2025 H1 | DevGPT logs |
| 1.2 | UOP Chat Volume | Monthly avg | 2025 H1 | UOP analytics |
| 1.2 | UOP Click Volume | Monthly avg | 2025 H1 | UOP analytics |
| 1.3 | MCP Request Volume | First full month per MCP | Per MCP launch | MCP request logs |
| 2.1 | Dynatrace Coverage | % at kickoff | 2025 H1 | Dynatrace |
| 2.2 | UOP/SLO Onboarding | App count at kickoff | 2025 H1 | UOP config |
| 2.3 | Knowledge Graph Coverage | 10 of 81 apps (12%) | Initial measurement | ERMA/V12 |
| 2.4 | RED Alert Count | Monthly avg | 2025 H1 | UOP signal data |
| 2.4 | P1/P2 Incident Count | Monthly avg per SEAL | 2025 H1 | ServiceNow |
| 2.4 | Service Request Count | Monthly avg per SEAL | 2025 H1 | ServiceNow |
| 2.4 | SRE Toil (alerts/on-call/wk) | Weekly avg | 2025 H1 | On-call schedules |
| 2.5 | Anomalies & RCAs | First full month | AURA launch | AURA |
| 3.1 | True Impact Duration | Median per severity | 2025 H1 | Dynatrace indicators |
| 3.2 | Signal-to-Action Latency | Median per channel | 2025 H1 | UOP analytics |
| 3.2 | Incident Zero Coverage | % of signals with IZ entry | 2025 H1 | Incident Zero |
| 3.3 | Unique Users per Tool | Monthly avg | 2025 H1 | UOP/DevGPT/MCP logs |
| 4.1 | Incident Count by Severity | Monthly avg per severity | 2025 H1 | ServiceNow |
| 4.2 | MTTR by Severity | Median per severity | 2025 H1 | ServiceNow |
| 4.4 | Service Request Volume | Monthly avg per type | 2025 H1 | ServiceNow |

### 5.2 Coverage Roll-up

Coverage tracks how much of the portfolio is onboarded to each layer. Without coverage, effectiveness metrics only apply to a subset.

#### Dynatrace Coverage

**Definition:** % of pilot apps onboarded to Dynatrace with Golden Signals configured.

**Calculation:** (Apps onboarded with Golden Signals / total pilot apps) × 100; show trend and count.

**Baseline:** % at program kickoff (2025 H1). **Segmentation:** By LOB/CTO/CBT/SEAL.

#### SRE Telemetry Coverage

**Definition:** % of pilot apps with SRE telemetry integrated into agreed dashboards/data pipelines.

**Calculation:** (Apps with SRE telemetry live / total pilot apps) × 100.

**Baseline:** % at program kickoff (2025 H1). **Segmentation:** By LOB/CTO/CBT; show gaps and target dates.

#### UOP Coverage

**Definition:** % of pilot apps with UOP signals and SLOs configured and active.

**Calculation:** (Apps with UOP signals & SLOs / total pilot apps) × 100. Measurable from UOP's completeness score (`has_slo`, `has_sla`, `has_blast_radius` fields).

**Baseline:** % at program kickoff (2025 H1). **Segmentation:** By LOB/CTO/CBT/SEAL; include SLOs defined vs. in-progress.

#### Knowledge Graph Coverage

**Definition:** % of pilot apps with component-level mappings in the Knowledge Graph.

**Calculation:** (SEALs with component mappings / total pilot apps) × 100. Currently 10 of 81 applications have component data mapped. This is the foundation for blast radius analysis — apps without graph data cannot benefit from dependency-aware alerting.

**Baseline:** 10 of 81 apps (12%) at initial measurement. **Segmentation:** By LOB/CTO/CBT; show gap count and target dates.

**Visual — Baselines & Coverage:**

```
┌─────────────────────────────────────────────────────────────────┐
│  BASELINES & COVERAGE ROLL-UP                                   │
│  "Where did we start, and where do we stand today?"             │
│                                                                 │
│  ┌─ Key Baselines vs Current ─────────────────────────────┐     │
│  │                                                          │   │
│  │  Metric               │ Baseline │ Current  │ Change     │   │
│  │  ─────────────────────┼──────────┼──────────┼──────────  │   │
│  │  True Impact Duration │  98 min  │  42 min  │ ▼ 57%     │   │
│  │  Signal-to-Action     │  12 min  │   8 min  │ ▼ 34%     │   │
│  │  P1 Incidents/mo      │    17    │    12    │ ▼ 28%     │   │
│  │  P2 Incidents/mo      │    57    │    47    │ ▼ 18%     │   │
│  │  Svc Requests/mo      │   209    │   184    │ ▼ 12%     │   │
│  │  AURA Noise Filter    │    0%    │   66%    │ ▲ 66pp    │   │
│  │  IZ Signal Coverage   │   58%    │   72%    │ ▲ 14pp    │   │
│  │  Active Tool Users    │   180    │   412    │ ▲ 129%    │   │
│  │                                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
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
│  │     base: 52%      base: 38%    base: 22%  base: 12%    │   │
│  │     ▲ 26pp         ▲ 26pp       ▲ 30pp     baseline     │   │
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
| **Baseline** | Specific metrics before intervention (from Section 5.1 baseline data) |
| **Metrics Impact** | Usage, time-to-action, anomalies per 100 changes, incidents avoided, toil reduction |
| **Time Horizon** | Measurement period |
| **Owners** | CTO, delivery lead, tech lead |

**Example Narrative:**

```
┌─────────────────────────────────────────────────────────────────┐
│  USE CASE: AWM — Automated Anomaly Detection                    │
│                                                                 │
│  BEFORE (baseline)                  AFTER (current)             │
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

Leaderboards and funnels (awareness → trial → active use) by tool and workstream. Each CTO gets a dedicated view showing their portfolio's coverage, effectiveness, and usage trends, drillable to CBT and individual SEAL level. All metrics shown against their respective baselines.

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
│  "Here's where we started and         ← Section 5: Baselines    │
│   how far we've come"                    & Coverage              │
│                                                                 │
│  Together: "Adoption is up, tools are working, SREs are faster, │
│   incidents are down, coverage is expanding — all measured       │
│   against defined baselines."                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Principles

1. **Show value, don't build new tools.** Everything here uses existing AIOps360 capabilities. The report should demonstrate ROI of what we have.

2. **Avoid misleading averages.** Use distribution bands and medians instead of means. A single outlier P1 can distort an average; bands tell the real story.

3. **Trend over snapshot.** Every metric should be a 12-month rolling trend graph wherever possible. A single number is a data point; a trend is a narrative.

4. **Baseline everything.** Every metric must have a defined "before" measurement. Without a baseline, improvement claims are unsubstantiated. Baselines come from 2025 H1 or from onboarding date for later additions.

5. **Segment everything by LOB/CTO/CBT/SEAL.** Leadership wants to see their portfolio at every level — from LOB-wide down to individual application. Leaderboards drive healthy competition; SEAL-level drill-down enables targeted action.

6. **True Impact Duration over MTTR.** MTTR is manually tracked and unreliable beyond P1s. True Impact Duration is automatic, precise, and covers all severities. Position MTTR as a supporting data point, not the headline.

7. **Link signals to actions.** The "Are signals being addressed?" metrics (Section 3.2) are arguably the most important. They answer: *does anyone care when UOP shows a problem?*

8. **Scope to pilot apps.** Outcome measures scope is the list of pilot applications where applicable. Don't dilute metrics with apps that aren't onboarded yet.

---

## Metric Ownership

| Section | Report Owners | Data Sources |
|---------|--------------|--------------|
| Overall Usage | Atziri, Souhel, Eric V | DevGPT logs, UOP analytics, MCP request logs |
| Priority Workstreams | Each workstream tech lead | Per-workstream tooling and tracking |
| SRE Effectiveness | Atziri, Souhel, Eric V | UOP signal data (Dynatrace indicators), AIOpsmode logs, Incident Zero |
| Traditional Support | Atziri, Souhel, Eric V | ServiceNow (incidents, MTTR, MTTA, service requests), JIRA |
| Baselines & Coverage | Atziri, Souhel, Eric V | All sources above; Dynatrace, SRE telemetry pipelines, UOP config, ERMA/V12 Knowledge Graph |

---

## Next Steps

1. **Baseline capture (critical path):** Pull 2025 H1 baselines for every metric in Section 5.1 — incidents, MTTR, signal durations, service requests, usage volumes, and coverage percentages. This is the single most important deliverable; without baselines, the report cannot show improvement.
2. **Data validation:** Confirm data sources exist for each metric — Mike should have AURA/MCP data per CTO/CBT
3. **JIRA labeling:** Ensure `AIOps360 triggered` label is being applied to relevant JIRAs
4. **Knowledge Graph coverage push:** Prioritize mapping the remaining 71 applications (of 81 total) with component-level data in ERMA/V12 to unlock blast radius analysis
5. **Wireframes:** Use the visuals above as the basis for UOP dashboard wireframes
6. **Day 2 narratives:** Begin collecting before/after stories from each CTO for the first quarterly narrative report
