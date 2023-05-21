import networkx as nx
import math
from sklearn.linear_model import LogisticRegression
import numpy as np
import pylab
import queue


#f = open('datasets\out.radoslaw_email_email', 'r')
#f = open('datasets\out.opsahl-ucsocial', 'r') 
#f = open('datasets\out.soc-sign-bitcoinalpha.txt', 'r')
#f = open('datasets\out.munmun_digg_reply', 'r')
#f = open('datasets\out.sx-mathoverflow', 'r')
#f = open('datasets\out.prosper-loans.txt', 'r')
#f = open('datasets\small-graph.txt', 'r') 
f = open('datasets\\assortativity-example.txt', 'r') 

dataset = f.readlines()

# count number of vertexes
uniqueVertexes = set()
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    uniqueVertexes.add(from_ind)
    uniqueVertexes.add(to_ind)

V = len(uniqueVertexes) + 1
adjList = [[] for _ in range(V)]

# transform directed graph to undirected
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    adjList[from_ind].append([to_ind, 1, 1])
    adjList[to_ind].append([from_ind, 1, 1])

# delete duplicate edges
for i in range(V):
    set_tuples = {tuple(a_list) for a_list in adjList[i]}
    adjList[i] = list(set_tuples)



### 2.1. Посчитать 4 статических топологических свойства


def Common_Neighbours(adjList, edge):
    src_v = edge[0]
    dst_v = edge[1]

    # print(adjList[src_v])
    # print(adjList[dst_v])

    intersection = list(set(adjList[src_v]) & set(adjList[dst_v]))

    return len(intersection)


def Adamic_Adar(adjList, edge):
    src_v = edge[0]
    dst_v = edge[1]

    intersection = list(set(adjList[src_v]) & set(adjList[dst_v]))
    
    sum = 0
    for node in intersection:
        to = node[0] # node - это tuple(to, weight, time)
        size = len(adjList[to]) # количество вершин, смежных вершине to
        sum += 1 / (math.log(size, 2))

    return sum


def Jaccard_Coef(adjList, edge):
    src_v = edge[0]
    dst_v = edge[1]

    intersection = list(set(adjList[src_v]) & set(adjList[dst_v]))
    union = list(set(adjList[src_v]) | set(adjList[dst_v]))

    result = len(intersection) / len(union)
  
    return result


def Preferential_Attachment(adjList, edge):
    u = edge[0]
    v = edge[1]

    degree_u = len(adjList[u])
    degree_v = len(adjList[v])

    result = degree_u * degree_v
  
    return result

print("for edge:", (3, 1))
print("CN:" , Common_Neighbours(adjList, (3, 1)))
print("AA:" ,Adamic_Adar(adjList, (3, 1)))
print("JC:" ,Jaccard_Coef(adjList, (3, 1)))
print("PA:" ,Preferential_Attachment(adjList, (3, 1)))


### 


# adj matrix (используется для преобразования в nx.Graph и отрисовки)
a = np.full((V, V), 0)
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    a[from_ind][to_ind] = 1
    a[to_ind][from_ind] = 1  

G = nx.from_numpy_array(a)
nx.draw_networkx(G)


def dijkstra_algo(adjList, start) -> list:
    min_queue = queue.PriorityQueue()
    distance = [np.inf] * V

    min_queue.put((0, start))
    distance[start] = 0
    
    while not min_queue.empty():
        u = min_queue.get()[1]
        for node in adjList[u]:
            v = node[0]
            weight = 1

            if distance[v] > distance[u] + weight:
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


# Выборка пар вершин, расстояние между которыми равно 2 (то есть минимальное расстояние равно 2)
# без симметричных ребер, так как граф неориентированный и статические метрики симметричные (то есть для ребер (u,v) и (v,u) значения метрик равны)
pairs_of_vertexes = []
for i in range(1, V):
    pairs_of_vertexes += dijkstra_algo(adjList, i)

print("pairs_of_vertexes:", pairs_of_vertexes)

print("size of pairs_of_vertexes:", len(pairs_of_vertexes))

pylab.show()
f.close()