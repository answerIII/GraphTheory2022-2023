import pandas as pd
import math
import random
import numpy as np
from collections import deque
import collections

#Получить список смежности для всего графа за все время для тестовых графов
def get_adjacency_list_test(data):
    adjacency_list = dict({})
    count_edges = 0
    edges_r = set()
    is_loop = False
    for row in data.itertuples():
        # Список смежности для все ребер за все время
        count_add = 0
        if (row[1] in adjacency_list):
            if (row[2] not in adjacency_list[row[1]]):
                adjacency_list[row[1]].append(row[2])
                count_add += 1
        else:
            adjacency_list[row[1]] = [row[2]]
            count_add += 1
        if (row[2] in adjacency_list):
            if (row[1] not in adjacency_list[row[2]]):
                adjacency_list[row[2]].append(row[1])
                count_add += 1
        else:
            adjacency_list[row[2]] = [row[1]]
            count_add += 1

        if count_add >= 1:
            if count_add == 1:
                is_loop = True
            count_edges += 1
        edges_r.add((min(row[1], row[2]), max(row[1], row[2])))

    return [adjacency_list, count_edges, is_loop, edges_r]

#Получить список смежности для всего графа за все время
def get_adjacency_list(data):
    adjacency_list = dict({})
    edges_r = dict({})
    time = []
    count_edges = 0
    is_loop = False
    for row in data.itertuples():
        # Список смежности для все ребер за все время
        count_add = 0
        if (row[1] in adjacency_list):
            if (row[2] not in adjacency_list[row[1]]):
                adjacency_list[row[1]].append(row[2])
                count_add += 1
        else:
            adjacency_list[row[1]] = [row[2]]
            count_add += 1
        if (row[2] in adjacency_list):
            if (row[1] not in adjacency_list[row[2]]):
                adjacency_list[row[2]].append(row[1])
                count_add += 1
        else:
            adjacency_list[row[2]] = [row[1]]
            count_add += 1

        if count_add >= 1:
            if count_add == 1:
                is_loop = True
            count_edges += 1

        # Заносим все ребра
        if (row[1] < row[2]):
            fir = row[1]
            sec = row[2]
        else:
            fir = row[2]
            sec = row[1]
        if (fir, sec) in edges_r:
            edges_r[(fir, sec)].append(row[4])
        else:
            edges_r[(fir, sec)] = [row[4]]

        time.append(row[4])
    return [adjacency_list, min(time), max(time), edges_r, count_edges, is_loop]


#Получить список смежности для графа до момента s
def get_adjacency_list_until_s(data, s):
    adjacency_list_until_s = dict({})
    edges_r_until_s = dict({})
    time = []
    for row in data.itertuples():
        # Список смежности до момента s
        if row[4] <= s:
            if (row[1] in adjacency_list_until_s):
                if (row[2] not in adjacency_list_until_s[row[1]]):
                    adjacency_list_until_s[row[1]].append(row[2])
            else:
                adjacency_list_until_s[row[1]] = [row[2]]
            if (row[2] in adjacency_list_until_s):
                if (row[1] not in adjacency_list_until_s[row[2]]):
                    adjacency_list_until_s[row[2]].append(row[1])
            else:
                adjacency_list_until_s[row[2]] = [row[1]]

            # Заносим все ребра до s
            if (row[1] < row[2]):
                fir = row[1]
                sec = row[2]
            else:
                fir = row[2]
                sec = row[1]
            if (fir, sec) in edges_r_until_s:
                edges_r_until_s[(fir, sec)].append(row[4])
            else:
                edges_r_until_s[(fir, sec)] = [row[4]]

            time.append(row[4])

    return adjacency_list_until_s, edges_r_until_s, min(time), max(time)


