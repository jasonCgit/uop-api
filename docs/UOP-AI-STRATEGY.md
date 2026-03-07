# UOP Chat and AI Strategy

How UOP positions itself as the enterprise AI surface — consuming AURA, SmartSDK, and third-party MCPs to deliver agentic intelligence across operations, FinOps, developer productivity, and more.

---

## Executive Summary

Multiple teams across the organization are building AI capabilities in silos: FinOps has a Cline mode in VS Code, AURA provides agentic chat via SmartSDK, and individual teams build one-off integrations. UOP is already the platform where SREs, developers, managers, and leadership go for operational intelligence — it should also be the platform where AI meets them.

UOP's AI strategy is built on three principles:

1. **UOP is the surface** — the chat interface, the visualizations, the user relationship. AI backends are pluggable.
2. **AURA is the primary AI backend** — it provides LLM orchestration, MCP tools, IAM, guardrails, and telemetry through Fusion SmartSDK.
3. **Direct SmartSDK is the resilient fallback** — UOP can call SmartSDK independently, ensuring AI capability is never blocked by a single team's availability or roadmap.

This strategy extends to any MCP-based capability — FinOps, Sourcegraph, Bitbucket, Jira, and future integrations — all consumed through UOP's existing streaming chat interface with zero per-user setup.

---

## 1. The Landscape: Who Owns What

| Team | Owns | AI Approach |
|------|------|-------------|
| **FinOps (Mike)** | FinOps MCP, DevGPT Cline modes, cost data | VS Code Cline extension with Sourcegraph MCP — requires per-developer local setup |
| **AURA (Bhargav)** | Agentic AI workflow, SmartSDK agents, MCP orchestration | Centralized AI backend with tool calling, IAM, guardrails |
| **UOP (Jason)** | Unified Operations Platform, chat UI, dashboards, View Central | Platform where all users already are — needs AI integration |
| **SmartSDK (CDAO)** | Fusion SmartSDK framework, Gen AI Gateway | Foundational SDK — available to any team including UOP directly |

### The Strategic Insight

UOP doesn't need to own the AI layer or the data. It needs to own the **delivery surface** — the place where AI capabilities from any team reach users. This makes UOP a force multiplier for every AI initiative, not a competitor.

---

## 2. UOP AI Architecture

### Current State

```
UOP-UI (Browser)
  └── AURA Chat Panel (AuraChatFab → AuraChatPanel)
        │  POST ${API_URL}/api/aura/chat
        ▼
UOP-API (FastAPI)
  └── Keyword-matching mock (aura_data.py)     ◄── 11 hardcoded scenario handlers
        │  returns structured blocks
        ▼
SSE Stream → Rich UI Blocks
  ├── text, metric_cards, table, bar_chart, line_chart
  ├── pie_chart, status_list, recommendations
  └── suggested followups
```

### Target State

```
UOP-UI (Browser)                              ◄── Any user, any browser, no setup
  └── AI Chat Panel
        │
        ├─── Primary: AURA Backend ──────────────────────────────────┐
        │      POST ${AURA_API_URL}/api/aura/chat                   │
        │      └── AURA SmartSDK Agent                               │
        │            ├── LLM (Gen AI Gateway)                        │
        │            ├── Operations MCPs                              │
        │            │     ├── query_incidents (ServiceNow)          │
        │            │     ├── get_metrics (Dynatrace)               │
        │            │     ├── check_slos (SLO store)                │
        │            │     ├── search_graph (ERMA/V12)               │
        │            │     └── get_app_metadata (PATOOLS)            │
        │            ├── FinOps MCPs                                  │
        │            │     ├── query_cost_data                       │
        │            │     ├── get_finops_recommendations            │
        │            │     └── check_graviton_eligibility            │
        │            ├── Developer Productivity MCPs                  │
        │            │     ├── search_code (Sourcegraph)             │
        │            │     ├── create_pull_request (Bitbucket)       │
        │            │     └── create_issue (Jira)                   │
        │            ├── IAM, Guardrails, Telemetry                  │
        │            └── Future MCPs (any team can contribute)       │
        │                                                             │
        └─── Fallback: UOP Direct SmartSDK ──────────────────────────┘
               POST ${SMARTSDK_API_URL}/api/aura/chat
               └── UOP's own SmartSDK Agent → Same MCPs
                     (independently maintained by UOP team)
```

