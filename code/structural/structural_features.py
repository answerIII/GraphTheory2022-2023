from collections import deque
import time

import numpy as np
from scipy.stats import pearsonr
import gc

from code.features.feature_extraction import load_graph

from ..base import Graph
from .dists import get_dist_stats_for_comp
import drq


def get_avg_cluster_coeff(graph: Graph) -> float:
    arr = []
    for node in graph.nodes.values():
        if len(node.neighbors) >= 2:
            arr.append(graph.get_subgraph(node.neighbors).density)
        else:
            arr.append(0)
    return np.mean(arr)


def get_deg_assortivity(graph: Graph) -> float:
    degs = np.vectorize(lambda node_id: graph.nodes[node_id].deg)(graph.edges_set)
    return pearsonr(degs[:, 0], degs[:, 1]).statistic


def get_connected_comps(graph: Graph) -> list[list[int]]:
    visited = {u_id: False for u_id in graph.nodes}
    queue = deque(graph.nodes)
    conn_comps: list[list[int]] = []

    for root_u_id in graph.nodes.keys():
        if visited[root_u_id]:
            continue

        queue = deque([root_u_id])
        conn_comps.append([])

        while queue:
            u_id = queue.popleft()
            conn_comps[-1].append(u_id)
            for neighbor_id in graph.nodes[u_id].neighbors:
                if not visited[neighbor_id]:
                    queue.append(neighbor_id)
                    visited[neighbor_id] = True
    return conn_comps


def first_task(path: str, full: bool = False, threads=16) -> dict[str, float | int]:
    t1 = time.time()
    graph = load_graph(path)
    num_vertices = len(graph.nodes)
    num_edges = len(graph.edges)
    density = graph.density

    conn_comps = get_connected_comps(graph)

    max_conn_comp = graph.get_subgraph(max(conn_comps, key=len))
    conn_comps = len(conn_comps)
    max_conn_comp_fraction = len(max_conn_comp.nodes) / num_vertices

    cl = get_avg_cluster_coeff(max_conn_comp)
    r = get_deg_assortivity(max_conn_comp)

    if full or num_vertices < 31000:
        graph.clear()
        del graph
        del max_conn_comp

        gc.collect()

        max_conn_comp = None
        diam, rad, q = drq.find_drq(path, threads)
        dist_stats = {"diameter": diam, "radius": rad, "90th_percentile": q}
    else:
        dist_stats = get_dist_stats_for_comp(max_conn_comp)
    t3 = time.time()
    return {
        "num_vertices": num_vertices,
        "num_edges": num_edges,
        "density": density,
        "conn_comps": conn_comps,
        "max_conn_comp_fraction": max_conn_comp_fraction,
        "cl": cl,
        "r": r,
        "full_time_secs": t3 - t1,
        **dist_stats,
    }
