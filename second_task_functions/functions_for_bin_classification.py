import math


def weighted_topological_features_linear(graph, a, b, tmin, tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    l = 0.2
    return l + (1 - l) * (t - tmin) / (tmax - tmin)

def weighted_topological_features_exp(graph, a, b, tmin, tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    l = 0.2
    return l + (1 - l) * (math.exp(3 * (t - tmin) / (tmax - tmin)) - 1) / (math.e ** 3 - 1)

def weighted_topological_features_square(graph, a, b, tmin, tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    l = 0.2
    return l + (1 - l) * (math.sqrt((t - tmin) / (tmax - tmin)))