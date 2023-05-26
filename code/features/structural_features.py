from collections import deque

import numpy as np
from scipy.stats import pearsonr 

from ..base import Graph
from ..utils import get_intersection

def get_avg_cluster_coeff(graph: Graph) -> float:
    return np.nanmean([graph.get_subgraph(node.neighbors).density
                       for node in graph.nodes.values()])

def get_deg_assortivity(graph: Graph) -> float:
    degs = np.vectorize(lambda node_id: graph.nodes[node_id].deg)(graph.edges_set)
    return pearsonr(degs[:, 0], degs[:, 1]).statistic

def first_task(graph):
    num_vertices = len(graph.nodes)
    num_edges = len(graph.edges_set)
    density = 2 * num_edges / num_vertices / (num_vertices - 1)

    conn_comps = get_connected_comps(graph)
    conn_comp = graph.get_subgraph(max(conn_comps, key=len))
    max_conn_comp_fraction =  len(conn_comp.nodes) / num_vertices
    
def get_connected_comps(graph: Graph) -> list[list[int]]:
    visited = {u_id : False for u_id in graph.nodes}
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
            if not visited[u_id]:
                for neighbor_id in graph.nodes[u_id].neighbors:
                    if not visited[neighbor_id]:
                        queue.append(neighbor_id)
                        visited[neighbor_id] = True
    return conn_comps