Both backends emit the **identical SSE event format**. The UI cannot tell the difference. The chat panel renders the same blocks regardless of which backend generated them.

---

## 3. Why UOP as the AI Surface

### For Teams Building AI Capabilities (FinOps, Security, Compliance, etc.)

| Without UOP | With UOP |
|-------------|----------|
| Build your own UI or require VS Code + Cline | Your MCP plugs into UOP's existing chat — instant reach |
| Each user must install, configure, and maintain | Zero setup — every UOP user gets your capability |
| Text-only output in terminal | Rich visualizations: charts, tables, metric cards, recommendations |
| No adoption metrics | UOP provides usage analytics, feedback (thumbs up/down), and session data |
| Credential management per user | Single service account, centralized governance |

### For Leadership

| Dimension | Siloed AI (Cline, one-off tools) | UOP-Integrated AI |
|-----------|----------------------------------|-------------------|
| **Reach** | Only users who install specific tools | Every UOP user — developers, SREs, managers |
| **Governance** | No centralized audit trail | Full telemetry, IAM, guardrails per SmartSDK |
| **Cost** | N tools x M users x ungoverned API calls | Centralized rate limiting, single billing path |
| **Consistency** | Different tools give different answers | One platform, one AI surface, consistent experience |
| **Visibility** | Fragmented — each team reports separately | Aggregate analytics across all AI capabilities |

---

## 4. MCP Integration Model

Any team can contribute AI capabilities to UOP by exposing an MCP server. UOP's SmartSDK agent (via AURA or direct) consumes the MCP and renders results through the chat interface.

### How MCPs Plug In

```
Team builds MCP server
  └── Exposes tools via MCP protocol (or HTTP API wrapped as MCP)
        └── Registered in SmartSDK agent's tool list
              └── Agent calls tools based on user intent
                    └── Results rendered as UOP chat blocks
```

### Current and Planned MCP Integrations

| Category | MCP Tools | Source | Status |
|----------|-----------|--------|--------|
| **Operations** | query_incidents, get_metrics, check_slos, search_graph, get_app_metadata, lookup_contacts | AURA / UOP | Documented in SmartSDK guide |
| **FinOps** | query_cost_data, get_finops_recommendations, check_graviton_eligibility, get_spot_candidates, check_lightswitch_status | FinOps Team (Mike) | Available in Cline; needs server-side deployment |
| **Code Intelligence** | search_code, get_file_content, create_batch_change | Sourcegraph | MCP exists; needs service account |
| **Source Control** | create_branch, commit_files, create_pull_request | Bitbucket | Standard API; wrap as MCP tool |
| **Project Tracking** | create_issue, link_to_pr | Jira | Standard API; wrap as MCP tool |
| **Future** | Security scanning, compliance checks, deployment pipelines, capacity forecasting | Various teams | Any team can contribute |

### Mapping MCP Results to Chat Blocks

All MCP data maps to UOP's existing 8 block types — no frontend changes needed per integration:

| Data Pattern | Block Type | Examples |
|-------------|------------|---------|
| KPIs, scores, trends | `metric_cards` | Cost savings, SLO compliance, error rates |
| Tabular data | `table` | Incident lists, cost breakdowns, app inventories |
| Time series | `line_chart` | Spend trends, error rate over time, deployment frequency |
| Comparisons | `bar_chart` | Before/after Graviton, team cost comparison |
| Distributions | `pie_chart` | Cost by service, incidents by category |
| Health/status | `status_list` | App health, migration readiness, SLO status |
| Action items | `recommendations` | Prioritized fixes, cost optimizations, remediation steps |
| Narrative | `text` | Explanations, summaries, analysis |

---

## 5. Case Study: FinOps Integration

The FinOps team's Cline mode illustrates why UOP is the better distribution channel for any AI capability.

### Current: Cline + FinOps MCP

```
Developer's VS Code
  └── Cline (Roo) Extension
        ├── FinOps Mode (DevGPT Marketplace)
        ├── Sourcegraph MCP (scans repos)
        └── LLM → generates code changes locally
```

