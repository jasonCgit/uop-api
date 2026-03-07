# AURA as the Enterprise FinOps AI Integration Point

Why centralized agentic AI through UOP is the better path for FinOps cost optimization — versus requiring every developer to run local VS Code tooling.

---

## Executive Summary

The FinOps team has built a V1 cost optimization mode in the DevGPT Cline (Roo) Marketplace that recommends Graviton migration, Spot Instance usage, Lightswitch adoption, and other savings to developers through VS Code. This approach requires every developer to install Cline, configure MCP connections to Sourcegraph and FinOps data, and maintain those configurations across Cline updates.

UOP's AURA already provides an AI chat interface with streaming responses, rich visualizations (tables, charts, metric cards, recommendations), and a documented agentic architecture (Fusion SmartSDK) designed for exactly this kind of MCP tool integration. By connecting the FinOps MCP to AURA instead of (or in addition to) Cline, the organization gets centralized governance, zero per-developer setup, richer output, and an automated code remediation pipeline through Bitbucket and Jira — all through a platform every operations user already accesses.

---

## 1. Current State: Cline + FinOps MCP

### How It Works Today

```
Developer's VS Code
  └── Cline (Roo) Extension
        ├── FinOps Mode (from DevGPT Marketplace)
        │     └── Recommendations: Graviton, Spot, Lightswitch, etc.
        ├── Sourcegraph MCP
        │     └── Scans developer's codebase for optimization targets
        └── LLM (via Cline's configured model)
              └── Generates code changes locally
```

The developer asks a question like "How can I reduce costs for my service?" — Cline uses Sourcegraph MCP to scan their repo, queries FinOps data, and suggests code changes that the developer applies locally and pushes.

### Pain Points

| Issue | Impact |
|-------|--------|
| **Per-developer installation** | Every developer must install and configure Cline + MCPs in VS Code |
| **MCP configuration drift** | Cline updates frequently break MCP server configurations; developers must re-configure |
| **VS Code dependency** | Only reaches developers using VS Code with Cline — excludes IntelliJ users, managers, SREs, and operations staff |
| **No centralized governance** | No audit trail of what recommendations were given, no rate limiting, no guardrails |
| **Credential sprawl** | Each developer needs their own API keys/tokens for Sourcegraph and FinOps data |
| **Inconsistent recommendations** | Different Cline versions or MCP configs can produce different advice for the same codebase |
| **Manual code application** | Developer must manually review, apply, commit, and push changes — no automation |
| **No org-wide visibility** | Leadership cannot see aggregate FinOps recommendations or adoption rates |

---

## 2. Proposed State: AURA + FinOps MCP

### Architecture

```
UOP-UI (Browser)                          ◄── Any user, any browser, no setup
  └── AURA Chat Panel
        │  POST /api/aura/chat
        ▼
UOP-API (FastAPI)
  └── Fusion SmartSDK Agent
        ├── LLM (via Gen AI Gateway)      ◄── Centralized, governed, audited
        ├── FinOps MCP                    ◄── Cost data, recommendations, Graviton eligibility
        ├── Sourcegraph MCP               ◄── Code search, batch changes across repos
        ├── Bitbucket MCP                 ◄── Create branches, commit changes, open PRs
        ├── Jira MCP                      ◄── Create tracking tickets linked to PRs
        ├── Existing UOP MCPs             ◄── ServiceNow, Dynatrace, ERMA, PATOOLS
        ├── IAM (JPMC auth)               ◄── User identity, permissions
        ├── Guardrails                    ◄── PII filtering, content safety, tool limits
        └── Telemetry                     ◄── Full audit trail of every query and action
              │
              ▼
SSE Stream → Rich UI Blocks
  ├── text          → Markdown explanations
  ├── metric_cards  → Cost savings KPIs with sparklines
  ├── table         → Per-service cost breakdowns
  ├── bar_chart     → Cost comparison before/after Graviton
  ├── line_chart    → Spend trends over time
  ├── pie_chart     → Cost distribution by service/team
  ├── status_list   → Migration readiness per application
  └── recommendations → Prioritized cost actions with expected savings
```

