import pandas as pd
import numpy as np
data = pd.read_csv('4.tsv', sep = "\t", header= None, names=['in','out','weight','time'])
dvudol = True
#Вывести количество ребер
print('Количество ребер в графе: ' + str(data.shape[0]))

#Вывести количество вершин и разбить по долям, сохранив в виде списков смежности
if dvudol:
    LeftVertex = {}
    RightVertex = {}
    for index, row in data.iterrows():
        left = LeftVertex.get(row['in'])
        if left:
            if (str(row['out']) + 'r') in left:
                continue
            else:
                left.append((str(row['out']) + 'r'))
                LeftVertex[row['in']] = left
        else:
            LeftVertex[row['in']] = [(str(row['out']) + 'r')]

        right = RightVertex.get((str(row['out']) + 'r'))
        if right:
            if row['in'] in right:
                continue
            else:
                right.append(row['in'])
                RightVertex[(str(row['out']) + 'r')] = right
        else:
            RightVertex[(str(row['out']) + 'r')] = [row['in']]
    AllVertex = LeftVertex | RightVertex
    countVertex = len(AllVertex)
else:
    pass

print('Количество вершин в графе: ' + str(countVertex))

#Считаем плотность графа
print("Плотность графа: " + str(data.shape[0]/(len(RightVertex)*len(LeftVertex))))

#Считаем количество Компонент слабой связности

def DFS_for_weak_component(vertex, part, component):
    visited.add(vertex)
    component.append(vertex)
    if part:
        neighs = LeftVertex.get(vertex)
    else:
        neighs = RightVertex.get(vertex)
    for neigh in neighs:
        if neigh in visited:
            continue
        elif part:
            DFS_for_weak_component(neigh, False, component)
        else:
            DFS_for_weak_component(neigh, True, component)

visited = set([])
components = []
for vertex in LeftVertex.items():
    if len(visited) == countVertex:
        break
    if vertex[0] in visited:
        continue
    component = []
    DFS_for_weak_component(vertex[0], True, component)
    components.append(component)
print('Количество компонент слабой связности: ' + str(len(components)))

#Ищем долю вершин в максимальной по мощности компоненте слабой связности
print('Доля вершин в максимальной по мощности компоненте слабой связности: ' + \
str(len(max(components, key=len))/countVertex))

#Ищем радиус и диаметр
import random
from collections import deque
max_component = max(components, key=len)
def BFS_for_snow_subgraph(vertex):
    subgraph = []
    queue = deque()
    queue.extend(vertex)
    visited=set([])
    while len(queue)>0 and len(subgraph)<750:
        actual = queue.popleft()
        subgraph.append(actual)
        neighs = []
        if str(actual)[-1]!='r':
            neighs = LeftVertex.get(actual)
        else:
            neighs = RightVertex.get(actual)
        for neigh in neighs:
            if neigh not in visited:
                queue.append(neigh)
    return subgraph

def simple_search(max_component):
    matrix = [[float('inf')]*len(max_component) for i in range(len(max_component))]
    order_in_max_component = {}
    for i in range(len(max_component)):
        vertex = max_component[i]
        order_in_max_component[vertex] = i
    for i in range(len(max_component)):
        vertex = max_component[i]
        if str(vertex)[-1]!='r':
            neighs = LeftVertex.get(vertex)
        else:
            neighs = RightVertex.get(vertex)
        for neigh in neighs:
            j = order_in_max_component.get(neigh)
            if j is not None:
                matrix[i][j] = 1
    for k in range(len(max_component)):
        for i in range(len(max_component)):
            for j in range(len(max_component)):
                matrix[i][j] = min(matrix[i][j], matrix[i][k]+matrix[k][j])
    radius = float('inf')
    diam = 0
    dist = []
    for row in matrix:
        max_row = -1
        for item in row:
            if item != float('inf'):
                dist.append(item)
                if item>max_row:
                    max_row = item
        if max_row!= -1:
            radius = min(max_row, radius)
            diam = max(max_row, diam)
    print('Диаметр графа: ' + str(diam))
    print('Радиус графа: ' + str(radius))
    print('90 процентиль расстояния в графе: ' + str(np.percentile(dist,90)))

if len(max_component)>750:
    new_random_component = []
    for _ in range(750):
        new_random_component.append(random.choice(max_component))
    new_snow_component = BFS_for_snow_subgraph([random.choice(max_component) for _ in range(3)])
    print('Метрики расстояний на случайном подграфе: ')
    simple_search(new_random_component)
    print('Метрики расстояний на подграфе методом снежный ком:  ')
    simple_search(new_snow_component)
else:
    simple_search(max_component)

#Вычисляем средний кластерный коэффициент:








