# Fusion SmartSDK Integration Guide

How to replace UOP's mock AURA chat with real AI agents powered by Fusion SmartSDK (`cdaosmart-sdk`).

---

## 1. Overview

AURA currently uses **keyword matching** against hardcoded scenarios (`app/mock_data/aura_data.py`). Fusion SmartSDK replaces this with real LLM-powered agents that can reason, call tools (MCP), and stream responses — all through JPMC's Gen AI Gateway with built-in IAM, guardrails, and telemetry.

**What changes:** The FastAPI backend (`app/routers/aura.py`).
**What stays the same:** The entire React frontend. The SSE streaming protocol and block format are already compatible.

---

## 2. Current Architecture

```
React UI (AuraChatContext.jsx)
  │  POST /api/aura/chat
  ▼
FastAPI (aura.py)
  │  keyword match on message
  ▼
Mock Data (aura_data.py)          ◄── 11 hardcoded scenario handlers
  │  returns { message_id, content: [blocks], suggested_followups }
  ▼
SSE Stream
  │  event: meta   → { message_id, timestamp }
  │  event: block  → { type, data }  (text | metric_cards | table | bar_chart | ...)
  │  event: followups → [string, ...]
  │  event: done   → {}
  ▼
React renders blocks via ChatBlockRenderer.jsx
```

### Supported Block Types

| Type | Renderer | Description |
|------|----------|-------------|
| `text` | ChatBlockText | Markdown text |
| `metric_cards` | ChatBlockMetrics | KPI cards with sparklines |
| `table` | ChatBlockTable | Data tables |
| `bar_chart` | ChatBlockBarChart | Bar charts |
| `line_chart` | ChatBlockLineChart | Line/trend charts |
| `pie_chart` | ChatBlockPieChart | Pie/donut charts |
| `status_list` | ChatBlockStatusList | Status indicators |
| `recommendations` | ChatBlockRecommendations | Prioritized action items |

---

## 3. Target Architecture

```
React UI (AuraChatContext.jsx)        ◄── NO CHANGES
  │  POST /api/aura/chat
  ▼
FastAPI (aura.py)                     ◄── MODIFIED
  │  create SmartSDK agent + run_stream()
  ▼
┌─────────────────────────────────────────┐
│  Fusion SmartSDK Agent                  │
│  ├── LLM via Gen AI Gateway             │
│  ├── MCP Tools:                         │
│  │   ├── query_incidents (ServiceNow)   │
│  │   ├── get_metrics (Dynatrace)        │
│  │   ├── check_slos (SLO store)         │
│  │   ├── search_graph (ERMA/V12)        │
│  │   ├── get_app_metadata (PATOOLS)     │
│  │   └── lookup_contacts (Corp Dir)     │
│  ├── IAM (JPMC auth)                    │
│  ├── Guardrails                         │
│  └── Telemetry / Tracing                │
└─────────────────────────────────────────┘
  │  SmartSDK event stream
  ▼
Event → SSE Block converter            ◄── NEW (in aura.py)
  │  maps agent output to block format
  ▼
SSE Stream (same format as today)
  ▼
React renders blocks                   ◄── NO CHANGES
```

---

## 4. Prerequisites

1. **Python 3.10–3.13** (already satisfied — project uses FastAPI/Python)
2. **Install SmartSDK:**
   ```bash
   uv pip install cdaosmart-sdk
   ```
3. **Install gRPC server** (required for SmartSDK agent communication):
   ```bash
   uv pip install cdaosmart-grpc
   ```
4. **Start the gRPC server** before running the API:
   ```bash
   smart-grpc-server
   ```
5. **Gen AI Gateway access** — obtain endpoint URL and credentials from your CDAO team
6. **IAM credentials** — JPMC IAM service account or user token for API authentication

---

## 5. Step-by-Step Integration

### Step 1: Update Dependencies

Add to `requirements.txt`:

```
cdaosmart-sdk
cdaosmart-grpc
```

### Step 2: Add Configuration

Add to `app/config.py`:

