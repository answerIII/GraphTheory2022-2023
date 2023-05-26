import pandas as pd
import math
import random
import numpy as np
from collections import deque
import collections

def temporal_weighting(timestamps, tmin, tmax):
    l = 0.2
    weights = dict({})
    weights['linear'] = [(l + (1 - l) * (i - tmin) / (tmax - tmin)) for i in timestamps]
    weights['exponential'] = [(l + (1 - l) * (math.exp(3 * (i - tmin) / (tmax - tmin)) - 1) / (math.e ** 3 - 1)) for i in timestamps]
    weights['square'] = [(l + (1 - l) * math.sqrt((i - tmin) / (tmax - tmin))) for i in timestamps]

    return weights

def past_event_aggregation(weights):
    weights_agg = []
    for weight_type in weights:
        weights_agg.append(np.quantile(weights[weight_type], 0))
        weights_agg.append(np.quantile(weights[weight_type], 0.25))
        weights_agg.append(np.quantile(weights[weight_type], 0.5))
        weights_agg.append(np.quantile(weights[weight_type], 0.75))
        weights_agg.append(np.quantile(weights[weight_type], 1))
        weights_agg.append(sum(weights[weight_type]))
        weights_agg.append(np.mean(weights[weight_type]))
        weights_agg.append(np.var(weights[weight_type]))

    return weights_agg

def topological_features(edge, adjacency_list, edges):
    Z = set(adjacency_list[edge[0]]) & set(adjacency_list[edge[1]])
    edge_vector = []
    for i in range(24):
        AA = 0
        CN = 0
        JC = 0
        PA = 0

        ux_sum = 0
        for x in adjacency_list[edge[0]]:
            wtf_ux = edges.get((edge[0], x))
            if not wtf_ux:
                wtf_ux = edges.get((x, edge[0]))
            wtf_ux = wtf_ux[i]
            ux_sum += wtf_ux

        vy_sum = 0
        for y in adjacency_list[edge[1]]:
            wtf_vy = edges.get((edge[1], y))
            if not wtf_vy:
                wtf_vy = edges.get((y, edge[1]))
            wtf_vy = wtf_vy[i]
            vy_sum += wtf_vy

        for z in Z:
            wtf_uz = edges.get((edge[0], z))
            if not wtf_uz:
                wtf_uz = edges.get((z, edge[0]))
            wtf_uz = wtf_uz[i]
            wtf_vz = edges.get((edge[1], z))
            if not wtf_vz:
                wtf_vz = edges.get((z, edge[1]))
            wtf_vz = wtf_vz[i]
            zx_sum = 0
            for x in adjacency_list[z]:
                wtf_zx = edges.get((z, x))
                if not wtf_zx:
                    wtf_zx = edges.get((x, z))
                wtf_zx = wtf_zx[i]
                zx_sum += wtf_zx

            if (zx_sum == 0): #Выводит пару вершин, если почему-то получилось деление на ноль
                print('AA: ' + 'u: ' + str(edge[0]) + ' ' + 'v: ' + str(edge[1]) + ' ' + 'z: ' + str(z))
            AA += (wtf_uz + wtf_vz) / math.log(1 + zx_sum)
            CN += wtf_uz + wtf_vz
            if (ux_sum + vy_sum == 0): #Выводит пару вершин, если почему-то получилось деление на ноль
                print('JC: ' + 'u: ' + str(edge[0]) + ' ' + 'v: ' + str(edge[1]) + ' ' + 'z: ' + str(z))
            JC += (wtf_uz + wtf_vz) / (ux_sum + vy_sum)

        PA = ux_sum * vy_sum
        # if math.isnan(CN):
        #     CN = 0
        # if math.isnan(AA):
        #     AA = 0
        # if math.isnan(JC):
        #     JC = 0
        # if math.isnan(PA):
        #     PA = 0
        edge_vector.append(CN)
        edge_vector.append(AA)
        edge_vector.append(JC)
        edge_vector.append(PA)

    return edge_vector

def get_temporal_topological_features(adjacency_list_until_s, tmin, tmax, edges_r_until_s, edges_p, edges_n):

    for edge in edges_r_until_s:
        # Пункты A и B
        edges_r_until_s[edge] = temporal_weighting(edges_r_until_s[edge], tmin, tmax)
        edges_r_until_s[edge] = past_event_aggregation(edges_r_until_s[edge])

    # Пункт C
    for i in range(len(edges_p)):
        u = edges_p[i][0]
        v = edges_p[i][1]
        edges_p[i] = topological_features(edges_p[i], adjacency_list_until_s, edges_r_until_s)

    for i in range(len(edges_n)):
        u = edges_n[i][0]
        v = edges_n[i][1]
        edges_n[i] = topological_features(edges_n[i], adjacency_list_until_s, edges_r_until_s)

    X_new = edges_n + edges_p;
    Y_new = [0] * len(edges_n) + [1] * len(edges_p);

    return X_new, Y_new
