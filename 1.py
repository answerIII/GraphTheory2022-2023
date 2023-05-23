import pandas as pd
import math
import random
import numpy as np
from collections import deque

# dataset_path = 'datasets/' + 'out.radoslaw_email_email' + '.txt'
dataset_path = 'datasets/' + 'out.prosper-loans' + '.txt'
data = pd.read_csv(dataset_path, sep='\s+', names=['id_from', 'id_to', 'weight', 'time'], header=None)

def get_adjacency_list(data):
    adjacency_list = dict({})
    count_edges = 0
    is_loop = False
    for row in data.itertuples():
        count_add = 0
        if(row[1] in adjacency_list):
            if(row[2] not in adjacency_list[row[1]]):
                adjacency_list[row[1]].append(row[2])
                count_add += 1
        else:
            adjacency_list[row[1]] = [row[2]]
            count_add += 1
        if(row[2] in adjacency_list):
            if(row[1] not in adjacency_list[row[2]]):
                adjacency_list[row[2]].append(row[1])
                count_add += 1
        else:
            adjacency_list[row[2]] = [row[1]]
            count_add += 1
        if count_add >= 1:
          if count_add == 1:
              is_loop = True
          count_edges += 1
    return [adjacency_list, count_edges, is_loop]

#количество вершин
def nodes_number(data, adjacency_list):
    # adjacency_list = get_adjacency_list(data)[0]
    return len(adjacency_list)

#количество ребер
def edges_number(data, count_edges):
    return count_edges

#плотность графа
def graph_density(data, edges_num, nodes_num, is_loop):
    if is_loop:
        return edges_num / (nodes_num * (nodes_num + 1) / 2)
    else:
        return edges_num / (nodes_num * (nodes_num - 1) / 2)

#получить все компоненты слабой связности
def get_components(data, adjacency_list):
    def DFS(node, component):
        visited.add(node)
        component.append(node)
        for neighbour in adjacency_list[node]:
            if neighbour not in visited:
                DFS(neighbour, component)

    def BFS(node, component):
        queue = deque()
        queue.append(node)
        visited.add(node)
        while len(queue) > 0:
            cur = queue.popleft()
            component.append(cur)
            for neighbour in adjacency_list[cur]:
                if (neighbour not in visited):
                    queue.append(neighbour)
                    visited.add(neighbour)

    visited = set()
    components = dict({})
    count = 0
    for node in adjacency_list:
        if node not in visited:
            count += 1
            component = []
            # DFS(node, component)
            BFS(node, component)
            components[count] = component
    return components

#получить количество компонент слабой связности
def components_number(data, adjacency_list):
    return(len(get_components(data, adjacency_list)))

#получить максимальную по мощности компоненту и долю вершин в максимальной по мощности компоненте слабой связности
def max_component(data, adjacency_list):
    components = get_components(data, adjacency_list)
    max_key = max(components, key = lambda x: len(components[x]))
    return [components[max_key],len(components[max_key])/nodes_number(data, adjacency_list)]

# получить матрицу расстояний между всеми вершинами макс компоненты(или сэмпла из макс компоненты)
def floyd_warshall(adjacency_list, max_comp):
    d = [[math.inf for _ in range(len(max_comp))] for __ in range(len(max_comp))]
    for node in max_comp:
        for neighbour in adjacency_list[node]:
            if neighbour in max_comp:
                d[max_comp.index(node)][max_comp.index(neighbour)] = 1

    for i in range(len(max_comp)):
        d_i = [d[j][:] for j in range(len(max_comp))]
        for u in range(len(max_comp)):
            for v in range(len(max_comp)):
                d[u][v] = min(d_i[u][v], d_i[u][i] + d_i[i][v])

    for i in range(len(max_comp)):
        d[i][i] = 0
    return d

# сэмплирование методом снежный ком
def BFS(adjacency_list, nodes):
    visited = set(nodes)
    sample = []
    queue = deque()
    queue.extend(nodes)

    while (len(sample) < 500 and len(queue) > 0):
        cur = queue.popleft()
        sample.append(cur)
        for neighbour in adjacency_list[cur]:
            if (neighbour not in visited):
                queue.append(neighbour)
                visited.add(neighbour)

    return sample