### What Already Exists in AURA

AURA's infrastructure is built and ready for this integration:

- **SSE streaming chat** with structured block rendering (8 block types including tables, charts, metric cards, and recommendation lists)
- **SmartSDK integration path** fully documented with MCP tool definition patterns, agent configuration, IAM, guardrails, and telemetry
- **Session persistence** with chat history, feedback capture (thumbs up/down), and suggested follow-ups
- **No frontend changes needed** — the React UI renders any block the backend streams, regardless of whether it comes from incident data or FinOps data

---

## 3. Why AURA Is Better

| Dimension | Cline (Local) | AURA (Centralized) |
|-----------|---------------|---------------------|
| **Reach** | VS Code + Cline users only | Every UOP user — developers, SREs, managers, leadership |
| **Setup** | Install Cline, configure MCPs per developer | Zero setup — open UOP, ask AURA |
| **Maintenance** | Each developer maintains their own MCP configs; breaks on Cline updates | One server-side config maintained by platform team |
| **Governance** | No audit trail, no rate limiting | Full telemetry, audit logging, guardrails, IAM |
| **Credentials** | Per-developer API keys for Sourcegraph, FinOps data | Single service account with proper access controls |
| **Consistency** | Version drift across developer machines | Same model, same tools, same recommendations for everyone |
| **Output quality** | Text-only in terminal | Rich visualizations: charts, tables, metric cards, status lists |
| **Code remediation** | Developer manually applies changes and pushes | Automated: AURA creates Bitbucket PRs + Jira tickets |
| **Org visibility** | None — each developer's session is local | Aggregate analytics on recommendations given, savings identified, PRs created |
| **Cost control** | N developers x M API calls = ungoverned spend | Centralized rate limiting, single billing path |

---

## 4. Code Remediation Workflow: Cline vs. AURA

### Cline Workflow (Today)

```
1. Developer asks Cline about cost savings
2. Cline → Sourcegraph MCP scans local repo
3. Cline suggests code changes in VS Code
4. Developer reviews changes in editor
5. Developer commits and pushes manually
6. Developer creates Jira ticket manually (maybe)
7. PR goes through normal review process
```

**Gaps:** Steps 5-6 are manual, often skipped. No tracking of which recommendations were acted on.

### AURA Workflow (Proposed)

```
1. User asks AURA: "What cost optimizations are available for Morgan Money?"
2. AURA → FinOps MCP: queries cost data, identifies savings opportunities
3. AURA → Sourcegraph MCP: scans Morgan Money repos for Graviton-incompatible code,
   non-Spot instance configs, Lightswitch candidates
4. AURA streams results to user:
   ├── metric_cards: $45K/month potential savings identified
   ├── table: Per-service breakdown (Graviton: $20K, Spot: $15K, Lightswitch: $10K)
   ├── recommendations: Prioritized list with effort estimates
   └── followups: "Create PRs for the top 3 recommendations?"
5. User confirms: "Yes, create PRs for the Graviton changes"
6. AURA → Sourcegraph MCP: generates code patches via batch changes
7. AURA → Bitbucket MCP: creates branch, commits changes, opens PR
8. AURA → Jira MCP: creates ticket linked to PR with cost impact details
9. AURA streams confirmation:
   ├── status_list: PR #1234 created, JIRA-5678 created
   └── text: "PR is ready for review. Expected savings: $20K/month"
```

**Advantages:** Fully automated from analysis to PR. Complete audit trail. User confirms before any write action (guardrail). Jira ticket ensures tracking.

---

## 5. Integration Architecture: MCP Tool Definitions

These tools follow the same pattern already documented in UOP's SmartSDK integration guide (`docs/SMARTSDK-INTEGRATION.md`) and would be added alongside the existing tool set.

