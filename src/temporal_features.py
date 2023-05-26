import numpy as np
from graph import Graph


# Max and min time in graph
T_MAX = T_MIN = 0


# Utility functions
def __normalize(value: float, l_bound: float = 0.2) -> float:
    return l_bound + (1 - l_bound) * value

def __get_lin(t: float) -> float:
    global T_MIN, T_MAX
    return (t - T_MIN) / (T_MAX - T_MIN)


# Time strategies
def __lin(t: float) -> float:
    return __normalize(__get_lin(t))

def __exp(t: float) -> float:
    return __normalize((np.exp(3 * __get_lin(t.astype(float))) - 1) / (np.exp(3) - 1))

def __sqrt(t: float) -> float:
    return __normalize(np.sqrt(__get_lin(t.astype(float))))


# All weighting strategies
WEIGHTINGS = (__lin, __exp, __sqrt)

# All past event aggregation strategies
AGGREGATIONS = (np.min, \
                lambda x: np.quantile(x, 0.25), \
                np.median, \
                lambda x: np.quantile(x, 0.75), \
                np.max, \
                np.sum, \
                np.mean, \
                np.var)


# Get weigth of edge(s)
def __wtf(times: np.ndarray, is_multiedge: bool = False) -> np.ndarray:
    if is_multiedge:
        weight = np.fromiter((w(times) for w in WEIGHTINGS), np.ndarray)

        if times.size > 1:
            weight = np.fromiter((a(arr) for a in AGGREGATIONS for arr in weight), np.ndarray)
        else:
            weight = np.fromiter((arr for _ in AGGREGATIONS for arr in weight), np.ndarray)

    else:
        weight = np.fromiter((w(times) for w in WEIGHTINGS), float)

    return weight

# Get final vector of temporal topological features
def get_temporal_features(u: int, v: int, graph: Graph) -> np.ndarray:
    is_multigraph = graph.is_multigraph() 

    vector_size = 3 * (1 + is_multigraph * 7)

    pa = np.zeros((vector_size))
    cn = np.zeros((vector_size))
    jc = np.zeros((vector_size))
    aa = np.zeros((vector_size))

    global T_MIN, T_MAX
    T_MIN = graph.min_timestamp()
    T_MAX = graph.max_timestamp()
    
    neighbors_u = graph.adj(u)
    neighbors_v = graph.adj(v)
    common_neighbors = neighbors_u.intersection(neighbors_v)

    edges_from_u = [graph.get_edges_between(u, z) for z in neighbors_u]
    edges_from_v = [graph.get_edges_between(u, z) for z in neighbors_v]

    times_edges_from_u = np.array( \
        [np.array([graph.get_edge_info(edgeId)[0] for edgeId in edges], float) for edges in edges_from_u if edges], \
        dtype=np.ndarray)
    
    times_edges_from_v = np.array( \
        [np.array([graph.get_edge_info(edgeId)[0] for edgeId in edges], float) for edges in edges_from_v if edges], \
        dtype=np.ndarray)
    
    sum_from_u = np.array([__wtf(time, is_multiedge=is_multigraph) for time in times_edges_from_u], float).sum(axis=0)
    sum_from_v = np.array([__wtf(time, is_multiedge=is_multigraph) for time in times_edges_from_v], float).sum(axis=0)

    pa += sum_from_u * sum_from_v

    for neighbor in common_neighbors:
        neighbors_nb = graph.adj(neighbor)
        edges_from_nb = [graph.get_edges_between(neighbor, z) for z in neighbors_nb]

        times_edges_from_nb = np.array( \
            [np.array([graph.get_edge_info(edgeId)[0] for edgeId in edges], float) for edges in edges_from_nb if edges], \
            dtype=np.ndarray)
        
        sum_from_nb = np.array([__wtf(time, is_multiedge=is_multigraph) for time in times_edges_from_nb], float).sum(axis=0)

        edges_to_u = graph.get_edges_between(neighbor, u)
        edges_to_v = graph.get_edges_between(neighbor, v)

        times_edges_to_u = np.array([graph.get_edge_info(edgeId)[0] for edgeId in edges_to_u], float)
        times_edges_to_v = np.array([graph.get_edge_info(edgeId)[0] for edgeId in edges_to_v], float)

        wtf_u = __wtf(times_edges_to_u, is_multiedge=is_multigraph).astype(float)
        wtf_v = __wtf(times_edges_to_v, is_multiedge=is_multigraph).astype(float)

        cn += wtf_u + wtf_v
        jc += wtf_u + wtf_v

        aa += (wtf_u + wtf_v) / np.where(np.log(1 + sum_from_nb)==0.0, 1e-15, np.log(1 + sum_from_nb))

    jc /= (sum_from_u + sum_from_v)

    return np.concatenate((aa, cn, jc, pa), axis=None)