#диаметр, радиус, 90 персентиль для рандомного семплирования макс компоненты
def random_sample_metrics(data, adjacency_list, max_comp):
    # adjacency_list = get_adjacency_list(data)[0]
    # max_comp = max_component(data)[0]
    if len(max_comp) > 500:
        random_sample = random.sample(max_comp, 500)
    else:
        random_sample = max_comp
    d = floyd_warshall(adjacency_list, random_sample)
    dist_list = []
    diam = -1
    rad = math.inf
    for i in d:
        row_max = -1
        for j in i:
            if j!=math.inf:
                dist_list.append(j)
                if j>row_max:
                    row_max = j
        if row_max != -1:
            diam = max(row_max, diam)
            rad = min(row_max, rad)
    return [diam, rad, np.percentile(dist_list,90)]

# диаметр, радиус, 90 персентиль для семплирования методом snowball макс компоненты
def snowball_sample(data, adjacency_list, max_comp):
    # adjacency_list = get_adjacency_list(data)[0]
    # max_comp = max_component(data)[0]
    if len(max_comp) > 500:
        sample = BFS(adjacency_list, random.sample(max_comp, 2))
    else:
        sample = max_comp

    d = floyd_warshall(adjacency_list, sample)
    dist_list = []
    diam = -1
    rad = math.inf
    for i in d:
        row_max = -1
        for j in i:
            if j != math.inf:
                dist_list.append(j)
                if j > row_max:
                    row_max = j
        if row_max != -1:
            diam = max(row_max, diam)
            rad = min(row_max, rad)
    return [diam, rad, np.percentile(dist_list, 90)]

# Для наибольшей компоненты слабой связности вычислить средний кластерный коэффициент сети
def CL(data, adjacency_list, max_comp):
    # adjacency_list = get_adjacency_list(data)[0]
    # max_comp = max_component(data)[0]
    cl = 0
    for node in max_comp:
        CLu = 0
        loop_edges = 0
        if (len(adjacency_list[node]) >= 2):
            for node2 in adjacency_list[node]:
                for node3 in adjacency_list[node2]:
                    if node3 in adjacency_list[node]:
                        if node3 == node2:
                            loop_edges += 1
                        else:
                            CLu += 1
            cl += (CLu + 2 * loop_edges) / (len(adjacency_list[node]) * (len(adjacency_list[node]) - 1))

    return cl / (len(max_comp))

#расчёт корреляции
def r_pearson(data, adjacency_list):
    # adjacency_list = get_adjacency_list(data)[0]
    X = []
    Y = []
    visited = set()
    for vertex_1 in adjacency_list:
        for vertex_2 in adjacency_list[vertex_1]:
            if ((vertex_2, vertex_1) not in visited) and ((vertex_1,vertex_2) not in visited):
                X.append(len(adjacency_list[vertex_1]))
                Y.append(len(adjacency_list[vertex_2]))
                visited.add((vertex_1, vertex_2))

    Avg_X = sum(X) / len(X)
    Avg_Y = sum(Y) / len(Y)

    deltaX = [x - Avg_X for x in X]
    deltaY = [y - Avg_Y for y in Y]

    numerator = sum([delta_x * delta_y for delta_x, delta_y in zip(deltaX, deltaY)])
    denominator = (sum([delta_x * delta_x for delta_x in deltaX]) * sum([delta_y * delta_y for delta_y in deltaY])) ** 0.5
    if denominator == 0:
        return 0
    else:
        return numerator / denominator

adjacency_list, count_edges, is_loop = get_adjacency_list(data)
nodes_num = nodes_number(data, adjacency_list)
edges_num = edges_number(data, count_edges)
print('Кол-во вершин: ' + str(nodes_num))
print('Кол-во ребер: ' + str(edges_num))
print('Плотность: '+ str(graph_density(data, edges_num, nodes_num, is_loop)))
print('Кол-во слабых компонент: ' + str(components_number(data, adjacency_list)))
max_comp = max_component(data, adjacency_list)[0]
print('Мощность максимальной слабой компоненты: ' + str(len(max_comp)))

diam_1, rad_1, percent_1 = random_sample_metrics(data, adjacency_list, max_comp)
print('Диаметр: ' + str(diam_1))
print('Радиус: ' + str(rad_1))
diam_2, rad_2, percent_2 = snowball_sample(data, adjacency_list, max_comp)
print('Диаметр: ' + str(diam_2))
print('Радиус: ' + str(rad_2))
# print('Average clustering coefficient: ' + str(CL(data, adjacency_list, max_comp)))
print('Коэффициент Пирсона: ' + str(r_pearson(data, adjacency_list)))