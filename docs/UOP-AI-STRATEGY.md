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
| **DevGPT Cline Team** | MCP management, DevGPT Cline modes (FinOps, Resiliency, Cost-Optimization, etc.) | VS Code Cline extension with Sourcegraph MCP — requires per-developer local setup |
| **AURA Team** | Agentic AI workflow, SmartSDK agents, MCP orchestration | Centralized AI backend with tool calling, IAM, guardrails |
| **UOP Team** | Unified Operations Platform, chat UI, dashboards, View Central | Platform where all users already are — needs AI integration |
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
| **FinOps** | query_cost_data, get_finops_recommendations, check_graviton_eligibility, get_spot_candidates, check_lightswitch_status | DevGPT Cline Team | Available in Cline; needs server-side deployment |
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

The DevGPT Cline team's FinOps mode illustrates why UOP is the better distribution channel for any AI capability.

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

### What the DevGPT Cline Team Needs to Do

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
| **Owner** | AURA team | UOP team |
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
    timedOut = false
    timeout = setTimeout(() => { timedOut = true; abort() }, 30000)

    try:
      res = POST ${url}/api/aura/chat
      clearTimeout(timeout)
      if !res.ok: throw Error
      consecutiveErrors = 0       // reset on success
      stream response...

    catch(err):
      if err is AbortError and !timedOut:
        // user cancelled — ignore
      else:
        consecutiveErrors++
        if consecutiveErrors >= 3 and backend === 'aura':
          backend = 'smartsdk'    // silent switch

    finally:
      clearTimeout(timeout)
```

**Triggers failover on:** HTTP errors (4xx/5xx), network unreachable, DNS failure, connection refused, and 30-second timeout (hanging backend). Does NOT count user-initiated cancels as errors.

### UI Changes Required

| File | Change |
|------|--------|
| `public/env-config.js` | Add `AURA_BACKEND`, `AURA_API_URL`, `SMARTSDK_API_URL` |
| `src/config.js` | Export new env vars with fallback defaults |
| `src/aura/AuraChatContext.jsx` | Backend routing, error counter, auto-fallback, expose `backend` on context |
| `src/aura/AuraChatHeader.jsx` | 5-click hidden toggle on title, dark icon + "(Direct)" subtitle on SmartSDK |
| `src/aura/AuraChatMenu.jsx` | Hidden Advanced section with backend toggle |

### Complete File Changes

Below are the full updated files. These can be applied manually or by another agent in any UOP-UI environment.

#### `public/env-config.js`

```javascript
// Runtime environment configuration
// In dev: API_URL is empty (Vite proxy handles /api)
// In CF: Set API_URL to your deployed uop-api URL (e.g. "https://uop-api.apps.cf.example.com")
window.__ENV__ = {
  API_URL: "",
  AURA_BACKEND: "aura",       // "aura" | "smartsdk"
  AURA_API_URL: "",            // AURA team's endpoint (empty = same as API_URL)
  SMARTSDK_API_URL: "",        // UOP's own SmartSDK endpoint (empty = same as API_URL)
};
```

#### `src/config.js`

```javascript
// API base URL — reads from runtime env-config.js injected in index.html
// Empty string in dev (Vite proxy forwards /api to the backend)
// Set window.__ENV__.API_URL in CF to point at the deployed uop-api
export const API_URL = window.__ENV__?.API_URL || '';