```python
# ── SmartSDK / AURA AI ──────────────────────────────────────────────────────
GENAI_GATEWAY_URL = os.environ.get("GENAI_GATEWAY_URL", "")
GENAI_API_KEY = os.environ.get("GENAI_API_KEY", "")
SMARTSDK_MODEL = os.environ.get("SMARTSDK_MODEL", "gpt-4")  # or your approved model
AURA_TOOLS_ENABLED = os.environ.get("AURA_TOOLS_ENABLED", "true").lower() == "true"
```

### Step 3: Define MCP Tools

Create `app/services/aura_tools.py` — one tool per external system:

```python
"""MCP tool definitions for AURA SmartSDK agent."""

# Each tool wraps an external API call that the agent can invoke autonomously.
# SmartSDK handles tool-call routing, retries, and response parsing.

def query_incidents_tool():
    """ServiceNow — active incidents, P1/P2 status, timeline."""
    return {
        "name": "query_incidents",
        "description": "Query active incidents from ServiceNow. Returns incident list with priority, status, affected apps, and timeline.",
        "parameters": {
            "type": "object",
            "properties": {
                "priority": {"type": "string", "enum": ["P1", "P2", "P3", "all"]},
                "status": {"type": "string", "enum": ["active", "resolved", "all"]},
                "app_name": {"type": "string", "description": "Filter by application name"},
                "limit": {"type": "integer", "default": 20},
            },
        },
    }

def get_metrics_tool():
    """Dynatrace — real-time performance metrics, error rates, response times."""
    return {
        "name": "get_metrics",
        "description": "Fetch real-time performance metrics from Dynatrace for a given application or service.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string"},
                "metric_type": {"type": "string", "enum": ["error_rate", "response_time", "throughput", "availability"]},
                "time_range": {"type": "string", "default": "24h"},
            },
            "required": ["app_name"],
        },
    }

def check_slos_tool():
    """SLO store — compliance, error budgets, burn rates."""
    return {
        "name": "check_slos",
        "description": "Check SLO compliance, error budget remaining, and burn rate for services.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {"type": "string", "description": "Specific service or 'all'"},
                "include_history": {"type": "boolean", "default": False},
            },
        },
    }

def search_graph_tool():
    """ERMA/V12 — knowledge graph for dependency mapping and blast radius."""
    return {
        "name": "search_graph",
        "description": "Search the application dependency graph (ERMA/V12) to find upstream/downstream dependencies, blast radius, and topology.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string"},
                "query_type": {"type": "string", "enum": ["dependencies", "blast_radius", "topology"]},
                "depth": {"type": "integer", "default": 2},
            },
            "required": ["app_name"],
        },
    }

def get_app_metadata_tool():
    """PATOOLS — application catalog, ownership, SRE contacts."""
    return {
        "name": "get_app_metadata",
        "description": "Look up application metadata from the product catalog (PATOOLS): owner, team, SRE contacts, tier, region.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string"},
                "seal_id": {"type": "string"},
            },
        },
    }

def lookup_contacts_tool():
    """Corporate Directory — people search, team membership."""
    return {
        "name": "lookup_contacts",
        "description": "Look up people in the corporate directory by name, SID, or role.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "search_by": {"type": "string", "enum": ["name", "sid", "role"]},
            },
            "required": ["query"],
        },
    }

ALL_TOOLS = [
    query_incidents_tool(),
    get_metrics_tool(),
    check_slos_tool(),
    search_graph_tool(),
    get_app_metadata_tool(),
    lookup_contacts_tool(),
]
```

### Step 4: Create the Agent Configuration

Create `app/services/aura_agent.py`:

```python
"""SmartSDK agent setup for AURA."""

from cdaosmart_sdk import Agent, Runner
from app.config import GENAI_GATEWAY_URL, GENAI_API_KEY, SMARTSDK_MODEL
from app.services.aura_tools import ALL_TOOLS

AURA_SYSTEM_PROMPT = """You are AURA, an AI-powered SRE assistant for the Unified Operations Platform (UOP).

You help operations teams by:
- Analyzing active incidents and their blast radius
- Reporting on SLO compliance and error budget burn rates
- Providing performance metrics and trend analysis
- Recommending remediation actions with priority and expected impact
- Looking up application ownership and escalation contacts

When responding, structure your output as a sequence of typed blocks:
- Use "text" blocks for narrative explanation
- Use "metric_cards" blocks for KPI summaries (include sparkline arrays for trends)
- Use "table" blocks for tabular comparisons
- Use "status_list" blocks for application health indicators
- Use "recommendations" blocks for prioritized action items
- Use "bar_chart", "line_chart", or "pie_chart" blocks for visualizations

Always provide 2-3 suggested follow-up questions at the end.

Each block must follow this JSON schema:
  { "type": "<block_type>", "data": <block_data>, "title": "<optional title>" }
"""

def create_aura_agent():
    """Create and return a configured SmartSDK agent."""
    agent = Agent(
        name="aura",
        model=SMARTSDK_MODEL,
        instructions=AURA_SYSTEM_PROMPT,
        tools=ALL_TOOLS,
    )
    return agent

def create_runner():
    """Create a SmartSDK Runner configured for Gen AI Gateway."""
    return Runner(
        gateway_url=GENAI_GATEWAY_URL,
        api_key=GENAI_API_KEY,
    )
```

### Step 5: Replace the AURA Router

Replace the contents of `app/routers/aura.py`:

```python
import json
import asyncio
import uuid
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas import AuraChatRequest
from app.config import USE_MOCK_DATA
from app.mock_data import _AURA_SCENARIOS, _aura_default_response

router = APIRouter()


# ── Mock path (existing behavior) ────────────────────────────────────────────

async def _stream_mock(payload: AuraChatRequest):
    """Original keyword-matching mock — kept for USE_MOCK_DATA=true."""
    import random

    msg_lower = payload.message.lower()
    response = None
    for keywords, handler in _AURA_SCENARIOS:
        if any(kw in msg_lower for kw in keywords):
            response = handler()
            break
    if response is None:
        response = _aura_default_response(payload.message)

    meta = {"message_id": response["message_id"], "timestamp": response["timestamp"]}
    yield f"event: meta\ndata: {json.dumps(meta)}\n\n"
    await asyncio.sleep(random.uniform(0.3, 0.6))

    for block in response["content"]:
        yield f"event: block\ndata: {json.dumps(block)}\n\n"
        await asyncio.sleep(random.uniform(0.4, 0.9))

    if response.get("suggested_followups"):
        yield f"event: followups\ndata: {json.dumps(response['suggested_followups'])}\n\n"

    yield "event: done\ndata: {}\n\n"


# ── SmartSDK path ────────────────────────────────────────────────────────────

async def _stream_smartsdk(payload: AuraChatRequest):
    """Stream real AI responses via Fusion SmartSDK."""
    from app.services.aura_agent import create_aura_agent, create_runner

    agent = create_aura_agent()
    runner = create_runner()

    message_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    # Send meta event
    yield f"event: meta\ndata: {json.dumps({'message_id': message_id, 'timestamp': timestamp})}\n\n"

    # Stream agent response
    event_stream = runner.run_stream(agent, payload.message)
    blocks = []
    followups = []

    async for event in event_stream:
        if event.author == "User":
            continue

        for part in event.content.parts:
            # Text responses → text blocks
            if part.text:
                block = {"type": "text", "data": part.text}
                blocks.append(block)
                yield f"event: block\ndata: {json.dumps(block)}\n\n"

            # If the agent returns structured JSON blocks, pass them through
            if part.function_response:
                response_data = part.function_response.response
                # Tool responses may contain structured blocks the agent generated
                if isinstance(response_data, dict) and "type" in response_data:
                    yield f"event: block\ndata: {json.dumps(response_data)}\n\n"

            # Tool calls can be logged for observability
            if part.function_call:
                pass  # Telemetry handles this via SmartSDK

    # Send followups if the agent included them
    if followups:
        yield f"event: followups\ndata: {json.dumps(followups)}\n\n"

    yield "event: done\ndata: {}\n\n"


# ── Route ────────────────────────────────────────────────────────────────────

@router.post("/api/aura/chat")
async def aura_chat(payload: AuraChatRequest):
    generator = _stream_mock(payload) if USE_MOCK_DATA else _stream_smartsdk(payload)

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
```