### FinOps MCP Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `query_cost_data` | Retrieve cloud spend by service, team, or account | service_name, team, time_range, granularity |
| `get_finops_recommendations` | Get cost optimization recommendations | app_name, category (graviton/spot/lightswitch/reserved), min_savings |
| `check_graviton_eligibility` | Assess Graviton migration readiness for a service | app_name, include_dependencies |
| `get_spot_candidates` | Identify workloads suitable for Spot Instances | app_name, fault_tolerance_required |
| `check_lightswitch_status` | Check if non-prod environments are Lightswitch-enabled | app_name, environment |

### Sourcegraph MCP Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `search_code` | Search across repositories for patterns | query, repo_filter, language, limit |
| `get_file_content` | Retrieve specific file content from a repo | repo, file_path, branch |
| `create_batch_change` | Generate code patches across multiple repos | change_spec, repo_filter, commit_message |

### Bitbucket MCP Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `create_branch` | Create a new branch in a repository | repo, branch_name, source_branch |
| `commit_files` | Commit file changes to a branch | repo, branch, files[], commit_message |
| `create_pull_request` | Open a PR with description and reviewers | repo, source_branch, target_branch, title, description, reviewers[] |

### Jira MCP Tools

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `create_issue` | Create a Jira ticket | project, issue_type, summary, description, labels[], priority |
| `link_to_pr` | Link a Jira issue to a Bitbucket PR | issue_key, pr_url, link_type |

### Mapping to AURA's Existing Block Types

All FinOps data maps naturally to AURA's existing UI block renderers — no frontend work needed:

| FinOps Data | Block Type | Example |
|-------------|------------|---------|
| Monthly spend, savings potential | `metric_cards` | KPI cards with sparklines showing spend trends |
| Per-service cost breakdown | `table` | Sortable table: service, current cost, savings, effort |
| Cost trends over time | `line_chart` | 12-month spend with projected savings overlay |
| Spend by category | `pie_chart` | Compute vs. storage vs. network vs. data transfer |
| Before/after Graviton | `bar_chart` | Current x86 cost vs. projected Graviton cost |
| Migration readiness | `status_list` | Green/amber/red per service |
| Prioritized actions | `recommendations` | Ranked by savings with effort level and links to PRs |

---

## 6. What the FinOps Team Needs to Do

### Option A: Expose FinOps Data as MCP Server (Preferred)

If the FinOps team already has their data accessible via MCP for Cline, the same MCP server can be consumed by AURA's SmartSDK agent on the server side. The team needs to:

1. **Make the MCP server network-accessible** — currently it may run locally with Cline; it needs to be deployable as a service (HTTP or gRPC endpoint)
2. **Provide connection details** — endpoint URL, authentication method, rate limits
3. **Document the tool schemas** — parameter definitions and response formats (may already exist for Cline)

### Option B: Expose FinOps Data as HTTP API

If the MCP server isn't easily deployable server-side, the FinOps team can expose their data as a standard REST API, and UOP wraps it as an MCP tool:

```python
# UOP wraps the FinOps API as an MCP tool for SmartSDK
def query_cost_data_tool():
    return {
        "name": "query_cost_data",
        "description": "Query cloud spend data from the FinOps platform.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string"},
                "team": {"type": "string"},
                "time_range": {"type": "string", "default": "30d"},
            },
        },
        # Tool executor calls the FinOps HTTP API
    }
```

### Collaboration Items

| Item | Owner | Description |
|------|-------|-------------|
| FinOps MCP/API access | FinOps Team | Provide server-side endpoint for cost data and recommendations |
| Prompt engineering | Joint | Tune AURA's system prompt for cost optimization conversations |
| Recommendation validation | FinOps Team | Verify AURA's FinOps answers match Cline's recommendations |
| Feedback loop | UOP Team | Route thumbs up/down from AURA UI back to FinOps for quality tracking |
| Sourcegraph service account | Joint | Provision server-side Sourcegraph access with appropriate repo permissions |
| Bitbucket service account | Joint | Provision write access for automated PR creation with approval guardrails |

