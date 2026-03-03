from collections import deque

from app.mock_data import NODES, EDGES_RAW, INDICATOR_NODES

# Precompute adjacency maps once at startup
NODE_MAP = {n["id"]: n for n in NODES}

# Components that have at least one health indicator — others get "no_data"
COMPONENTS_WITH_INDICATORS: set[str] = {ind["component"] for ind in INDICATOR_NODES}

forward_adj: dict[str, list[str]] = {n["id"]: [] for n in NODES}
reverse_adj: dict[str, list[str]] = {n["id"]: [] for n in NODES}

for src, dst in EDGES_RAW:
    forward_adj[src].append(dst)
    reverse_adj[dst].append(src)


def bfs(start_id: str, adj: dict[str, list[str]]) -> list[str]:
    visited: set[str] = {start_id}
    queue: deque[str] = deque([start_id])
    result: list[str] = []
    while queue:
        curr = queue.popleft()
        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                result.append(neighbor)
                queue.append(neighbor)
    return result


def _effective_status(cid):
    node = NODE_MAP.get(cid)
    if not node:
        return "no_data"
    # Components without health indicators -> no_data
    if cid not in COMPONENTS_WITH_INDICATORS:
        return "no_data"
    own = node["status"]
    dep_ids = bfs(cid, forward_adj)
    worst = own
    _status_rank = {"critical": 0, "warning": 1, "healthy": 2, "no_data": 3}
    for did in dep_ids:
        dn = NODE_MAP.get(did)
        if not dn:
            continue
        dep_status = dn["status"] if did in COMPONENTS_WITH_INDICATORS else "no_data"
        if dep_status == "no_data":
            continue
        if _status_rank.get(dep_status, 9) < _status_rank.get(worst, 9):
            worst = dep_status
    return worst