// AI backend configuration
export const AURA_BACKEND = window.__ENV__?.AURA_BACKEND || 'aura';
export const AURA_API_URL = window.__ENV__?.AURA_API_URL || API_URL;
export const SMARTSDK_API_URL = window.__ENV__?.SMARTSDK_API_URL || API_URL;
```

#### `src/aura/AuraChatContext.jsx`

Key changes from the original:
- Import `AURA_BACKEND`, `AURA_API_URL`, `SMARTSDK_API_URL` from config
- Add `getInitialBackend()` — reads URL param `?aura_backend=`, then localStorage, then config default
- Add `getBackendUrl()` — resolves backend name to URL
- Add `backend`, `showAdvanced` state and `setBackend`, `clearBackendOverride` callbacks
- Replace hardcoded `${API_URL}/api/aura/chat` with `${getBackendUrl(backend)}/api/aura/chat`
- Add `consecutiveErrorsRef` — after 3 failures on AURA, auto-switch to SmartSDK
- Expose `backend`, `showAdvanced`, `setBackend`, `setShowAdvanced`, `clearBackendOverride` on context

```jsx
import { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react'
import { API_URL, AURA_BACKEND, AURA_API_URL, SMARTSDK_API_URL } from '../config'

const AuraChatContext = createContext()
export const useAuraChat = () => useContext(AuraChatContext)

const STORAGE_KEY = 'aura-chat-history'
const SESSIONS_KEY = 'aura-chat-sessions'
const BACKEND_KEY = 'aura-backend-override'
const MAX_MESSAGES = 50
const MAX_CONSECUTIVE_ERRORS = 3

function getInitialBackend() {
  // URL param takes priority (e.g. ?aura_backend=smartsdk)
  const params = new URLSearchParams(window.location.search)
  const paramBackend = params.get('aura_backend')
  if (paramBackend === 'aura' || paramBackend === 'smartsdk') return paramBackend
  // localStorage override from hidden toggle
  const stored = localStorage.getItem(BACKEND_KEY)
  if (stored === 'aura' || stored === 'smartsdk') return stored
  // Default from config
  return AURA_BACKEND
}

function getBackendUrl(backend) {
  return backend === 'smartsdk' ? (SMARTSDK_API_URL || API_URL) : (AURA_API_URL || API_URL)
}

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch { return [] }
}

function loadSessions() {
  try {
    const raw = localStorage.getItem(SESSIONS_KEY)
    return raw ? JSON.parse(raw) : []
  } catch { return [] }
}

function saveSessions(sessions) {
  try { localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions.slice(-20))) }
  catch { /* ignore */ }
}

function deriveTitle(messages) {
  const firstUser = messages.find(m => m.role === 'user')
  if (!firstUser) return 'New Chat'
  const text = typeof firstUser.content === 'string' ? firstUser.content : 'Chat'
  return text.length > 50 ? text.slice(0, 47) + '...' : text
}

/* Parse SSE text buffer into individual events */
function parseSSEEvents(text) {
  const events = []
  const blocks = text.split('\n\n')
  for (const block of blocks) {
    if (!block.trim()) continue
    let eventType = 'message'
    let data = ''
    for (const line of block.split('\n')) {
      if (line.startsWith('event: ')) eventType = line.slice(7).trim()
      else if (line.startsWith('data: ')) data = line.slice(6)
    }
    if (data) {
      try { events.push({ type: eventType, data: JSON.parse(data) }) }
      catch { /* skip malformed */ }
    }
  }
  return events
}

