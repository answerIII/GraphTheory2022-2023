import pandas as pd
import math
import random
import numpy as np
from collections import deque
import collections

dataset_path = 'datasets/' + 'out.radoslaw_email_email' + '.txt'
# dataset_path = 'datasets/' + 'out.prosper-loans' + '.txt'
data = pd.read_csv(dataset_path, sep='\s+', names=['id_from', 'id_to', 'weight', 'time'], header=None)

def get_adjacency_list(data):
    adjacency_list = dict({})
    edges = dict({})
    time = []
    for row in data.itertuples():
        # if row[4] >= t0 and row[4] <= t1:
        if(row[1] in adjacency_list):
            if(row[2] not in adjacency_list[row[1]]):
                adjacency_list[row[1]].append(row[2])
        else:
            adjacency_list[row[1]] = [row[2]]
        if(row[2] in adjacency_list):
            if(row[1] not in adjacency_list[row[2]]):
                adjacency_list[row[2]].append(row[1])
        else:
            adjacency_list[row[2]] = [row[1]]

        time.append(row[4])

        if (row[1], row[2]) in edges:
            edges[(row[1], row[2])].append(row[4])
        elif (row[2], row[1]) in edges:
            edges[(row[2], row[1])].append(row[4])
        else:
            edges[(row[1], row[2])] = [row[4]]
    return [adjacency_list, min(time), max(time), edges]

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
            AA += (wtf_uz + wtf_vz) / math.log(1 + wtf_zx)
            CN += wtf_uz + wtf_vz
            JC += (wtf_uz + wtf_vz) / (ux_sum + vy_sum)

        PA = ux_sum * vy_sum
        edge_vector.append(AA)
        edge_vector.append(CN)
        edge_vector.append(JC)
        edge_vector.append(PA)

    return edge_vector

adjacency_list, tmin, tmax, edges = get_adjacency_list(data)
for edge in edges:
    edges[edge] = temporal_weighting(edges[edge], tmin, tmax)
    edges[edge] = past_event_aggregation(edges[edge])

edges_copy = edges
for edge in edges:
    edges_copy[edge] = topological_features(edge, adjacency_list, edges)
