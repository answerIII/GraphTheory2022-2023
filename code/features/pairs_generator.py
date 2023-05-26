import numpy as np

from ..base import StaticGraph
from ..utils import get_intersection

def get_all_pairs(current_graph: StaticGraph, future_graph: StaticGraph):
    has_link = []
    no_link = []
    
    visited = np.zeros(len(current_graph.nodes) + 1, dtype=bool)
    for node in current_graph.nodes.values():
        if node.deg <= 1:
            continue
        
        visited[np.concatenate([current_graph.nodes[neighbor_id].neighbors
                                for neighbor_id in node.neighbors])] = True
        visited[node.u_id] = False
        intersection = get_intersection(future_graph.nodes[node.u_id].neighbors, visited.nonzero()[0]).astype(int)
        has_link.append(np.vstack([np.full_like(intersection, node.u_id), intersection]))
        visited[intersection] = False
        
        no_link_t = visited.nonzero()[0]
        no_link.append(np.vstack([np.full_like(no_link_t, node.u_id), no_link_t]))
        visited[no_link_t] = False
    has_link, no_link = [np.hstack(arrs).T for arrs in [has_link, no_link]]
    return has_link, no_link

def get_train_set(graph: StaticGraph, seed: int = 42, size: int = 10_000):
    rng = np.random.RandomState(seed=seed)
    
    future_graph = StaticGraph.from_time_slice(graph.network, 1, graph.quantile_end)
    has_link, no_link = get_all_pairs(graph, future_graph)
    train_edges = np.hstack([
        np.vstack([
            has_link[rng.choice(len(has_link), size)],
            no_link[rng.choice(len(no_link), size)]
        ]),
        np.repeat([1, 0], size).reshape(-1, 1)
    ])
    return train_edges