# Database Schema Recommendation

Analysis of the proposed UOP database schema and recommendations for performance at 2,500+ SEALs.

---

## Current Schema (13 Tables)

```
application ─┬─► deployment ─┬─► cloudfoundrycomponent ─┬─► cfc_pool ──► gap_platform ──► Datacenter
             │               │                          └─► cfc_indicator ──► Indicator
             │               │
             │               └─► gkppod ─┬─► gkp_cluster ──► gkp_platform ──► Datacenter
             │                           └─► gkp_indicator ──► Indicator
             │
             └─► (future: aws component?) ──► aws_platform
```

### Tables

| Layer | Table | PK | Key FKs |
|-------|-------|----|---------|
| App | `application` | id | — |
| Deployment | `deployment` | deployment_id | seal |
| Component | `cloudfoundrycomponent` | id | seal, deployment_id |
| Component | `gkppod` | id | seal, deployment_id |
| Junction | `cfc_pool` | (cfc_id, platform_id) | — |
| Junction | `gkp_cluster` | (gkppod_id, platform_id) | — |
| Junction | `cfc_indicator` | (cfc_id, indicator_id) | — |
| Junction | `gkp_indicator` | (cfc_id, indicator_id) | — |
| Platform | `gap_platform` | id | datacenter_name |
| Platform | `gkp_platform` | id | datacenter_name |
| Platform | `aws_platform` | id | — |
| Infra | `Datacenter` | name | — |
| Indicator | `Indicator` (DynatraceEntities) | id | — |

---

## Problem: Table-Per-Type Antipattern

### Components are nearly identical

| Column | `cloudfoundrycomponent` | `gkppod` |
|--------|------------------------|----------|
| id | int | int |
| seal | varchar(10) | varchar(10) |
| deployment_id | int | int |
| name / pod_name | varchar | varchar |
| env | varchar | varchar |
| create_time | timestamp | timestamp |
| update_time | timestamp | timestamp |
| status_code | int | int |
| status_update_time | int | int |
| namespace | — | varchar |

The only difference is `gkppod` has a `namespace` column. Every other column is identical.

### Platforms are nearly identical

| Column | `gap_platform` | `gkp_platform` | `aws_platform` |
|--------|---------------|---------------|---------------|
| id | int | int | int |
| type | Type | Type | Type |
| env | varchar | varchar | varchar |
| name (pool/cluster) | pool_name | cluster_name | name |
| datacenter | FK | FK | — |

Same structure, different column names for the same concept.

### Why this hurts at scale

The enrichment query (the main UOP-API call) needs all components, platforms, and indicators for a set of SEALs. With split tables:

```sql
-- Components: UNION required
SELECT id, seal, deployment_id, name, env, status_code
  FROM cloudfoundrycomponent WHERE seal IN (...)
UNION ALL
SELECT id, seal, deployment_id, pod_name, env, status_code
  FROM gkppod WHERE seal IN (...)

-- Indicators: separate join paths
SELECT i.* FROM indicator i
  JOIN cfc_indicator ci ON ci.indicator_id = i.id
  WHERE ci.cfc_id IN (...)
UNION ALL
SELECT i.* FROM indicator i
  JOIN gkp_indicator gi ON gi.indicator_id = i.id
  WHERE gi.cfc_id IN (...)

-- Platforms: 3-way UNION through different junction tables
SELECT p.* FROM gap_platform p
  JOIN cfc_pool cp ON cp.platform_id = p.id
  WHERE cp.cfc_id IN (...)
UNION ALL
SELECT p.* FROM gkp_platform p
  JOIN gkp_cluster gc ON gc.platform_id = p.id
  WHERE gc.gkppod_id IN (...)
UNION ALL
SELECT * FROM aws_platform WHERE ...
```

At 2,500 SEALs with thousands of components, this means:
- Multiple UNIONs across separate B-trees
- Query planner cannot optimize across table boundaries
- Every new platform type requires 3 new tables + new queries
- ORM code branches on type everywhere

---

## Recommended Schema (7 Tables)

Merge component types and platform types into single tables with a `type` discriminator.