### Step 6: Handle Structured Output

The key challenge is getting the LLM to return **typed blocks** (metric_cards, tables, etc.) instead of plain text. Two approaches:

**Approach A: System Prompt Instrumentation (simpler)**

The system prompt in Step 4 instructs the agent to return JSON blocks. Parse the agent's text output for embedded JSON:

```python
import re

def extract_blocks_from_text(text):
    """Extract JSON blocks from agent text output."""
    blocks = []
    # Look for ```json ... ``` fenced blocks
    json_pattern = re.compile(r'```json\s*(\{.*?\})\s*```', re.DOTALL)
    matches = json_pattern.findall(text)
    for match in matches:
        try:
            block = json.loads(match)
            if "type" in block and "data" in block:
                blocks.append(block)
        except json.JSONDecodeError:
            continue
    # Remaining text (outside JSON blocks) becomes a text block
    remaining = json_pattern.sub('', text).strip()
    if remaining:
        blocks.insert(0, {"type": "text", "data": remaining})
    return blocks
```

**Approach B: Dedicated Formatting Tool (more reliable)**

Give the agent a `format_response` MCP tool that accepts typed blocks:

```python
def format_response_tool():
    return {
        "name": "format_response",
        "description": "Format a response block for the user. Use this to return structured data like tables, charts, metrics, and recommendations.",
        "parameters": {
            "type": "object",
            "properties": {
                "block_type": {
                    "type": "string",
                    "enum": ["text", "metric_cards", "table", "bar_chart", "line_chart", "pie_chart", "status_list", "recommendations"],
                },
                "title": {"type": "string"},
                "data": {"description": "Block data matching the block_type schema"},
            },
            "required": ["block_type", "data"],
        },
    }
```

When the agent calls this tool, intercept it in the stream and emit it as an SSE block directly.

### Step 7: Configure IAM

SmartSDK supports JPMC IAM natively. Pass user context from the frontend:

```python
# In aura.py — extract user identity from request headers
@router.post("/api/aura/chat")
async def aura_chat(payload: AuraChatRequest, request: Request):
    user_token = request.headers.get("Authorization", "")
    # Pass to SmartSDK runner for IAM validation
    runner = create_runner(user_token=user_token)
    ...
```

### Step 8: Enable Telemetry

SmartSDK provides telemetry out of the box. Configure in your agent setup:

```python
agent = Agent(
    name="aura",
    model=SMARTSDK_MODEL,
    instructions=AURA_SYSTEM_PROMPT,
    tools=ALL_TOOLS,
    # SmartSDK telemetry config
    telemetry={
        "enabled": True,
        "log_tool_calls": True,
        "log_llm_requests": True,
        "trace_id_header": "X-Trace-Id",
    },
)
```

### Step 9: Add Guardrails

SmartSDK guardrails prevent the agent from returning sensitive data or taking dangerous actions:

```python
agent = Agent(
    name="aura",
    ...
    guardrails={
        "block_pii": True,
        "max_tool_calls": 10,        # Prevent runaway tool loops
        "allowed_tools": [t["name"] for t in ALL_TOOLS],
        "content_filters": ["financial_data", "customer_pii"],
    },
)
```

---

## 6. Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `USE_MOCK_DATA` | No | `true` (default) uses mock data, `false` uses SmartSDK |
| `GENAI_GATEWAY_URL` | Yes* | Gen AI Gateway endpoint URL |
| `GENAI_API_KEY` | Yes* | API key for Gen AI Gateway |
| `SMARTSDK_MODEL` | No | Model to use (default: `gpt-4`) |
| `AURA_TOOLS_ENABLED` | No | Enable MCP tools (default: `true`) |

