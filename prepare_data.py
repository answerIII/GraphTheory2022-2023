import numpy as np 
import queue
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict

def number_of_vertexes(dataset):
    uniqueVertexes = set()
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        uniqueVertexes.add(from_ind)
        uniqueVertexes.add(to_ind)

    # return len(uniqueVertexes) + 1
    return max(uniqueVertexes) + 1

def get_edgeList(dataset):
     edgeList = []
     for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        # print([from_ind, to_ind, time])
        edgeList.append([from_ind, to_ind, time])
        edgeList.append([to_ind, from_ind, time])
     return edgeList

def draw_graph(dataset, qs):
    G = nx.Graph()
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        G.add_edge(from_ind, to_ind, weight=time)
    
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > qs]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= qs]

    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(
        G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed"
    )

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def prepare_data_at_dist_2(dataset, s = 75, display_interm_results = False):
    
    def dijkstra_algo(adjList: list[list], start) -> list:
        min_queue = queue.PriorityQueue()
        distance = [np.inf] * V

        min_queue.put((0, start))
        distance[start] = 0
        
        while not min_queue.empty():
            u = min_queue.get()[1]
            for v in adjList[u]:
                weight = 1

                if distance[v] > distance[u] + weight and distance[u] < 2:
                    distance[v] = distance[u] + weight
                    min_queue.put((distance[v], v))


        pairs_of_vertexes = [] # at distance = 2
        for i in range(start, V):
            if distance[i] == 2:
                pairs_of_vertexes.append((start, i))

            # print(i, ":", distance[i])

        # print(pairs_of_vertexes)
        # print()


        return pairs_of_vertexes
    
    
    V = number_of_vertexes(dataset)
    edgeList = get_edgeList(dataset)

    time_list = [edge[2] for edge in edgeList]
    qs = np.percentile(time_list, s) # qs - s-й процентиль списка timestamp'ов
    t_min = min(time_list)
    t_max = max(time_list)
    if display_interm_results: print("time_list:", time_list)
    print("t_min:", t_min)
    print("t_max:", t_max)
    print("qs:", qs)
    

    adjList = defaultdict(list)
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        if time <= qs:
            adjList[from_ind].append(to_ind)
            adjList[to_ind].append(from_ind)

    # delete duplicate edges
    for i in range(V):
        _set = set(adjList[i])
        adjList[i] = list(_set)


    edgeL_till_qs = set()
    edgeL_after_qs = set()
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        if time <= qs: 
            edgeL_till_qs.add((min(from_ind, to_ind), max(from_ind, to_ind)))
        else:
            edgeL_after_qs.add((min(from_ind, to_ind), max(from_ind, to_ind)))


    if display_interm_results: print("edgeL_till_qs:", edgeL_till_qs)
    print("size of edgeL_till_qs:", len(edgeL_till_qs), end='\n\n')

    if display_interm_results: print("edgeL_after_qs:", edgeL_after_qs)
    print("size of edgeL_after_qs:", len(edgeL_after_qs), end='\n\n')


    # Выборка пар вершин, расстояние между которыми равно 2
    # без симметричных ребер, так как граф неориентированный и статические метрики симметричные
    pairs_at_dist_2 = []
    for i in range(1, V):
        pairs_at_dist_2 += dijkstra_algo(adjList, i)

    pairs_at_dist_2 = set(pairs_at_dist_2)
    if display_interm_results: print("pairs_at_dist_2:", pairs_at_dist_2)
    print("size of pairs_at_dist_2:", len(pairs_at_dist_2), end='\n\n')


    positives = []
    negatives = []
    for pair in pairs_at_dist_2:
        if pair in edgeL_after_qs:
            positives.append(pair)
        else:
            negatives.append(pair)

    sample_size = 10000

    pos_sample = random.choices(positives, k = sample_size)
    neg_sample = random.choices(negatives, k = sample_size)

    print("size of pos_sample:", len(pos_sample), end='\n\n')
    print("size of neg_sample:", len(neg_sample), end='\n\n')

    nonexistent_edges = list(pos_sample)
    nonexistent_edges.extend(neg_sample)
    y = [1]*sample_size
    y.extend([0]*sample_size)

    print("size of y:", len(y), end='\n\n')
    


    return [V, qs, adjList, nonexistent_edges, y]