**Pain points:** Per-developer install, MCP config drift on Cline updates, VS Code only, no governance, manual code push, no org-wide visibility.

### Proposed: UOP + FinOps MCP

```
1. User asks: "What cost optimizations are available for Morgan Money?"
2. AI → FinOps MCP: queries cost data, identifies $45K/month savings
3. AI → Sourcegraph MCP: scans repos for Graviton-incompatible code
4. AI streams to user:
   ├── metric_cards: $45K/month potential savings
   ├── table: Per-service breakdown (Graviton: $20K, Spot: $15K, Lightswitch: $10K)
   ├── recommendations: Prioritized list with effort estimates
   └── followups: "Create PRs for the top 3 recommendations?"
5. User confirms → AI creates Bitbucket PRs + Jira tickets automatically
```

### Complementary Positioning

UOP does not replace Cline — it handles what Cline cannot:

| Use Case | Best Fit | Why |
|----------|----------|-----|
| In-editor suggestions while coding | **Cline** | IDE context, inline changes |
| Org-wide cost analysis for leadership | **UOP** | Rich visualizations, presentation-ready |
| Automated bulk PR creation | **UOP** | Bitbucket + Jira MCP automation |
| Individual developer exploring one service | **Either** | Cline for local flow, UOP for richer analysis |
| Tracking recommendation adoption | **UOP** | Centralized telemetry and Jira integration |

### What the FinOps Team Needs to Do

1. **Make FinOps MCP server-deployable** — currently runs locally with Cline; needs HTTP/gRPC endpoint
2. **Provide connection details** — endpoint URL, auth method, rate limits
3. **Collaborate on prompt tuning** — optimize AURA's system prompt for cost conversations
4. **Validate recommendations** — verify UOP's FinOps answers match Cline's output

If the MCP isn't easily server-deployable, UOP can wrap a REST API as an MCP tool — same result, different plumbing.

---

## 6. Resilient AI Backend Architecture (Internal)

> **Note:** This section is for UOP team internal planning. It should not be shared externally without review.

### Design Principle

UOP's chat interface is **backend-agnostic**. It consumes SSE streams with typed blocks regardless of what generates them. This means UOP can switch AI backends with zero frontend code changes — only a configuration flip.

### Dual-Backend Strategy

| | AURA Backend (Primary) | UOP Direct SmartSDK (Fallback) |
|-|------------------------|-------------------------------|
| **Owner** | Bhargav's team | Jason's team (UOP) |
| **Endpoint** | `${AURA_API_URL}/api/aura/chat` | `${SMARTSDK_API_URL}/api/aura/chat` |
| **How** | AURA's SmartSDK Agent with their MCP ecosystem | UOP's own SmartSDK Agent with same/similar MCPs |
| **SSE format** | Identical | Identical |
| **When** | Default — all traffic | Auto-failover after 3 consecutive AURA failures, or manual switch |

### Runtime Configuration

```javascript
// public/env-config.js — changed at deploy time, no code deploy needed
window.__ENV__ = {
  API_URL: "",
  AURA_BACKEND: "aura",                    // "aura" | "smartsdk"
  AURA_API_URL: "https://aura.internal",   // AURA team's endpoint
  SMARTSDK_API_URL: "",                     // UOP's own SmartSDK endpoint
};
```

```javascript
// src/config.js
export const API_URL = window.__ENV__?.API_URL || '';
export const AURA_BACKEND = window.__ENV__?.AURA_BACKEND || 'aura';
export const AURA_API_URL = window.__ENV__?.AURA_API_URL || API_URL;
export const SMARTSDK_API_URL = window.__ENV__?.SMARTSDK_API_URL || API_URL;
```

### Switching Mechanisms

- **Ops (manual):** Change `AURA_BACKEND` in `env-config.js` — no code deploy, just config update
- **Auto-failover:** `AuraChatContext.jsx` counts consecutive errors. After 3 failures, silently switches to fallback for the session. Page refresh resets to configured primary.
- **Hidden toggle (internal testing):** Click "AURA" header 5 times to reveal Advanced settings with backend switch. Or use `?aura_backend=smartsdk` URL param.
- **Indicator:** Subtitle changes to "AI Assistant (Direct)" when on SmartSDK — subtle, only visible to someone looking for it

