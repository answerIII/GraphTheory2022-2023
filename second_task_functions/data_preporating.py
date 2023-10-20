import pandas as pd
from collections import defaultdict
import csv


def read_graph_edges_from_csv(filename):
    edges = []
    with open(filename, 'r') as csvfile:
          csvreader = csv.DictReader(csvfile, delimiter='\t')
          for row in csvreader:
              in_node = int(row['in'])
              out_node = int(row['out'])
              weight = int(row['weight'])
              time = int(row['time'])
              edges.append((in_node, out_node, weight, time))
    return edges

def write_results_to_csv(results, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Node1', 'Node2', 'Common Neighbours', 'Adamic-Adar', 'Jaccard Coefficient', 'Preferential Attachment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

def read_edge_features_from_csv(filename):
    edge_features = {}
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            node1 = int(row['Node1'])
            node2 = int(row['Node2'])
            features = [
                float(row['Common Neighbours']),
                float(row['Adamic-Adar']),
                float(row['Jaccard Coefficient']),
                float(row['Preferential Attachment'])
            ]
            edge_features[(node1, node2)] = features
    return edge_features


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