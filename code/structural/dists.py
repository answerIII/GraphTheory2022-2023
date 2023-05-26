from collections import deque, defaultdict
from typing import Iterable

import numpy as np

from ..base import Graph, Node

def get_stats(distances):
    return {
        "diameter": distances.max(),
        "radius": distances.max(axis=1).min(),
        "90th_percentile": np.quantile(distances, .9)
    }

def get_distance_between_all(graph: Graph, nodes_ids: Iterable[int]) -> np.ndarray:
    to_reach = set(nodes_ids)
    distances = defaultdict(list)
    
    for root_id in nodes_ids.copy():
        to_reach.remove(root_id)
        to_reach_local = to_reach.copy()
        
        visited = set([root_id])
        
        queue1, queue2 = [graph.nodes[root_id]], []
        d = 1
        
        while queue1 and to_reach_local:
            for node in queue1:
                for neighbor_id in node.neighbors:
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue2.append(graph.nodes[neighbor_id])
                        
                        if neighbor_id in to_reach_local:
                            to_reach_local.remove(neighbor_id)
                            distances[neighbor_id].append(d)
                            distances[root_id].append(d)
                            
            d += 1
            queue1, queue2 = queue2, []
            
    return np.array(list(distances.values()))


def get_distances_random(graph: Graph, n_samples: int = 500, seed: int = 1) -> np.ndarray:
    rng = np.random.RandomState(seed=seed)
    nodes_n = len(graph.nodes)
    nodes_ids = rng.choice(graph.active_nodes, n_samples, replace=False)
    return get_distance_between_all(graph, nodes_ids)


def get_snowball_distance(graph: Graph, start_points_num: int = 3, 
                      max_size: int = 1000, seed: int = 2) -> np.ndarray:
    rng = np.random.RandomState(seed=seed)
    queue: deque[Node] = deque([
        graph.nodes[node_id]
        for node_id in rng.choice(graph.active_nodes, start_points_num, replace=False)
    ])
    visited = {node.u_id for node in queue}
    
    snowball_size = 0
    while snowball_size < max_size and queue:
        node = queue.popleft()
        for neighbor_id in node.neighbors:
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append(graph.nodes[neighbor_id])
                snowball_size += 1
                
    return get_distance_between_all(graph, visited)


def get_dist_stats_for_comp(component: Graph, random_samples=1000, snowball_max_size=1000, do_full=False):
    distances_random = get_distances_random(component, random_samples)
    distances_snowball = get_snowball_distance(component, max_size=snowball_max_size)
    
    estimations = {
        "random": get_stats(distances_random),
        "snowball": get_stats(distances_snowball),
    }
    
    return estimations
