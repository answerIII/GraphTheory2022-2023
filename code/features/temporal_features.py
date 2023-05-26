import numpy as np
import pandas as pd
from numba import njit
from numba.typed import List

from ..utils import get_intersection
from ..base import StaticGraph

@njit
def _feat(weight):
    if weight.size == 1:
        t = weight[0]
        return np.array([t, t, t, t, t, t, t, 0])
    
    return np.array([
        *np.quantile(weight, [0, .25, .5, .75, 1]),
        weight.sum(),
        weight.mean(),
        weight.var()
    ])

@njit
def intersection_indices(first, second, offset):
    i = j = k = 0
    buffer = np.empty(min(first.size, second.size), dtype=first.dtype)
    while i < first.size and j < second.size:
        if first[i] == second[j]:
            buffer[k] = i + offset
            k += 1
            i += 1
            j += 1
        elif first[i] < second[j]:
            i += 1
        else: 
            j += 1
    return buffer[:k]

@njit
def calc(timestamps_global, edges_grouped, time_grouped,
         edges, intersections, lower_bound):
    
    EPS = 1e-5
    
    edges = edges[:, :2]
    t_min, t_max = timestamps_global.min(), timestamps_global.max()
    wtf = np.zeros((len(time_grouped), 24))
    
    for time_idx, time in enumerate(time_grouped):
        dt = (time - t_min) / (t_max - t_min)
        wtf[time_idx, : 8] = _feat(lower_bound + (1 - lower_bound) * dt)
        wtf[time_idx, 8 : 16] = _feat(lower_bound + (1 - lower_bound) * (np.exp(3 * dt) - 1) / (np.exp(3) - 1))
        wtf[time_idx, 16 : 24] = _feat(lower_bound + (1 - lower_bound) * np.sqrt(dt))
        
    # sorting by 2 arguments
    e_g = np.vstack((edges_grouped, edges_grouped[:, ::-1]))
    order_last = np.argsort(e_g[:, -1])
    order_first = np.argsort(e_g[order_last, 0], kind="mergesort")
    order = order_last[order_first]
    
    wtf = np.vstack((wtf, wtf))[order]
    e_g = e_g[order]
    
    # definining borders of equals
    col = e_g[:, 0]
    end = e_g[:, 1]
    size = col.max() + 1
    indices = np.zeros((size, 2), np.int32)
    summ = np.zeros((size, 24), np.float64)
    
    nonzero = np.concatenate((
        np.nonzero(col[1:] - col[:-1])[0], 
        np.array([col.size - 1])
    ))
    indices[col[nonzero[1:]], 0] = nonzero[:-1] + 1
    indices[col[nonzero], 1] = nonzero + 1
    
    for idx, (fr, to) in enumerate(indices[col[nonzero]]):
        for i in range(fr, to):
            summ[col[nonzero[idx]]] += wtf[i]
    
    # calculating features for edge requests
    output = np.zeros((len(intersections), 96))
    for idx, (node_indices, intersection) in enumerate(zip(edges, intersections)):
        jc_denom = summ[node_indices[0]] + summ[node_indices[1]] + EPS
        output[idx, 72:] = summ[node_indices[0]] * summ[node_indices[1]]
        for node_index in node_indices:            
            fr, to = indices[node_index]
            inters = intersection_indices(end[fr : to], intersection, fr)
            output[idx, :72] += np.hstack((
                wtf[inters] / np.log(1 + summ[end[inters]] + EPS), # AA
                wtf[inters], # CN
                wtf[inters] / jc_denom, # JC
            )).sum(axis=0)
            
    return output

def compute_temporal_features(graph: StaticGraph, edges: np.ndarray, lower_bound):
    grouped = pd.DataFrame({"v1": graph.edges[:, 0], "v2": graph.edges[:, 1], "time": graph.timestamps})\
        .groupby(["v1", "v2"])\
        ["time"].apply(np.array)
    
    intersections = []
    for first_id, second_id, *_ in edges:
        intersection = get_intersection(graph.nodes[first_id].neighbors, graph.nodes[second_id].neighbors)
        intersections.append(intersection)
    
    needed_vertices = np.sort(np.concatenate((
        np.concatenate(intersections),
        np.concatenate(edges[:, :2])
    )))
    idx1, idx2 = map(np.array, zip(*grouped.index))
    idx2 = np.sort(idx2)
    needed_edges = pd.concat([
        grouped.loc[get_intersection(idx1, needed_vertices), :],
        grouped.loc[:, get_intersection(idx2, needed_vertices)]
    ])
    needed_edges = needed_edges[~needed_edges.index.duplicated()]

    features = calc(graph.timestamps, np.array(list(map(list, needed_edges.index))),
                    List(needed_edges.values), edges, List(intersections), lower_bound)
    
    return features
    
