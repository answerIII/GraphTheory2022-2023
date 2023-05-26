import pandas as pd
import math
import random
import numpy as np
from collections import deque
import collections

def common_neighbours(u, v, adjacency_list):
    return len(set(adjacency_list[u]) & set(adjacency_list[v]))


def adamic_adar(u, v, adjacency_list):
    AA = 0
    if u == v:
        return AA
    else:
        Z = set(adjacency_list[u]) & set(adjacency_list[v])
        for z in Z:
            AA += 1 / math.log(len(adjacency_list[z]))
        return AA


def jaccard_coefficient(u, v, adjacency_list):
    return len(set(adjacency_list[u]) & set(adjacency_list[v])) / len(set(adjacency_list[u]) | set(adjacency_list[v]))


def preferential_attachment(u, v, adjacency_list):
    return len(adjacency_list[u]) * len(adjacency_list[v])


def get_static_topological_features(adjacency_list_until_s, edges_p, edges_n):

    # Считаем векторы признаков для positives
    for i in range(len(edges_p)):
        CN = common_neighbours(edges_p[i][0], edges_p[i][1], adjacency_list_until_s)
        AA = adamic_adar(edges_p[i][0], edges_p[i][1], adjacency_list_until_s)
        JC = jaccard_coefficient(edges_p[i][0], edges_p[i][1], adjacency_list_until_s)
        PA = preferential_attachment(edges_p[i][0], edges_p[i][1], adjacency_list_until_s)
        edges_p[i] = [CN, AA, JC, PA]

    # Считаем векторы признаков для negatives
    for i in range(len(edges_n)):
        CN = common_neighbours(edges_n[i][0], edges_n[i][1], adjacency_list_until_s)
        AA = adamic_adar(edges_n[i][0], edges_n[i][1], adjacency_list_until_s)
        JC = jaccard_coefficient(edges_n[i][0], edges_n[i][1], adjacency_list_until_s)
        PA = preferential_attachment(edges_n[i][0], edges_n[i][1], adjacency_list_until_s)
        edges_n[i] = [CN, AA, JC, PA]

    X_new = edges_n + edges_p;
    Y_new = [0] * len(edges_n) + [1] * len(edges_p);
    return  X_new, Y_new