```
application ──► deployment ──► component ──┬──► component_platform ──► platform ──► Datacenter
                                           └──► component_indicator ──► Indicator
```

### `application` (unchanged)

```sql
CREATE TABLE application (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    seal                VARCHAR(10) NOT NULL,
    lob                 VARCHAR(10),
    name                VARCHAR(200),
    party_type          VARCHAR(50),
    hosting_indicator   VARCHAR(50),
    cpof                VARCHAR(10),
    state               VARCHAR(10),
    ao                  VARCHAR(100),
    cto                 VARCHAR(100),
    cbt                 VARCHAR(100),
    risk_ranking        VARCHAR(10),
    app_classification  VARCHAR(50),
    status_code         INT,
    status_update_time  INT,
    slo_update_time     INT,
    slo                 FLOAT,
    slo_target          FLOAT,
    error_budget        FLOAT,
    rto                 VARCHAR(10),

    UNIQUE INDEX idx_seal (seal),
    INDEX idx_lob (lob),
    INDEX idx_cto (cto),
    INDEX idx_cbt (cbt),
    INDEX idx_status (status_code)
);
```

### `deployment` (unchanged)

```sql
CREATE TABLE deployment (
    deployment_id       INT PRIMARY KEY AUTO_INCREMENT,
    seal                VARCHAR(10) NOT NULL,
    deployment_name     VARCHAR(255),
    cpof                VARCHAR(255),
    rto                 VARCHAR(255),

    INDEX idx_seal (seal),
    FOREIGN KEY (seal) REFERENCES application(seal)
);
```

### `component` (merged from cloudfoundrycomponent + gkppod)

```sql
CREATE TABLE component (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    seal                VARCHAR(10) NOT NULL,
    deployment_id       INT NOT NULL,
    type                VARCHAR(20) NOT NULL,  -- 'cloudfoundry', 'gkp', 'aws'
    name                VARCHAR(255),
    namespace           VARCHAR(255),          -- NULL for non-GKP
    env                 VARCHAR(50),
    create_time         TIMESTAMP,
    update_time         TIMESTAMP,
    status_code         INT,
    status_update_time  INT,

    INDEX idx_seal (seal),
    INDEX idx_seal_deployment (seal, deployment_id),
    INDEX idx_type (type),
    FOREIGN KEY (seal) REFERENCES application(seal),
    FOREIGN KEY (deployment_id) REFERENCES deployment(deployment_id)
);
```

### `platform` (merged from gap_platform + gkp_platform + aws_platform)

```sql
CREATE TABLE platform (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    type                VARCHAR(20) NOT NULL,  -- 'gap', 'gkp', 'aws'
    env                 VARCHAR(50),
    name                VARCHAR(255),          -- pool_name / cluster_name / name
    datacenter_name     VARCHAR(255),

    INDEX idx_type (type),
    FOREIGN KEY (datacenter_name) REFERENCES datacenter(name)
);
```

### `datacenter` (unchanged)

```sql
CREATE TABLE datacenter (
    name                VARCHAR(255) PRIMARY KEY,
    region              VARCHAR(255)
);
```

### `component_platform` (merged from cfc_pool + gkp_cluster)

```sql
CREATE TABLE component_platform (
    component_id        INT NOT NULL,
    platform_id         INT NOT NULL,

    PRIMARY KEY (component_id, platform_id),
    FOREIGN KEY (component_id) REFERENCES component(id),
    FOREIGN KEY (platform_id) REFERENCES platform(id)
);
```

### `component_indicator` (merged from cfc_indicator + gkp_indicator)

```sql
CREATE TABLE component_indicator (
    component_id        INT NOT NULL,
    indicator_id        INT NOT NULL,

    PRIMARY KEY (component_id, indicator_id),
    FOREIGN KEY (component_id) REFERENCES component(id),
    FOREIGN KEY (indicator_id) REFERENCES indicator(id)
);
```

### `indicator` (unchanged)