---

## 7. Complementary Positioning: AURA + Cline

AURA does not need to replace Cline — it can complement it by handling the use cases Cline cannot:

| Use Case | Best Fit | Why |
|----------|----------|-----|
| Developer wants in-editor suggestions while coding | **Cline** | IDE integration provides inline context |
| SRE wants to know cost savings across all services | **AURA** | Org-wide queries, rich visualizations |
| Manager wants a cost optimization report for leadership | **AURA** | Tables, charts, metric cards — presentation-ready |
| Automated bulk PR creation for Graviton migration | **AURA** | Bitbucket MCP + Jira MCP for end-to-end automation |
| Developer explores optimization for their specific service | **Either** | Cline for local flow, AURA for richer analysis |
| Tracking which recommendations were acted on | **AURA** | Centralized telemetry and Jira integration |

However, the **high-impact, high-value actions** — org-wide scanning, automated PR creation, leadership reporting, governance — all belong in AURA. Cline's strength is the individual developer's local workflow, but that represents a fraction of the FinOps value chain.

---

## 8. Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| FinOps MCP not server-deployable | Medium | Wrap FinOps data as HTTP API; UOP creates MCP tool adapter (Option B above) |
| Sourcegraph access from server-side | Low | Provision service account; Sourcegraph supports API tokens for server use |
| Bitbucket write access concerns | Medium | AURA guardrails require user confirmation before any write action; PRs still go through normal review process; audit trail for all actions |
| LLM hallucination on cost numbers | Medium | FinOps MCP returns actual data; AURA presents MCP output directly in structured blocks rather than generating numbers |
| SmartSDK not yet in production | Depends on timeline | AURA can demo with mock FinOps data today using existing keyword-matching architecture; SmartSDK integration is incremental |
| FinOps team resistance | Medium | Position as complementary (Section 7), not replacement; AURA extends their reach beyond VS Code users |

---

## 9. Implementation Timeline

| Phase | Description | Effort |
|-------|-------------|--------|
| **Phase 1: Mock Demo** | Add FinOps keyword handlers to existing AURA mock data — demonstrates the UX with hardcoded responses | Days |
| **Phase 2: FinOps MCP Integration** | Connect AURA to FinOps MCP/API for real cost data and recommendations | Weeks (depends on FinOps team readiness) |
| **Phase 3: Sourcegraph Integration** | Add Sourcegraph MCP for code scanning — enables "what code needs to change?" answers | Weeks |
| **Phase 4: Automated Remediation** | Add Bitbucket + Jira MCPs for automated PR creation and ticket tracking | Weeks |
| **Phase 5: Org-Wide Analytics** | Dashboard widgets showing aggregate FinOps recommendations, savings tracked, PR adoption rates | Weeks |

Phase 1 can be delivered immediately as a proof of concept to demonstrate the value to both the FinOps team and leadership.

---

## 10. Summary

| | Cline (Local) | AURA (Centralized) |
|-|---------------|---------------------|
| **Who benefits** | Individual developer in VS Code | Everyone — developers, SREs, managers, leadership |
| **Setup cost** | N developers x (install + configure + maintain) | Zero — it's already in UOP |
| **Governance** | None | Full audit, IAM, guardrails, telemetry |
| **Output** | Text in terminal | Rich blocks: charts, tables, metrics, recommendations |
| **Code changes** | Manual push by developer | Automated PRs via Bitbucket MCP |
| **Tracking** | None | Jira tickets, telemetry, aggregate analytics |
| **Scalability** | Linear with developer count | One config serves the entire org |

AURA is not just a better distribution channel for FinOps recommendations — it's a force multiplier that turns individual developer suggestions into org-wide automated cost optimization with full governance and accountability.
