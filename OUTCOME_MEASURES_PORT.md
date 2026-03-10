# Porting Outcome Measures

Files and changes needed to add the Outcome Measures tab to a clean UOP deployment.

## New files (copy wholesale)

| Repo | File | Description |
|------|------|-------------|
| uop-api | `app/mock_data/outcome_measures_data.py` | Mock data |
| uop-api | `app/routers/outcome_measures.py` | API endpoints |
| uop-ui | `src/pages/OutcomeMeasures.jsx` | Page component |

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