### Auto-Failover Logic

```
AuraChatContext.jsx:
  consecutiveErrors = 0

  on sendMessage():
    url = (backend === 'aura') ? AURA_API_URL : SMARTSDK_API_URL
    try:
      stream = POST ${url}/api/aura/chat
      consecutiveErrors = 0
    catch:
      consecutiveErrors++
      if consecutiveErrors >= 3 and fallbackAvailable:
        backend = 'smartsdk'
        retry with new backend
```

### UI Changes Required

| File | Change |
|------|--------|
| `public/env-config.js` | Add `AURA_BACKEND`, `AURA_API_URL`, `SMARTSDK_API_URL` |
| `src/config.js` | Export new env vars with fallback defaults |
| `src/aura/AuraChatContext.jsx` | Backend routing, error counter, auto-fallback, expose `backend` on context |
| `src/aura/AuraChatMenu.jsx` | Hidden Advanced section with backend toggle |

### Why This Matters

| Benefit | Description |
|---------|-------------|
| **No single-team dependency** | UOP's AI isn't blocked by AURA's uptime or roadmap |
| **Resilience** | AURA outage doesn't mean UOP AI goes dark |
| **Independent iteration** | UOP team can test new MCPs on SmartSDK without waiting for AURA releases |
| **Political framing** | Architecture resilience pattern — comparable to a database replica, not a bypass |
| **Zero user impact** | Same chat, same blocks, same experience regardless of active backend |

---

## 7. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| MCPs not server-deployable | Medium | Wrap as HTTP API; UOP creates MCP tool adapter |
| Sourcegraph server-side access | Low | Service account with API token |
| Bitbucket write access concerns | Medium | Guardrails require user confirmation; PRs go through normal review; full audit trail |
| LLM hallucination on data | Medium | MCPs return actual data; AI presents structured blocks, not generated numbers |
| Team resistance to sharing MCPs | Medium | Position UOP as distribution layer that increases their reach — not a competitor |
| AURA dependency risk | Medium | Direct SmartSDK fallback (Section 6) ensures independence |
| SmartSDK not yet in production | Varies | Mock data path works today; SmartSDK integration is incremental |

---

## 8. Implementation Timeline

| Phase | Description | Effort |
|-------|-------------|--------|
| **Phase 1: Mock Demo** | Add FinOps keyword handlers to existing mock data — demonstrates UX immediately | Days |
| **Phase 2: Dual-Backend Config** | Add env-config vars, config exports, and auto-failover logic in AuraChatContext | Days |
| **Phase 3: AURA Integration** | Connect to AURA's SmartSDK endpoint for real AI responses | Weeks |
| **Phase 4: FinOps MCP** | Integrate FinOps MCP (via AURA or direct SmartSDK) for cost data | Weeks (depends on FinOps team) |
| **Phase 5: Developer MCPs** | Add Sourcegraph, Bitbucket, Jira MCPs for code remediation workflow | Weeks |
| **Phase 6: Org-Wide Analytics** | Dashboard widgets for aggregate AI usage, recommendations, adoption rates | Weeks |

Phase 1 and 2 can be delivered immediately — mock FinOps demo + resilient backend architecture.

---

## 9. Summary

UOP's AI strategy is simple: **be the surface, not the engine**.

| Principle | What It Means |
|-----------|---------------|
| **UOP is the surface** | Users come to UOP for AI — not Cline, not a separate AURA portal, not a one-off tool |
| **AURA is the primary engine** | Bhargav's team provides the SmartSDK orchestration, MCPs, IAM, guardrails |
| **SmartSDK is the fallback engine** | UOP can run its own agent if AURA is unavailable or doesn't meet a need |
| **MCPs are pluggable** | Any team can contribute AI capabilities by exposing an MCP — UOP distributes them |
| **The UI is backend-agnostic** | Same chat, same blocks, same experience — regardless of which engine is active |

This positions UOP as a **force multiplier** for every AI initiative in the organization. FinOps reaches more users. AURA gets a high-traffic consumer. Leadership gets centralized governance. And UOP maintains the independence to serve its users regardless of any single team's roadmap.