*Required when `USE_MOCK_DATA=false`

---

## 7. Frontend Impact

**No frontend changes required.**

The React UI (`src/aura/AuraChatContext.jsx`) already:
- Sends `POST /api/aura/chat` with `{ message, attachments }`
- Parses SSE events: `meta`, `block`, `followups`, `done`
- Renders blocks via `ChatBlockRenderer.jsx` (8 block types)
- Supports abort/cancel, session history, feedback

As long as the backend emits the same SSE event format, the UI works identically whether the source is mock data or a SmartSDK agent.

---

## 8. Optional: SLO Agent (Multi-Agent)

The static SLO Agent page (`src/pages/SloCorrector.jsx`) can be upgraded to a real multi-agent workflow:

```python
from cdaosmart_sdk import Agent, Runner

slo_monitor = Agent(
    name="slo_monitor",
    instructions="Monitor SLO compliance. Alert when error budget < 20%.",
    tools=[check_slos_tool(), get_metrics_tool()],
)

slo_corrector = Agent(
    name="slo_corrector",
    instructions="When SLOs are at risk, recommend and execute corrective actions.",
    tools=[scale_service_tool(), enable_failover_tool(), rollback_canary_tool()],
)

# SmartSDK orchestrates the agents as a team
team_runner = Runner(agents=[slo_monitor, slo_corrector])
```

---

## 9. Rollout Strategy

1. **Phase 1 — Mock (current):** `USE_MOCK_DATA=true`. No SmartSDK dependency.
2. **Phase 2 — Shadow mode:** Run SmartSDK alongside mock. Log SmartSDK responses but return mock to the user. Compare quality.
3. **Phase 3 — Live with fallback:** `USE_MOCK_DATA=false`. If SmartSDK errors, fall back to mock.
4. **Phase 4 — Full production:** Remove mock fallback. SmartSDK is the sole provider.

Fallback pattern for Phase 3:

```python
async def _stream_with_fallback(payload):
    try:
        async for event in _stream_smartsdk(payload):
            yield event
    except Exception:
        async for event in _stream_mock(payload):
            yield event
```

---

## 10. Testing

### Local Development
```bash
# Terminal 1: Start gRPC server
smart-grpc-server

# Terminal 2: Start API with SmartSDK
USE_MOCK_DATA=false \
GENAI_GATEWAY_URL=https://your-gateway.jpmc.com \
GENAI_API_KEY=your-key \
uvicorn app.main:app --reload
```

### Verify SSE Format
```bash
curl -X POST http://localhost:8000/api/aura/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "show me active incidents"}' \
  --no-buffer
```

Expected output should contain:
```
event: meta
data: {"message_id": "...", "timestamp": "..."}

event: block
data: {"type": "text", "data": "Here are the current active incidents..."}

event: block
data: {"type": "status_list", "title": "Active Incidents", "data": [...]}

event: done
data: {}
```

### Checklist
- [ ] `smart-grpc-server` starts without errors
- [ ] Agent responds to natural language queries
- [ ] MCP tools are invoked when relevant (check telemetry logs)
- [ ] SSE blocks render correctly in the React UI
- [ ] Streaming works (blocks appear incrementally, not all at once)
- [ ] Abort/cancel works (user can stop a streaming response)
- [ ] Fallback to mock works when SmartSDK errors
- [ ] IAM rejects unauthorized requests
- [ ] Guardrails block PII in responses

---

## Files Reference

| File | Action | Purpose |
|------|--------|---------|
| `app/config.py` | Edit | Add SmartSDK env vars |
| `app/routers/aura.py` | Edit | Add SmartSDK streaming path |
| `app/services/aura_tools.py` | Create | MCP tool definitions |
| `app/services/aura_agent.py` | Create | Agent + Runner setup |
| `requirements.txt` | Edit | Add cdaosmart-sdk, cdaosmart-grpc |
| `src/aura/*` (UI) | No change | Already compatible |
