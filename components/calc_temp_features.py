from components.calculator import Calculator
import math
from collections import defaultdict
import time
import pandas as pd


class Temporal_calculator(Calculator):

    def calc(self, current_graph, filename, max):
        filepath = 'datasets/' + filename + '.csv'
        graph, count_node, count_edge, tmin, tmax = read_edge_for_bin(filepath)

        df = pd.DataFrame({'def': [], 'u': [], 'v': [],
                        'cnwl': [], 'aawl': [], 'jcwl': [], 'pawl': [],
                        'cnws': [], 'aaws': [], 'jcws': [], 'paws': [],
                        'cnwe': [], 'aawe': [], 'jcwe': [], 'pawe': [], 'time': []})
        pos_counter = 0
        neg_counter = 0
      


        print('Начинаю вычислять признаки')
        for i in graph:
            if ((pos_counter >= max) and (neg_counter >= max)):
                    break
            
            jaccard_linear1 = 0
            jaccard_exp1 = 0
            jaccard_square1 = 0
            for l1 in graph[i]['neigh']:
                jaccard_linear1 += weighted_topological_features_linear(graph, i, l1, tmin, tmax)
                jaccard_exp1 += weighted_topological_features_exp(graph, i, l1, tmin, tmax)
                jaccard_square1 += weighted_topological_features_square(graph, i, l1, tmin, tmax)
            for j in graph:
                if ((pos_counter > max) and (neg_counter > max)):
                    break
                jaccard_linear2 = 0
                jaccard_exp2 = 0
                jaccard_square2 = 0

                for l2 in graph[j]['neigh']:
                    jaccard_linear2 += weighted_topological_features_linear(graph, j, l2, tmin, tmax)
                    jaccard_exp2 += weighted_topological_features_exp(graph, j, l2, tmin, tmax)
                    jaccard_square2 += weighted_topological_features_square(graph, j, l2, tmin, tmax)

                common_neigh_linear = 0
                adamic_linear = 0
                jaccard_linear = 0
                preferential_linear = 0
                common_neigh_exp = 0
                adamic_exp = 0
                jaccard_exp = 0
                preferential_exp = 0
                common_neigh_square = 0
                adamic_square = 0
                jaccard_square = 0
                preferential_square = 0

                if ((pos_counter > max) and (neg_counter > max)):
                    break
                
                for k in graph[i]['neigh']:
                    
                    if k in graph[j]['neigh']:
                        if ((pos_counter > max) and (neg_counter > max)):
                            break
                        adamic_linear1 = 0
                        adamic_square1 = 0
                        adamic_exp1 = 0
                        common_neigh_linear = common_neigh_linear + weighted_topological_features_linear(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)
                        common_neigh_square = common_neigh_square + weighted_topological_features_square(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)
                        common_neigh_exp = common_neigh_exp + weighted_topological_features_exp(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)
                        for l in graph[i]['neigh']:
                            if l in graph[j]['neigh'] and l in graph[k]['neigh']:
                                adamic_linear1 += weighted_topological_features_linear(graph, k, l, tmin, tmax)
                                adamic_square1 += weighted_topological_features_square(graph, k, l, tmin, tmax)
                                adamic_exp1 += weighted_topological_features_exp(graph, k, l, tmin, tmax)

                        if (adamic_linear1 == 0):
                            adamic_linear1 = math.e - 1
                        if (adamic_square1 == 0):
                            adamic_square1 = math.e - 1
                        if (adamic_exp1 == 0):
                            adamic_exp1 = math.e - 1

                        adamic_linear = (weighted_topological_features_linear(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)) / math.log(1 + adamic_linear1)
                        adamic_square = (weighted_topological_features_square(graph, i, k, tmin, tmax) + weighted_topological_features_square(graph, j, k, tmin, tmax)) / math.log(1 + adamic_square1)
                        adamic_exp = (weighted_topological_features_exp(graph, i, k, tmin, tmax) + weighted_topological_features_exp(graph, j, k, tmin, tmax)) / math.log(1 + adamic_exp1)

                        jaccard_linear = (weighted_topological_features_linear(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)) / (jaccard_linear1 + jaccard_linear2)
                        jaccard_square = (weighted_topological_features_square(graph, i, k, tmin, tmax) + weighted_topological_features_square(graph, j, k, tmin, tmax)) / (jaccard_square1 + jaccard_square2)
                        jaccard_exp = (weighted_topological_features_exp(graph, i, k, tmin, tmax) + weighted_topological_features_exp(graph, j, k, tmin, tmax)) / (jaccard_exp1 + jaccard_exp2)

                        preferential_linear = jaccard_linear1 * jaccard_linear2
                        preferential_square = jaccard_square1 * jaccard_square2
                        preferential_exp = jaccard_exp1 * jaccard_exp2

                if  (j in graph[i]['neigh']):
                    if (pos_counter < max):
                        new_row = pd.DataFrame({'def': [1], 'u': [i], 'v': [j],
                                        'cnwl': [common_neigh_linear], 'aawl': [adamic_linear], 'jcwl': [jaccard_linear], 'pawl': [preferential_linear],
                                        'cnws': [common_neigh_square], 'aaws': [adamic_square], 'jcws': [jaccard_square], 'paws': [preferential_square],
                                        'cnwe': [common_neigh_exp], 'aawe': [adamic_exp], 'jcwe': [jaccard_exp], 'pawe': [preferential_exp], 'time': [graph[j]['time'][graph[j]['neigh'].index(i)]]})
                        df = pd.concat([df, new_row], ignore_index=True)
                        pos_counter = pos_counter +1
                        print(f"pos: {pos_counter} neg: {neg_counter}")
                    
                else:
                    if (neg_counter < max):
                        new_row = pd.DataFrame({'def': [0], 'u': [i], 'v': [j],
                                                'cnwl': [common_neigh_linear], 'aawl': [adamic_linear], 'jcwl': [jaccard_linear], 'pawl': [preferential_linear],
                                                'cnws': [common_neigh_square], 'aaws': [adamic_square], 'jcws': [jaccard_square], 'paws': [preferential_square],
                                                'cnwe': [common_neigh_exp], 'aawe': [adamic_exp], 'jcwe': [jaccard_exp], 'pawe': [preferential_exp], 'time': [0]})

                        df = pd.concat([df, new_row], ignore_index=True)
                        neg_counter = neg_counter + 1
                        print(f"pos: {pos_counter} neg: {neg_counter}")
                
        print('Вычисление темпоральных признаков закончено')
        current_graph.temporal_features = df