def floyd_warshall(adjacency_list):
    d = [[[] for _ in range(len(adjacency_list))] for __ in range(len(adjacency_list))]
    for node_1 in adjacency_list:
        for node_2 in adjacency_list:
            d[list(adjacency_list).index(node_1)][list(adjacency_list).index(node_2)] = [math.inf, min(node_1, node_2),
                                                                                         max(node_1, node_2)]

    for node in adjacency_list:
        for neighbour in adjacency_list[node]:
            d[list(adjacency_list).index(node)][list(adjacency_list).index(neighbour)][0] = 1

    for i in range(len(d)):
        d_i = [d[j][:] for j in range(len(d))]
        for u in range(len(d)):
            for v in range(len(d)):
                d[u][v][0] = min(d_i[u][v][0], d_i[u][i][0] + d_i[i][v][0])

    for i in range(len(d)):
        d[i][i][0] = 0
    return d

def BFS(node, adjacency_list):
    visited = set()
    queue = deque()
    queue.append(node)
    visited.add(node)
    dist = 1
    while len(queue) > 0 and dist < 3:
        size = len(queue)
        while size > 0:
            cur = queue.popleft()
            size -= 1
            for neighbour in adjacency_list[cur]:
                if (neighbour not in visited):
                    queue.append(neighbour)
                    visited.add(neighbour)
        dist += 1
    return list(queue)