export function AuraChatProvider({ children }) {
  const [isOpen, setIsOpen] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [messages, setMessages] = useState(loadFromStorage)
  const [isLoading, setIsLoading] = useState(false)
  const [attachments, setAttachments] = useState([])
  const [activeSessionId, setActiveSessionId] = useState(() => crypto.randomUUID())
  const [chatSessions, setChatSessions] = useState(loadSessions)
  const [backend, setBackendState] = useState(getInitialBackend)
  const [showAdvanced, setShowAdvanced] = useState(() => localStorage.getItem(BACKEND_KEY) !== null)
  const abortRef = useRef(null)
  const consecutiveErrorsRef = useRef(0)

  const setBackend = useCallback((value) => {
    setBackendState(value)
    localStorage.setItem(BACKEND_KEY, value)
  }, [])

  const clearBackendOverride = useCallback(() => {
    setBackendState(AURA_BACKEND)
    localStorage.removeItem(BACKEND_KEY)
    setShowAdvanced(false)
  }, [])

  const sendMessage = useCallback(async (text) => {
    const currentAttachments = [...attachments]
    const userMsg = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString(),
      attachments: currentAttachments.length > 0
        ? currentAttachments.map(f => ({ name: f.name, size: f.size, type: f.type }))
        : null,
    }
    setMessages(prev => [...prev, userMsg])
    setAttachments([])
    setIsLoading(true)

    const assistantId = crypto.randomUUID()
    const assistantMsg = {
      id: assistantId,
      role: 'assistant',
      content: [],
      timestamp: new Date().toISOString(),
      suggestedFollowups: null,
      _streaming: true,
    }
    setMessages(prev => [...prev, assistantMsg])

    try {
      const controller = new AbortController()
      abortRef.current = controller

      // 30s connection timeout — triggers failover if backend is unreachable/hanging
      let timedOut = false
      const timeoutId = setTimeout(() => { timedOut = true; controller.abort() }, 30000)

      const backendUrl = getBackendUrl(backend)
      const res = await fetch(`${backendUrl}/api/aura/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          attachments: currentAttachments.map(f => f.name),
        }),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)

      consecutiveErrorsRef.current = 0
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })

        const lastDoubleNewline = buffer.lastIndexOf('\n\n')
        if (lastDoubleNewline === -1) continue

        const complete = buffer.slice(0, lastDoubleNewline + 2)
        buffer = buffer.slice(lastDoubleNewline + 2)

        const events = parseSSEEvents(complete)
        for (const evt of events) {
          if (evt.type === 'meta') {
            setMessages(prev => prev.map(m =>
              m.id === assistantId
                ? { ...m, id: evt.data.message_id || m.id, timestamp: evt.data.timestamp || m.timestamp }
                : m
            ))
          } else if (evt.type === 'block') {
            setMessages(prev => prev.map(m =>
              m.id === assistantId || m.id === evt.data?.message_id || (m._streaming && m.role === 'assistant')
                ? { ...m, content: [...m.content, evt.data] }
                : m
            ))
          } else if (evt.type === 'followups') {
            setMessages(prev => prev.map(m =>
              m._streaming && m.role === 'assistant'
                ? { ...m, suggestedFollowups: evt.data }
                : m
            ))
          } else if (evt.type === 'done') {
            setMessages(prev => prev.map(m =>
              m._streaming && m.role === 'assistant'
                ? { ...m, _streaming: false }
                : m
            ))
          }
        }
      }
    } catch (err) {
      if (err.name === 'AbortError' && !timedOut) {
        // User-initiated cancel — don't count as error
      } else {
        consecutiveErrorsRef.current++
        // Auto-failover: switch to SmartSDK after 3 consecutive failures on AURA
        if (consecutiveErrorsRef.current >= MAX_CONSECUTIVE_ERRORS && backend === 'aura' && SMARTSDK_API_URL) {
          setBackendState('smartsdk')
        }
        setMessages(prev => {
          const last = prev[prev.length - 1]
          if (last?._streaming && last.content.length === 0) {
            return [...prev.slice(0, -1), {
              id: crypto.randomUUID(),
              role: 'assistant',
              content: [{ type: 'text', data: 'I encountered an error processing your request. Please try again.' }],
              timestamp: new Date().toISOString(),
            }]
          }
          return prev.map(m => m._streaming ? { ...m, _streaming: false } : m)
        })
      }
    } finally {
      clearTimeout(timeoutId)
      setIsLoading(false)
      abortRef.current = null
    }
  }, [attachments, backend])

  const saveCurrentSession = useCallback(() => {
    if (messages.length === 0) return
    setChatSessions(prev => {
      const filtered = prev.filter(s => s.id !== activeSessionId)
      const session = {
        id: activeSessionId,
        title: deriveTitle(messages),
        timestamp: messages[0]?.timestamp || new Date().toISOString(),
        messageCount: messages.length,
        messages: messages.filter(m => !m._streaming).slice(-MAX_MESSAGES),
        active: true,
      }
      const updated = [...filtered, session].slice(-20)
      saveSessions(updated)
      return updated
    })
  }, [messages, activeSessionId])

  const newChat = useCallback(() => {
    if (abortRef.current) abortRef.current.abort()
    saveCurrentSession()
    const newId = crypto.randomUUID()
    setActiveSessionId(newId)
    setMessages([])
    setIsLoading(false)
    setAttachments([])
    localStorage.removeItem(STORAGE_KEY)
  }, [saveCurrentSession])

  const clearChat = useCallback(() => {
    if (abortRef.current) abortRef.current.abort()
    setMessages([])
    setIsLoading(false)
    localStorage.removeItem(STORAGE_KEY)
    setChatSessions(prev => {
      const updated = prev.filter(s => s.id !== activeSessionId)
      saveSessions(updated)
      return updated
    })
  }, [activeSessionId])

  const activateSession = useCallback((sessionId) => {
    saveCurrentSession()
    setChatSessions(prev => {
      const session = prev.find(s => s.id === sessionId)
      if (!session) return prev
      setActiveSessionId(sessionId)
      setMessages(session.messages || [])
      setIsLoading(false)
      setAttachments([])
      localStorage.setItem(STORAGE_KEY, JSON.stringify(session.messages || []))
      return prev.map(s => ({ ...s, active: s.id === sessionId }))
    })
  }, [saveCurrentSession])

  const setMessageFeedback = useCallback((messageId, feedback) => {
    setMessages(prev => prev.map(m =>
      m.id === messageId ? { ...m, feedback: m.feedback === feedback ? null : feedback } : m
    ))
  }, [])

  const toggleOpen = useCallback(() => setIsOpen(p => !p), [])
  const toggleExpand = useCallback(() => setIsExpanded(p => !p), [])
  const toggleMenu = useCallback(() => setMenuOpen(p => !p), [])
  const addAttachment = useCallback((file) => setAttachments(p => [...p, file]), [])
  const removeAttachment = useCallback((idx) => setAttachments(p => p.filter((_, i) => i !== idx)), [])

  useEffect(() => {
    if (messages.length > 0) {
      const toSave = messages.filter(m => !m._streaming).slice(-MAX_MESSAGES)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(toSave))
    }
  }, [messages])

  useEffect(() => {
    if (messages.length > 0) {
      setChatSessions(prev => {
        const updated = prev.map(s =>
          s.id === activeSessionId
            ? { ...s, title: deriveTitle(messages), messageCount: messages.length, active: true }
            : { ...s, active: false }
        )
        if (!updated.find(s => s.id === activeSessionId)) {
          updated.push({
            id: activeSessionId,
            title: deriveTitle(messages),
            timestamp: messages[0]?.timestamp || new Date().toISOString(),
            messageCount: messages.length,
            messages: [],
            active: true,
          })
        }
        return updated.slice(-20)
      })
    }
  }, [messages, activeSessionId])

  return (
    <AuraChatContext.Provider value={{
      isOpen, isExpanded, menuOpen, messages, isLoading, attachments,
      chatSessions, activeSessionId,
      backend, showAdvanced,
      sendMessage, clearChat, newChat, toggleOpen, toggleExpand, toggleMenu,
      addAttachment, removeAttachment, activateSession, setMessageFeedback,
      setBackend, setShowAdvanced, clearBackendOverride,
    }}>
      {children}
    </AuraChatContext.Provider>
  )
}
```

#### `src/aura/AuraChatHeader.jsx`

Key changes from the original:
- Add 5-click counter on the "AURA AI Assistant" title text (2-second timeout window)
- 5 clicks toggles `showAdvanced` state (reveals Advanced section in menu)
- Icon gradient changes to dark/black (`#1a1a1a → #404040`) when on SmartSDK
- Subtitle appends "(Direct)" when on SmartSDK

```jsx
import { useRef, useCallback } from 'react'
import { Box, Typography, IconButton, Tooltip } from '@mui/material'
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome'
import CloseIcon from '@mui/icons-material/Close'
import OpenInFullIcon from '@mui/icons-material/OpenInFull'
import CloseFullscreenIcon from '@mui/icons-material/CloseFullscreen'
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline'
import MenuIcon from '@mui/icons-material/Menu'
import AddIcon from '@mui/icons-material/Add'
import { useAuraChat } from './AuraChatContext'

const fBody = { fontSize: 'clamp(0.85rem, 1.1vw, 0.95rem)' }
const fSmall = { fontSize: 'clamp(0.72rem, 0.9vw, 0.82rem)' }

export default function AuraChatHeader() {
  const { toggleOpen, toggleExpand, isExpanded, clearChat, newChat, messages, toggleMenu, backend, showAdvanced, setShowAdvanced } = useAuraChat()

  // 5-click hidden toggle to reveal advanced backend settings
  const clickCountRef = useRef(0)
  const clickTimerRef = useRef(null)

  const handleTitleClick = useCallback(() => {
    clickCountRef.current++
    if (clickTimerRef.current) clearTimeout(clickTimerRef.current)
    if (clickCountRef.current >= 5) {
      clickCountRef.current = 0
      setShowAdvanced(prev => !prev)
    } else {
      clickTimerRef.current = setTimeout(() => { clickCountRef.current = 0 }, 2000)
    }
  }, [setShowAdvanced])

  const subtitle = backend === 'smartsdk'
    ? 'AI-Powered Observability Insights (Direct)'
    : 'AI-Powered Observability Insights'

  return (
    <Box sx={{
      px: 2, py: 1.5,
      borderBottom: '1px solid',
      borderColor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.12)' : 'divider',
      background: t => t.palette.mode === 'dark'
        ? 'linear-gradient(135deg, rgba(21,101,192,0.22), rgba(14,165,233,0.14))'
        : 'linear-gradient(135deg, rgba(21,101,192,0.12), rgba(14,165,233,0.08))',
      display: 'flex', alignItems: 'center', gap: 1,
      flexShrink: 0,
    }}>
      <Tooltip title="Chat Menu">
        <IconButton size="small" onClick={toggleMenu} sx={{ color: 'text.secondary', '&:hover': { color: 'text.primary' } }}>
          <MenuIcon sx={{ fontSize: 18 }} />
        </IconButton>
      </Tooltip>

      <Box sx={{
        width: 28, height: 28, borderRadius: '50%',
        background: backend === 'smartsdk'
          ? 'linear-gradient(135deg, #1a1a1a, #404040)'
          : 'linear-gradient(135deg, #1565C0, #0ea5e9)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }}>
        <AutoAwesomeIcon sx={{ fontSize: 15, color: '#fff' }} />
      </Box>

      <Box sx={{ flex: 1, cursor: 'default', userSelect: 'none' }} onClick={handleTitleClick}>
        <Typography fontWeight={700} sx={{ ...fBody, color: 'text.primary', lineHeight: 1.3 }}>
          AURA AI Assistant
        </Typography>
        <Typography sx={{ ...fSmall, color: 'text.secondary', lineHeight: 1.2 }}>
          {subtitle}
        </Typography>
      </Box>

      <Tooltip title="New Chat">
        <IconButton size="small" onClick={newChat} sx={{ color: 'text.secondary', '&:hover': { color: 'text.primary' } }}>
          <AddIcon sx={{ fontSize: 18 }} />
        </IconButton>
      </Tooltip>

      {messages.length > 0 && (
        <Tooltip title="Clear chat">
          <IconButton size="small" onClick={clearChat} sx={{ color: 'text.secondary', '&:hover': { color: 'text.primary' } }}>
            <DeleteOutlineIcon sx={{ fontSize: 18 }} />
          </IconButton>
        </Tooltip>
      )}
      <Tooltip title={isExpanded ? 'Collapse' : 'Expand'}>
        <IconButton size="small" onClick={toggleExpand} sx={{ color: 'text.secondary', '&:hover': { color: 'text.primary' } }}>
          {isExpanded
            ? <CloseFullscreenIcon sx={{ fontSize: 18 }} />
            : <OpenInFullIcon sx={{ fontSize: 18 }} />}
        </IconButton>
      </Tooltip>
      <Tooltip title="Close">
        <IconButton size="small" onClick={toggleOpen} sx={{ color: 'text.secondary', '&:hover': { color: 'text.primary' } }}>
          <CloseIcon sx={{ fontSize: 18 }} />
        </IconButton>
      </Tooltip>
    </Box>
  )
}
```

#### `src/aura/AuraChatMenu.jsx`

Key changes from the original:
- Add `SettingsIcon` import
- Destructure `backend`, `showAdvanced`, `setBackend`, `clearBackendOverride` from context
- Add `advancedOpen` state
- Add "Advanced" section (only renders when `showAdvanced` is true) with AURA/SmartSDK radio toggle and "Reset & hide advanced" option

The full file is shown below. Only the additions after the Customizations `</Collapse>` are new — everything above it is unchanged from the original.

```jsx
import { Box, Typography, IconButton, Collapse, Tooltip, Divider } from '@mui/material'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import ExpandLessIcon from '@mui/icons-material/ExpandLess'
import ChatBubbleOutlineIcon from '@mui/icons-material/ChatBubbleOutline'
import HistoryIcon from '@mui/icons-material/History'
import TuneIcon from '@mui/icons-material/Tune'
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline'
import ToggleOnIcon from '@mui/icons-material/ToggleOn'
import ToggleOffIcon from '@mui/icons-material/ToggleOff'
import CloseIcon from '@mui/icons-material/Close'
import SettingsIcon from '@mui/icons-material/Settings'
import { useState } from 'react'
import { useAuraChat } from './AuraChatContext'

const fBody = { fontSize: 'clamp(0.82rem, 1.1vw, 0.92rem)' }
const fSmall = { fontSize: 'clamp(0.7rem, 0.9vw, 0.8rem)' }
const fTiny = { fontSize: 'clamp(0.63rem, 0.8vw, 0.72rem)' }

function formatSessionDate(ts) {
  try {
    const d = new Date(ts)
    const now = new Date()
    const diff = now - d
    if (diff < 86400000) return 'Today'
    if (diff < 172800000) return 'Yesterday'
    return d.toLocaleDateString([], { month: 'short', day: 'numeric' })
  } catch { return '' }
}

function SectionHeader({ icon: Icon, title, expanded, onToggle }) {
  return (
    <Box
      onClick={onToggle}
      sx={{
        display: 'flex', alignItems: 'center', gap: 1,
        px: 1.5, py: 1,
        cursor: 'pointer',
        '&:hover': { bgcolor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.02)' },
      }}
    >
      <Icon sx={{ fontSize: 16, color: 'text.secondary' }} />
      <Typography fontWeight={600} sx={{ ...fSmall, color: 'text.primary', flex: 1 }}>
        {title}
      </Typography>
      {expanded ? <ExpandLessIcon sx={{ fontSize: 16, color: 'text.secondary' }} /> : <ExpandMoreIcon sx={{ fontSize: 16, color: 'text.secondary' }} />}
    </Box>
  )
}

const CUSTOMIZATIONS = [
  { key: 'streaming', label: 'Streaming Responses', description: 'Enable real-time streaming of AI responses', defaultOn: true },
  { key: 'charts', label: 'Rich Visualizations', description: 'Show charts and graphs in responses', defaultOn: true },
  { key: 'followups', label: 'Suggested Follow-ups', description: 'Display suggested prompts after responses', defaultOn: true },
  { key: 'timestamps', label: 'Message Timestamps', description: 'Show time on each message', defaultOn: true },
  { key: 'sounds', label: 'Notification Sounds', description: 'Play sounds on new responses', defaultOn: false },
]

export default function AuraChatMenu({ onClose }) {
  const { chatSessions, activateSession, messages, backend, showAdvanced, setBackend, clearBackendOverride } = useAuraChat()
  const [historyOpen, setHistoryOpen] = useState(true)
  const [customOpen, setCustomOpen] = useState(true)
  const [advancedOpen, setAdvancedOpen] = useState(true)
  const [toggles, setToggles] = useState(() =>
    Object.fromEntries(CUSTOMIZATIONS.map(c => [c.key, c.defaultOn]))
  )

  const handleToggle = (key) => {
    setToggles(p => ({ ...p, [key]: !p[key] }))
  }

  const sessions = chatSessions || []

  return (
    <Box sx={{
      width: '100%',
      display: 'flex', flexDirection: 'column',
      flex: 1,
      overflowY: 'auto',
    }}>
      {/* Menu header */}
      <Box sx={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        px: 1.5, py: 1.25,
        borderBottom: '1px solid',
        borderColor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.08)' : 'divider',
      }}>
        <Typography fontWeight={700} sx={{ ...fBody, color: 'text.primary' }}>
          Chat Menu
        </Typography>
        <Tooltip title="Close menu">
          <IconButton size="small" onClick={onClose} sx={{ color: 'text.secondary' }}>
            <CloseIcon sx={{ fontSize: 16 }} />
          </IconButton>
        </Tooltip>
      </Box>

      {/* Chat History */}
      <SectionHeader
        icon={HistoryIcon}
        title="Chat History"
        expanded={historyOpen}
        onToggle={() => setHistoryOpen(p => !p)}
      />
      <Collapse in={historyOpen}>
        <Box sx={{ px: 1, pb: 1 }}>
          {sessions.length === 0 ? (
            <Typography sx={{ ...fTiny, color: 'text.disabled', px: 0.75, py: 0.5 }}>
              No previous chats
            </Typography>
          ) : (
            sessions.map((session) => (
              <Box
                key={session.id}
                onClick={() => activateSession(session.id)}
                sx={{
                  display: 'flex', alignItems: 'center', gap: 0.75,
                  px: 1, py: 0.6,
                  borderRadius: 1,
                  cursor: 'pointer',
                  bgcolor: session.active
                    ? (t => t.palette.mode === 'dark' ? 'rgba(96,165,250,0.12)' : 'rgba(21,101,192,0.08)')
                    : 'transparent',
                  '&:hover': {
                    bgcolor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
                  },
                  mb: 0.25,
                }}
              >
                <ChatBubbleOutlineIcon sx={{ fontSize: 13, color: 'text.secondary', flexShrink: 0 }} />
                <Box sx={{ flex: 1, minWidth: 0 }}>
                  <Typography noWrap fontWeight={session.active ? 600 : 400} sx={{ ...fTiny, color: 'text.primary', lineHeight: 1.3 }}>
                    {session.title}
                  </Typography>
                  <Typography sx={{ ...fTiny, color: 'text.disabled', lineHeight: 1.2 }}>
                    {formatSessionDate(session.timestamp)} · {session.messageCount} msgs
                  </Typography>
                </Box>
              </Box>
            ))
          )}
        </Box>
      </Collapse>

      <Divider sx={{ borderColor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.06)' : 'divider' }} />

      {/* Customizations */}
      <SectionHeader
        icon={TuneIcon}
        title="Customizations"
        expanded={customOpen}
        onToggle={() => setCustomOpen(p => !p)}
      />
      <Collapse in={customOpen}>
        <Box sx={{ px: 1, pb: 1.5 }}>
          {CUSTOMIZATIONS.map((c) => (
            <Box
              key={c.key}
              onClick={() => handleToggle(c.key)}
              sx={{
                display: 'flex', alignItems: 'center', gap: 0.75,
                px: 1, py: 0.5,
                borderRadius: 1,
                cursor: 'pointer',
                '&:hover': {
                  bgcolor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.02)',
                },
                mb: 0.25,
              }}
            >
              {toggles[c.key]
                ? <ToggleOnIcon sx={{ fontSize: 20, color: t => t.palette.mode === 'dark' ? '#60a5fa' : '#1565C0', flexShrink: 0 }} />
                : <ToggleOffIcon sx={{ fontSize: 20, color: 'text.disabled', flexShrink: 0 }} />}
              <Box sx={{ flex: 1, minWidth: 0 }}>
                <Typography fontWeight={500} sx={{ ...fTiny, color: 'text.primary', lineHeight: 1.3 }}>
                  {c.label}
                </Typography>
                <Typography sx={{ ...fTiny, color: 'text.disabled', lineHeight: 1.2, fontSize: 'clamp(0.52rem, 0.65vw, 0.6rem)' }}>
                  {c.description}
                </Typography>
              </Box>
            </Box>
          ))}
        </Box>
      </Collapse>

      {/* Advanced — only visible after 5-click on header title */}
      {showAdvanced && (
        <>
          <Divider sx={{ borderColor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.06)' : 'divider' }} />
          <SectionHeader
            icon={SettingsIcon}
            title="Advanced"
            expanded={advancedOpen}
            onToggle={() => setAdvancedOpen(p => !p)}
          />
          <Collapse in={advancedOpen}>
            <Box sx={{ px: 1, pb: 1.5 }}>
              <Typography sx={{ ...fTiny, color: 'text.disabled', px: 1, pb: 0.5 }}>
                AI Backend
              </Typography>
              {[
                { key: 'aura', label: 'AURA', description: 'Primary — routed through AURA team' },
                { key: 'smartsdk', label: 'Direct SmartSDK', description: 'Fallback — UOP-managed agent' },
              ].map((opt) => (
                <Box
                  key={opt.key}
                  onClick={() => setBackend(opt.key)}
                  sx={{
                    display: 'flex', alignItems: 'center', gap: 0.75,
                    px: 1, py: 0.5,
                    borderRadius: 1,
                    cursor: 'pointer',
                    bgcolor: backend === opt.key
                      ? (t => t.palette.mode === 'dark' ? 'rgba(96,165,250,0.12)' : 'rgba(21,101,192,0.08)')
                      : 'transparent',
                    '&:hover': {
                      bgcolor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
                    },
                    mb: 0.25,
                  }}
                >
                  {backend === opt.key
                    ? <CheckCircleOutlineIcon sx={{ fontSize: 16, color: t => t.palette.mode === 'dark' ? '#60a5fa' : '#1565C0', flexShrink: 0 }} />
                    : <Box sx={{ width: 16, height: 16, flexShrink: 0 }} />}
                  <Box sx={{ flex: 1, minWidth: 0 }}>
                    <Typography fontWeight={backend === opt.key ? 600 : 400} sx={{ ...fTiny, color: 'text.primary', lineHeight: 1.3 }}>
                      {opt.label}
                    </Typography>
                    <Typography sx={{ ...fTiny, color: 'text.disabled', lineHeight: 1.2, fontSize: 'clamp(0.52rem, 0.65vw, 0.6rem)' }}>
                      {opt.description}
                    </Typography>
                  </Box>
                </Box>
              ))}
              <Box
                onClick={clearBackendOverride}
                sx={{
                  display: 'flex', alignItems: 'center', gap: 0.75,
                  px: 1, py: 0.5, mt: 0.5,
                  borderRadius: 1,
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: t => t.palette.mode === 'dark' ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)',
                  },
                }}
              >
                <CloseIcon sx={{ fontSize: 14, color: 'text.disabled', flexShrink: 0 }} />
                <Typography sx={{ ...fTiny, color: 'text.disabled', lineHeight: 1.3 }}>
                  Reset &amp; hide advanced
                </Typography>
              </Box>
            </Box>
          </Collapse>
        </>
      )}
    </Box>
  )
}
```

### Independent MCP Testing

The dual-backend architecture enables UOP to test new MCPs ahead of AURA's registration cycle. UOP's SmartSDK agent can carry a **superset** of tools compared to AURA:

```
AURA Agent tools:          [incidents, metrics, slos, graph, contacts]
UOP SmartSDK Agent tools:  [incidents, metrics, slos, graph, contacts,
                            finops, sourcegraph, bitbucket, jira]  ◄── testing ahead of AURA
```

**Workflow:**
1. A team (e.g., FinOps) gives UOP access to their MCP
2. UOP registers the MCP on its own SmartSDK agent
3. UOP team tests internally using hidden toggle (`?aura_backend=smartsdk`) or 5-click advanced mode
4. Once validated with real users, UOP brings results to AURA: *"We tested this MCP, here's the feedback — please add it to AURA production"*
5. When AURA registers the MCP, UOP switches back to the primary backend

**Why this matters:**
- UOP isn't blocked waiting for AURA's release cycle to test new capabilities
- New MCPs get validated with real users before going into AURA production
- Framing to AURA team: *"We're helping you validate MCPs before production — think of it as a staging environment"*
- Framing to MCP owners: *"We can start testing your MCP today, no waiting"*

### Why This Matters

| Benefit | Description |
|---------|-------------|
| **No single-team dependency** | UOP's AI isn't blocked by AURA's uptime or roadmap |
| **Resilience** | AURA outage doesn't mean UOP AI goes dark |
| **Independent iteration** | UOP team can test new MCPs on SmartSDK without waiting for AURA releases |
| **MCP staging environment** | Validate new MCPs with real users before requesting AURA registration |
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
| **Phase 4: FinOps MCP** | Integrate FinOps MCP (via AURA or direct SmartSDK) for cost data | Weeks (depends on DevGPT Cline team) |
| **Phase 5: Developer MCPs** | Add Sourcegraph, Bitbucket, Jira MCPs for code remediation workflow | Weeks |
| **Phase 6: Org-Wide Analytics** | Dashboard widgets for aggregate AI usage, recommendations, adoption rates | Weeks |

Phase 1 and 2 can be delivered immediately — mock FinOps demo + resilient backend architecture.

---

## 9. Summary

UOP's AI strategy is simple: **be the surface, not the engine**.

| Principle | What It Means |
|-----------|---------------|
| **UOP is the surface** | Users come to UOP for AI — not Cline, not a separate AURA portal, not a one-off tool |
| **AURA is the primary engine** | AURA team provides the SmartSDK orchestration, MCPs, IAM, guardrails |
| **SmartSDK is the fallback engine** | UOP can run its own agent if AURA is unavailable or doesn't meet a need |
| **MCPs are pluggable** | Any team can contribute AI capabilities by exposing an MCP — UOP distributes them |
| **The UI is backend-agnostic** | Same chat, same blocks, same experience — regardless of which engine is active |

This positions UOP as a **force multiplier** for every AI initiative in the organization. FinOps reaches more users. AURA gets a high-traffic consumer. Leadership gets centralized governance. And UOP maintains the independence to serve its users regardless of any single team's roadmap.
