import numpy as np
from numba import njit

from ..utils import get_intersection
from ..base import StaticGraph

@njit
def get_static_features_for_pair(first_neighbors, second_neighbors, degrees):
    intersection = get_intersection(first_neighbors, second_neighbors)
    first_deg, second_deg = first_neighbors.size, second_neighbors.size
    return np.array([
        intersection.size, # CN
        (1 / np.log(degrees[intersection])).sum(), # AA
        intersection.size / (first_deg + second_deg - intersection.size), ## JC
        first_deg * second_deg # PA
    ])

def compute_static_features(graph: StaticGraph, edges: np.ndarray):
    ids = list(graph.nodes.keys())
    degrees_raw = [node.deg for node in graph.nodes.values()]
    
    degrees = np.zeros(graph.network.total_nodes + 1)
    degrees[ids] = degrees_raw
    
    features = np.vstack([
        get_static_features_for_pair(
            graph.nodes[first_id].neighbors, graph.nodes[second_id].neighbors,
            degrees
        ) for first_id, second_id, *_ in edges
    ])
    
    return features