def read_edge_for_bin(filename):
    f = open(filename)
    f.readline()
    graph = {}
    count_node = 0
    count_edge = 0
    edge = f.readline().split()
    tmax = 1000000000000
    tmin = 0

    while edge:
        if len(edge) != 1:
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            edge[3] = int(edge[3])
            count_edge += 1

            if tmin > edge[3]:
                tmin = edge[3]
            elif tmax < edge[3]:
                tmax = edge[3]

            if edge[0] in graph:
                if edge[0] == edge[1]:
                    graph[edge[0]]['neigh'].append(edge[1])
                    graph[edge[0]]['time'].append(edge[3])
                    graph[edge[0]]['degree'] += 2
                elif edge[1] not in graph[edge[0]]['neigh']:
                    graph[edge[0]]['neigh'].append(edge[1])
                    graph[edge[0]]['time'].append(edge[3])
                    graph[edge[0]]['degree'] += 1
            else:
                if edge[0] != edge[1]:
                    graph[edge[0]] = {'neigh': [edge[1]], 'degree': 1, 'component': '', 'marker': False,
                                    'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0, 'time': [edge[3]]}
                    count_node += 1
                else:
                    graph[edge[0]] = {'neigh': [edge[0]], 'degree': 2, 'component': '', 'marker': False, 'color': 'white',
                                    'dist': 0, 'Lv': 0, 'cl': 0, 'time': [edge[3]]}
                    count_node += 1

            if edge[1] in graph:
                if edge[0] not in graph[edge[1]]['neigh'] and edge[0] != edge[1]:
                    graph[edge[1]]['neigh'].append(edge[0])
                    graph[edge[1]]['time'].append(edge[3])
                    graph[edge[1]]['degree'] += 1
            else:
                graph[edge[1]] = {'neigh': [edge[0]], 'degree': 1, 'component': '', 'marker': False, 'color': 'white',
                                'dist': 0, 'Lv': 0, 'cl': 0, 'time': [edge[3]]}
                count_node += 1

        edge = f.readline().split()
    f.close()
    return graph, count_node, count_edge, tmin, tmax


def weighted_topological_features_linear(graph, a, b, tmin, tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    #l = 0.2
    l = 1
    return l + (1 - l) * (t - tmin) / (tmax - tmin)

def weighted_topological_features_exp(graph, a, b, tmin, tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    l = 1
    return l + (1 - l) * (math.exp(3 * (t - tmin) / (tmax - tmin)) - 1) / (math.e ** 3 - 1)

def weighted_topological_features_square(graph, a, b, tmin, tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    l = 1
    return l + (1 - l) * (math.sqrt((t - tmin) / (tmax - tmin)))