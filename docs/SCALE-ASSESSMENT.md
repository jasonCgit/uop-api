# Scale Assessment: 2,500 Applications

Performance analysis of the UOP platform at 2,500 SEAL applications (currently 81 in mock data).

---

## Summary

The platform works well at ~100 apps but several areas would degrade noticeably at 2,500. The main bottlenecks are **un-virtualized DOM rendering** and **full-list API responses** — the filtering logic itself holds up reasonably well thanks to `useMemo`.

---

## What Would Be Slow

### High Severity

| Area | File(s) | Problem |
|------|---------|---------|
| **Applications card view** | `src/pages/Applications.jsx` | Renders all matching apps to DOM at once via CSS Grid. 2,500 cards = massive DOM, multi-second paint and scroll jank. |
| **AppTable (table view)** | `src/components/AppTable.jsx` | All rows rendered with expand/collapse. No virtual scrolling. Sorting via `useMemo([...filtered].sort())` is fine, but DOM rendering is the bottleneck. |
| **API enrichment** | `app/services/enrichment.py` | `_get_enriched_apps()` enriches every app with components, SLOs, and deployments. Cached in-memory but rebuilds on restart. At 2,500 this could take several seconds per cold request. |
| **Graph explorer** | `src/components/DependencyFlow.jsx` | Dagre layout engine computes positions for all nodes at once. At 2,500+ nodes with proportional edges, layout would freeze the browser for seconds. No viewport culling. |

### Medium Severity

| Area | File(s) | Problem |
|------|---------|---------|
| **Client-side filtering** | `src/FilterContext.jsx` | Loops all apps on every filter change. `useMemo` helps, but cascading filters rebuild multiple passes. At 2,500: ~50-100ms per filter change — noticeable but not broken. |
| **Search suggestions** | `src/components/SearchFilterPopover.jsx` | Joins 8 fields per app into a string, then `.includes()` on all 2,500 on every keystroke. No debounce. |
| **View Central widgets** | `src/view-central/ViewCentralDashboard.jsx` | `ApplicationsWidget` fetches full enriched list and filters client-side. Same DOM issues as Applications page. |

### Fine at Scale

| Area | Why |
|------|-----|
| **Dashboard page** | Server-side filtering returns aggregated summaries, not full lists. |
| **AURA chat** | Independent of app count. |
| **Filter dropdowns** | Distinct values for LOB/CTO/CBT won't grow much even at 2,500 apps. |
| **Announcements, Teams, Contacts** | Separate data, not tied to app count. |

---

## Current Architecture

```
API: GET /api/applications/enriched
  → Returns ALL apps in one response (no pagination)
  → Each app enriched with components, deployments, SLOs, completeness scores
  → Cached at module level (_enriched_cache)

UI: FilterContext.jsx
  → Fetches full list once
  → Filters entirely client-side (useMemo)
  → Multi-field: LOB, Sub-LOB, CTO, CBT, SEAL, status, search text
  → Search: joins 8 fields per app, substring match

UI: AppTable.jsx
  → 3x useMemo (rows, filtered, sorted)
  → All rows rendered to DOM (no virtualization)
  → Expand/collapse state persisted to sessionStorage

UI: Applications.jsx (card view)
  → CSS Grid with auto-fill, all cards rendered
  → Additional client-side text filter layered on top of FilterContext
```

---

## Recommended Fixes

### 1. Server-Side Pagination

Add pagination to `/api/applications/enriched`:

```
GET /api/applications/enriched?page=1&page_size=50&sort=name&search=payment&lob=AWM
```

Returns `{ items: [...], total: 2500, page: 1, pages: 50 }` instead of the full array.

**Files to change:**
- `app/routers/applications.py` — add query params
- `app/services/enrichment.py` — apply pagination after filtering
- `src/pages/Applications.jsx` — fetch per-page instead of full list
- `src/FilterContext.jsx` — convert to server-driven filtering

### 2. Virtualized Lists

Add `react-virtuoso` (or `react-window`) for large scrollable areas:

- **AppTable** — virtualize table rows so only visible rows are in the DOM
- **Card grid** — virtualize the grid so off-screen cards are not rendered
- **View Central widgets** — same treatment for ApplicationsWidget table

**Files to change:**
- `package.json` — add `react-virtuoso`
- `src/components/AppTable.jsx` — wrap rows in virtualized container
- `src/pages/Applications.jsx` — wrap card grid in virtualized container

### 3. Debounced Search

Throttle the search input so filtering doesn't fire on every keystroke:

```javascript
const debouncedSearch = useMemo(
  () => debounce((value) => setSearchText(value), 300),
  []
)
```

**Files to change:**
- `src/FilterContext.jsx` — debounce the search text state update
- `src/components/SearchFilterPopover.jsx` — debounce suggestion computation

### 4. Graph Viewport Culling

Only render nodes visible in the viewport, or cluster nodes by LOB/tier:

- Use `@xyflow/react` built-in viewport awareness to skip off-screen nodes
- Cluster 2,500 apps into ~20 LOB groups, expand on click
- Lazy-load edges on node expansion

**Files to change:**
- `src/components/DependencyFlow.jsx` — add clustering or viewport-aware rendering
- `app/services/graph_engine.py` — add clustered graph endpoint

### 5. API Caching Layer

Pre-compute enrichment instead of building on-demand:

- Background task rebuilds enriched cache on a schedule (or on data change)
- Redis or similar for shared cache across API pods
- Cache invalidation on app metadata updates

**Files to change:**
- `app/services/enrichment.py` — add cache warming strategy
- `app/config.py` — add `CACHE_URL` config

---

## Priority Order

| Priority | Fix | Impact | Effort |
|----------|-----|--------|--------|
| 1 | Server-side pagination | Eliminates full-list API response and client-side filtering bottleneck | Medium |
| 2 | Virtualized lists | Fixes DOM rendering — the single biggest UI bottleneck | Medium |
| 3 | Debounced search | Quick win — prevents keystroke-level re-filtering | Low |
| 4 | API caching | Eliminates cold-start enrichment delay | Medium |
| 5 | Graph clustering | Only needed if graph grows proportionally with apps | High |