def get_info_dataset(data, q):
    adjacency_list, tmin, tmax, edges_r, count_edges, is_loop = get_adjacency_list(data)
    nodesNumber = len(adjacency_list)
    print(nodesNumber)

    s = (tmax + tmin) * q
    print('tmin: ' + str(tmin))
    print('tmax: ' + str(tmax))
    print('ts: ' + str(s))

    #Нужные данные до момента s
    adjacency_list_until_s, edges_r_until_s, tmin, tmax = get_adjacency_list_until_s(data, s)

    number1 = 0
    number0 = 0
    edges_p = []
    edges_n = []

    for i in range(1, nodesNumber + 1):
        for j in range(i, nodesNumber + 1):
            if (j in adjacency_list[i]):
                if (min(edges_r[(i, j)]) >= s):
                    edges_p.append((i, j))
            else:
                edges_n.append((i, j))
            if (len(edges_p) > 30000) and (len(edges_n) > 30000):
                break
        if (len(edges_p) > 30000) and (len(edges_n) > 30000):
            break

    # all_possible_edges = []
    #
    # for i in range(1, nodesNumber + 1):
    #     for j in range(i, nodesNumber + 1):
    #         all_possible_edges.append((i, j))

    # for edge in all_possible_edges:
    #     if (edge not in edges_r):
    #         edges_n.append(edge)
    #         number0 += 1
    #     elif (min(edges_r[edge]) > s):
    #         edges_p.append(edge)
    #         number1 += 1

    edges_p_copy = edges_p.copy()
    edges_n_copy = edges_n.copy()

    print('Посчитал edges_p и edges_n')
    print('edges_p: ' + str(len(edges_p)))
    print('edges_n: ' + str(len(edges_n)))

    #Считаем для 4.1.1

    #Ищем все пары вершин, между которыми расстояние 2
    pair_dist_2 = []
    for node in adjacency_list_until_s:
        nodes_dist_2 = BFS(node, adjacency_list_until_s)
        for node_2 in nodes_dist_2:
            pair_dist_2.append((min(node, node_2), max(node, node_2)))

    edges_p = list(set(pair_dist_2) & set(edges_p))
    edges_n = list(set(pair_dist_2) & set(edges_n))
    number1 = len(edges_p)
    number0 = len(edges_n)

    #Вариант через Флойда-Воршалла
    # d = floyd_warshall(adjacency_list_until_s)
    #
    # seen_edges = []
    # for i in range(0, len(d)):
    #     for j in range(i, len(d)):
    #         if ((min(d[i][j][1], d[i][j][2]), max(d[i][j][1], d[i][j][2])) in edges_p):
    #             seen_edges.append((min(d[i][j][1], d[i][j][2]), max(d[i][j][1], d[i][j][2])))
    #             if (d[i][j][0] != 2):
    #                 edges_p.remove((min(d[i][j][1], d[i][j][2]), max(d[i][j][1], d[i][j][2])))
    #                 number1 -= 1
    #
    # edges_p = [edge for edge in edges_p if edge in seen_edges]
    #
    # seen_edges = []
    #
    # for i in range(0, len(d)):
    #     for j in range(i, len(d)):
    #         if ((min(d[i][j][1], d[i][j][2]), max(d[i][j][1], d[i][j][2])) in edges_n):
    #             seen_edges.append((min(d[i][j][1], d[i][j][2]), max(d[i][j][1], d[i][j][2])))
    #             if (d[i][j][0] != 2):
    #                 edges_n.remove((min(d[i][j][1], d[i][j][2]), max(d[i][j][1], d[i][j][2])))
    #                 number0 -= 1
    #
    # edges_n = [edge for edge in edges_n if edge in seen_edges]

    #Ограничения на количество предсказываемых ребер
    if (number1 >= 10000):
        edges_p = random.sample(edges_p, 10000)
    if (number0 >= 10000):
        edges_n = random.sample(edges_n, 10000)

    if (len(edges_p) > 4 * len(edges_n)):
        edges_p = random.sample(edges_p, 4 * len(edges_n))
    elif (len(edges_p) * 4 < len(edges_n)):
        edges_n = random.sample(edges_n, 4 * len(edges_p))

    print('Посчитал все для 4.1.1')
    print('edges_p: ' + str(len(edges_p)))
    print('edges_n: ' + str(len(edges_n)))
    # Считаем для 4.1.2
    temp = tmin
    tmin = tmax
    tmax = temp

    edges_r_until_s_multi = edges_r_until_s.copy()

    #Ищем все ребра, у которых несколько временных отметок
    for edge in edges_r_until_s:
        edges_r_until_s_multi[edge] = list(set(edges_r_until_s[edge]))
        if len(edges_r_until_s_multi[edge]) < 2:
            edges_r_until_s_multi.pop(edge)
        else:
            for time in edges_r_until_s_multi[edge]:
                if time > tmax:
                    tmax = time
                if time < tmin:
                    tmin = time

    #Создаем новый список смежности из полученных ребер
    adjacency_list_until_s_multi = adjacency_list_until_s.copy()
    for node in adjacency_list_until_s_multi:
        new_neighs = []
        for neigh in adjacency_list_until_s_multi[node]:
            if (node, neigh) in edges_r_until_s_multi or (neigh, node) in edges_r_until_s_multi:
                new_neighs.append(neigh)
        adjacency_list_until_s_multi[node] = new_neighs

    #Ищем пары вершин, между которыми расстояние 2 в новом списке смежности
    pair_dist_2_multi = []
    for node in adjacency_list_until_s_multi:
        nodes_dist_2 = BFS(node, adjacency_list_until_s_multi)
        for node_2 in nodes_dist_2:
            pair_dist_2_multi.append((min(node, node_2), max(node, node_2)))

    edges_p_multi = list(set(pair_dist_2_multi) & set(edges_p_copy))
    edges_n_multi = list(set(pair_dist_2_multi) & set(edges_n_copy))
    number1_multi = len(edges_p_multi)
    number0_multi = len(edges_n_multi)

    # Ограничения на количество предсказываемых ребер
    if (number1_multi >= 10000):
        edges_p_multi = random.sample(edges_p_multi, 10000)
    if (number0_multi >= 10000):
        edges_n_multi = random.sample(edges_n_multi, 10000)

    if (len(edges_p_multi) > len(edges_n_multi)):
        edges_p_multi = random.sample(edges_p_multi, len(edges_n_multi))
    elif (len(edges_p_multi) < len(edges_n_multi)):
        edges_n_multi = random.sample(edges_n_multi, len(edges_p_multi))

    print('Посчитал все для 4.1.2')
    print('edges_p_multi: ' + str(len(edges_p_multi)))
    print('edges_n_multi: ' + str(len(edges_n_multi)))

    return adjacency_list, adjacency_list_until_s, adjacency_list_until_s_multi, edges_r, edges_r_until_s, \
           edges_r_until_s_multi, edges_p, edges_n, edges_p_multi, edges_n_multi, tmin, tmax, count_edges, is_loop