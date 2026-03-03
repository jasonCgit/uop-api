from fastapi import APIRouter, HTTPException

from app.services.graph_engine import NODE_MAP, bfs, forward_adj, reverse_adj
from app.mock_data import (
    NODES,
    EDGES_RAW,
    SEAL_COMPONENTS,
    SEAL_LABELS,
    BIDIRECTIONAL_PAIRS,
    INDICATOR_NODES,
    PLATFORM_NODES,
    COMPONENT_PLATFORM_EDGES,
    DATA_CENTER_NODES,
    DC_LOOKUP,
    COMP_TO_SEAL,
)

router = APIRouter()


@router.get("/api/graph/nodes")
def get_all_nodes():
    return NODES


@router.get("/api/graph/dependencies/{service_id}")
def get_dependencies(service_id: str):
    if service_id not in NODE_MAP:
        raise HTTPException(status_code=404, detail=f"Service '{service_id}' not found")
    dep_ids = bfs(service_id, forward_adj)
    root = NODE_MAP[service_id]
    dependencies = [NODE_MAP[i] for i in dep_ids if i in NODE_MAP]

    subgraph_ids = {service_id} | set(dep_ids)
    edges = []
    for src, dst in EDGES_RAW:
        if src in subgraph_ids and dst in subgraph_ids:
            edges.append({"source": src, "target": dst})

    return {"root": root, "dependencies": dependencies, "edges": edges}


@router.get("/api/graph/blast-radius/{service_id}")
def get_blast_radius(service_id: str):
    if service_id not in NODE_MAP:
        raise HTTPException(status_code=404, detail=f"Service '{service_id}' not found")
    impacted_ids = bfs(service_id, reverse_adj)
    root = NODE_MAP[service_id]
    impacted = [NODE_MAP[i] for i in impacted_ids if i in NODE_MAP]

    subgraph_ids = {service_id} | set(impacted_ids)
    edges = []
    for src, dst in EDGES_RAW:
        if src in subgraph_ids and dst in subgraph_ids:
            edges.append({"source": src, "target": dst})

    return {"root": root, "impacted": impacted, "edges": edges}


@router.get("/api/graph/layer-seals")
def get_layer_seals():
    return [
        {"seal": s, "label": l, "component_count": len(SEAL_COMPONENTS[s])}
        for s, l in [
            ("16649", "Morgan Money"),
            ("35115", "PANDA"),
            ("88180", "Connect OS"),
            ("90176", "Advisor Connect"),
            ("81884", "Order Decision Engine"),
            ("91001", "Quantum"),
            ("45440", "Credit Card Processing Engine"),
            ("102987", "AWM Entitlements (WEAVE)"),
            ("90215", "Spectrum Portfolio Mgmt"),
            ("62100", "Real-Time Payments Gateway"),
        ]
    ]


@router.get("/api/graph/layers/{seal_id}")
def get_graph_layers(seal_id: str):
    if seal_id not in SEAL_COMPONENTS:
        raise HTTPException(status_code=404, detail=f"SEAL '{seal_id}' not found")

    component_ids = SEAL_COMPONENTS[seal_id]
    component_set = set(component_ids)

    # Component layer
    component_nodes = [NODE_MAP[cid] for cid in component_ids if cid in NODE_MAP]
    component_edges = []
    external_ids: set[str] = set()
    external_dirs: dict[str, set[str]] = {}
    for src, dst in EDGES_RAW:
        src_in = src in component_set
        dst_in = dst in component_set
        direction = "bi" if (src, dst) in BIDIRECTIONAL_PAIRS or (dst, src) in BIDIRECTIONAL_PAIRS else "uni"
        if src_in and dst_in:
            component_edges.append({"source": src, "target": dst, "direction": direction})
        elif src_in and dst in COMP_TO_SEAL and COMP_TO_SEAL[dst] != seal_id:
            component_edges.append({"source": src, "target": dst, "direction": direction, "cross_seal": COMP_TO_SEAL[dst]})
            external_ids.add(dst)
            external_dirs.setdefault(dst, set()).add("downstream")
        elif dst_in and src in COMP_TO_SEAL and COMP_TO_SEAL[src] != seal_id:
            component_edges.append({"source": src, "target": dst, "direction": direction, "cross_seal": COMP_TO_SEAL[src]})
            external_ids.add(src)
            external_dirs.setdefault(src, set()).add("upstream")
    external_nodes = [
        {
            **NODE_MAP[eid],
            "external": True,
            "external_seal": COMP_TO_SEAL[eid],
            "external_seal_label": SEAL_LABELS.get(COMP_TO_SEAL[eid], COMP_TO_SEAL[eid]),
            "cross_direction": sorted(external_dirs.get(eid, {"downstream"}))[0] if len(external_dirs.get(eid, set())) == 1 else "both",
        }
        for eid in external_ids if eid in NODE_MAP
    ]

    # Platform layer
    platform_node_ids: set[str] = set()
    platform_edge_list = []
    for comp_id, plat_id in COMPONENT_PLATFORM_EDGES:
        if comp_id in component_set:
            platform_edge_list.append({"source": comp_id, "target": plat_id, "layer": "platform"})
            platform_node_ids.add(plat_id)
    platform_nodes = [pn for pn in PLATFORM_NODES if pn["id"] in platform_node_ids]

    # Data Center layer
    dc_node_ids: set[str] = set()
    dc_edge_list = []
    for pn in platform_nodes:
        dc_id = DC_LOOKUP.get(pn["datacenter"])
        if dc_id:
            dc_edge_list.append({"source": pn["id"], "target": dc_id, "layer": "datacenter"})
            dc_node_ids.add(dc_id)
    dc_nodes = [dc for dc in DATA_CENTER_NODES if dc["id"] in dc_node_ids]

    # Indicator layer
    indicator_nodes = [ind for ind in INDICATOR_NODES if ind["component"] in component_set]
    indicator_edges = [
        {"source": ind["component"], "target": ind["id"], "layer": "indicator"}
        for ind in indicator_nodes
    ]

    return {
        "seal": seal_id,
        "components": {"nodes": component_nodes, "edges": component_edges, "external_nodes": external_nodes},
        "platform":   {"nodes": platform_nodes,   "edges": platform_edge_list},
        "datacenter": {"nodes": dc_nodes,          "edges": dc_edge_list},
        "indicators": {"nodes": indicator_nodes,   "edges": indicator_edges},
    }