```sql
CREATE TABLE indicator (
    id                  INT PRIMARY KEY AUTO_INCREMENT,
    name                VARCHAR(255),
    datasource_id       INT,
    external_id         VARCHAR(50),
    entity_type         VARCHAR(50),
    service_type        VARCHAR(50),
    seal                VARCHAR(10),
    status_code         INT,
    status_update_time  INT,
    url                 VARCHAR(500),
    create_time         INT,
    update_time         INT,
    last_seen_timestamp TIMESTAMP,

    INDEX idx_seal (seal),
    INDEX idx_external (external_id),
    INDEX idx_entity_type (entity_type)
);
```

---

## Enrichment Query (After Merge)

The main query UOP-API runs to build the enriched app list:

```sql
SELECT
    a.seal, a.name, a.lob, a.cto, a.cbt, a.slo_target,
    d.deployment_id, d.deployment_name,
    c.id AS component_id, c.type AS component_type, c.name AS component_name,
    c.status_code AS component_status,
    p.id AS platform_id, p.type AS platform_type, p.name AS platform_name,
    p.datacenter_name,
    i.id AS indicator_id, i.name AS indicator_name, i.entity_type,
    i.status_code AS indicator_status
FROM application a
JOIN deployment d ON d.seal = a.seal
JOIN component c ON c.seal = a.seal AND c.deployment_id = d.deployment_id
LEFT JOIN component_platform cp ON cp.component_id = c.id
LEFT JOIN platform p ON p.id = cp.platform_id
LEFT JOIN component_indicator ci ON ci.component_id = c.id
LEFT JOIN indicator i ON i.id = ci.indicator_id
WHERE a.seal IN (...)
ORDER BY a.seal, d.deployment_id, c.id;
```

One query. No UNIONs. The query planner uses `idx_seal` on `component` and the composite PKs on junction tables.

---

## Comparison

| Metric | Current (split) | Recommended (merged) |
|--------|-----------------|---------------------|
| Total tables | 13 | 7 |
| Junction tables | 4 | 2 |
| Enrichment query | 3 UNIONs, 6+ join paths | 1 query, 5 JOINs |
| New platform type | 3 new tables + new code | 1 new `type` value |
| ORM complexity | Branching on type everywhere | Single model per concern |
| Index scans | Across 5+ separate B-trees | 2 B-trees (component, platform) |
| Query plan cacheability | Poor (UNION plans vary) | Good (single stable plan) |

---

## What Stays the Same

- **`application`** — no changes needed
- **`deployment`** — no changes needed
- **`datacenter`** — no changes needed
- **`indicator`** (DynatraceEntities) — already unified, no changes needed

---

## Indexing Strategy for 2,500 SEALs

Critical indexes for the enrichment query:

| Table | Index | Purpose |
|-------|-------|---------|
| `application` | `idx_seal` (UNIQUE) | PK lookup by SEAL |
| `application` | `idx_lob`, `idx_cto`, `idx_cbt` | Dashboard filter queries |
| `deployment` | `idx_seal` | Get deployments for a SEAL |
| `component` | `idx_seal_deployment` | Get components for a SEAL + deployment |
| `component` | `idx_type` | Filter by platform type if needed |
| `component_platform` | PK `(component_id, platform_id)` | Junction lookup |
| `component_indicator` | PK `(component_id, indicator_id)` | Junction lookup |
| `indicator` | `idx_seal` | Indicator lookup by SEAL |
| `indicator` | `idx_external` | Dynatrace entity cross-reference |

At 2,500 SEALs with ~10 components each = ~25,000 component rows. With proper indexes, the enrichment query runs in single-digit milliseconds.

---

## Migration Path

If migrating from the split schema to the merged schema:

1. Create new `component`, `platform`, `component_platform`, `component_indicator` tables
2. Migrate data:
   ```sql
   INSERT INTO component (seal, deployment_id, type, name, namespace, env, ...)
   SELECT seal, deployment_id, 'cloudfoundry', name, NULL, env, ...
   FROM cloudfoundrycomponent;

   INSERT INTO component (seal, deployment_id, type, name, namespace, env, ...)
   SELECT seal, deployment_id, 'gkp', pod_name, namespace, env, ...
   FROM gkppod;
   ```
3. Migrate junction tables with updated component IDs
4. Verify row counts match
5. Drop old tables
