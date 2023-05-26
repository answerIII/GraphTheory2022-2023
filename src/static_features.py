from graph import Graph
import math

# common neighbours
def __get_CN(common_neighbours: set) -> int:
    return len(common_neighbours)

# adamic adar
def __get_AA(common_neighbours: set, graph: Graph) -> float:
    result = 0
    for v in common_neighbours:
        result += 1.0 / math.log(len(graph.adj(v)))
    return result

# jaccard coefficient
def __get_JC(common_neighbours: set, union: set) -> float:
    return len(common_neighbours) / (len(union))

# preferential attachment
def __get_PA(adj_u: set, adj_v: set) -> int:
    return len(adj_u) * len(adj_v)

# this function counts all static properties for (u, v) and returns
# list = [ 'CN', 'AA', 'JC', 'PA' ]
# assuming that given graph is temporal slice
def get_static_properties(u: int, v: int, graph: Graph):
    adj_u: set = graph.adj(u)
    adj_v: set = graph.adj(v)

    common_neighbours = adj_u.intersection(adj_v)
    union = adj_u.union(adj_v)
    
    return [__get_CN(common_neighbours), \
            __get_AA(common_neighbours, graph), \
            __get_JC(common_neighbours, union), \
            __get_PA(adj_u, adj_v)]
