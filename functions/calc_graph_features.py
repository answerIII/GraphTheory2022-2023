import pandas as pd
import numpy as np
import sys
import random
from collections import deque

def calc_static_features(file):
    file_path = 'datasets/' + file + '.csv'
    data = pd.read_csv(file_path, sep="\t")
    dvudol = False
    if file[-9] == '1':
        dvudol = True
    AllVertex = {}
    if dvudol:
        RightVertex =set([])
        LeftVertex = set([])

    AllVertex, LeftVertex, RightVertex = build_vertex_adjacency(data, dvudol)
    countVertex = len(AllVertex)
    print('----1.1----')
    print('Количество вершин в графе: ' + str(countVertex))
    M = calculate_edge_count(AllVertex)
    print('Количество ребер в графе: ' + str(M))
    sys.setrecursionlimit(1000000)
    density = calculate_density(M, LeftVertex, RightVertex, countVertex)
    print ('Плотность графа: ' + str(density))

    # Использование функций для поиска компонент и вычисления доли вершин в максимальной компоненте
    components = find_weak_components(AllVertex, countVertex)
    print('Количество компонент слабой связности: ' + str(len(components)))
    print('Доля вершин в максимальной по мощности компоненте слабой связности: ' + str(calculate_largest_component_ratio(components, countVertex)))






    print('----1.2----')
    #Получение метрик расстойний на случайном подграфе
    max_component = max(components, key=len)
    # Определим случайные подграфы и вычислим их метрики
    if len(max_component) > 750: # Если компонент содержит более 750 вершин, создаем случайный подграф и подграф методом "снежный ком"
    
        random_component = [random.choice(max_component) for _ in range(750)]
        snow_component = bfs_for_snow_subgraph([random.choice(max_component) for _ in range(3)], AllVertex)
    
        print('Метрики расстояний на случайном подграфе: ')
        random_diameter, random_radius, random_percentile = calculate_graph_metrics(random_component, AllVertex)
        print(f'Диаметр графа: {random_diameter}')
        print(f'Радиус графа: {random_radius}')
        print(f'90 процентиль расстояния в графе: {random_percentile}')
    
        print('Метрики расстояний на подграфе методом снежный ком:')
        snow_diameter, snow_radius, snow_percentile = calculate_graph_metrics(snow_component, AllVertex)
        print(f'Диаметр графа: {snow_diameter}')
        print(f'Радиус графа: {snow_radius}')
        print(f'90 процентиль расстояния в графе: {snow_percentile}')
    else: # В противном случае рассчитываем метрики для всего компонентаv
    
        diameter, radius, percentile = calculate_graph_metrics(max_component, AllVertex)
        print('Метрики расстояний на компоненте:')
        print(f'Диаметр графа: {diameter}')
        print(f'Радиус графа: {radius}')
        print(f'90 процентиль расстояния в графе: {percentile}')






    print('----1.3----')
    # Вычисление и вывод результатов
    average_clustering_coefficient = calculate_average_clustering_coefficient(AllVertex, countVertex)
    assortativity_coefficient = calculate_assortativity_coefficient(data, AllVertex, countVertex)

    print('Средний кластерный коэффициент:', average_clustering_coefficient)
    print('Коэффициент ассортативности:', assortativity_coefficient)





def build_vertex_adjacency(data, is_dvudol): #Вычисление долей вершин, по спискам смежности
    AllVertex = {}
    LeftVertex, RightVertex = set(), set()

    for index, row in data.iterrows():
        if is_dvudol:
            LeftVertex.add(row['in'])
            RightVertex.add(row['out'])
        
        source_vertex = row['in']
        target_vertex = row['out']

        if source_vertex == target_vertex:
            continue

        # Обработка левой вершины
        left_neighbors = AllVertex.get(source_vertex, [])
        if target_vertex not in left_neighbors:
            left_neighbors.append(target_vertex)
            AllVertex[source_vertex] = left_neighbors

        # Обработка правой вершины
        right_neighbors = AllVertex.get(target_vertex, [])
        if source_vertex not in right_neighbors:
            right_neighbors.append(source_vertex)
            AllVertex[target_vertex] = right_neighbors

    return AllVertex, LeftVertex, RightVertex
        
def calculate_edge_count(AllVertex): # Вычисление кол-ва ребер
    count = 0
    for vertex_neighbors in AllVertex.values():
        count += len(vertex_neighbors)
    return count / 2

def calculate_density(M, LeftVertex, RightVertex, countVertex): #Вычисление плотности графа
    if LeftVertex and RightVertex:
        density = M / (len(RightVertex) * len(LeftVertex))
    else:
        density = M / (countVertex * (countVertex - 1) * 0.5)
    return density

def depth_first_search(AllVertex, vertex, visited, component): #DFS
    visited.add(vertex)
    component.append(vertex)
    neighbors = AllVertex.get(vertex, [])
    
    for neighbor in neighbors:
        if neighbor not in visited:
            depth_first_search(AllVertex, neighbor, visited, component)

def find_weak_components(AllVertex, countVertex): #Вычисление компонент слабой связности
    visited = set()
    components = []

    for vertex in AllVertex:
        if len(visited) == countVertex:
            break
        if vertex not in visited:
            component = []
            depth_first_search(AllVertex, vertex, visited, component)
            components.append(component)
    
    return components

def calculate_largest_component_ratio(components, countVertex): #Доля вершин в максимальной по мощности компоненте слабой связности
    largest_component = max(components, key=len)
    ratio = len(largest_component) / countVertex
    return ratio

def bfs_for_snow_subgraph(start_vertex, AllVertex):
    # Ищем подграф с помощью обхода в ширину (BFS)
    subgraph = []
    queue = deque()
    queue.extend(start_vertex)
    visited = set()

    while len(queue) > 0 and len(subgraph) < 750:
        current_vertex = queue.popleft()
        subgraph.append(current_vertex)
        neighbors = AllVertex.get(current_vertex)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return subgraph

def calculate_graph_metrics(graph, AllVertex):
    # Рассчитываем метрики графа, такие как диаметр, радиус и 90-процентиль расстояния
    matrix = [[float('inf')] * len(graph) for _ in range(len(graph))]
    order_in_graph = {vertex: i for i, vertex in enumerate(graph)}

    for i, vertex in enumerate(graph):
        neighbors = AllVertex.get(vertex)
        for neighbor in neighbors:
            j = order_in_graph.get(neighbor)
            if j is not None:
                matrix[i][j] = 1

    for k in range(len(graph)):
        for i in range(len(graph)):
            for j in range(len(graph)):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

    radius = float('inf')
    diameter = 0
    distances = []

    for row in matrix:
        max_distance_in_row = -1
        for item in row:
            if item != float('inf'):
                distances.append(item)
                max_distance_in_row = max(max_distance_in_row, item)
        if max_distance_in_row != -1:
            radius = min(max_distance_in_row, radius)
            diameter = max(max_distance_in_row, diameter)

    return diameter, radius, np.percentile(distances, 90)

def calculate_average_clustering_coefficient(AllVertex, countVertex):
    total_clustering_coefficient = 0
    for vertex, neighbors in AllVertex.items():
        if len(neighbors) < 2:
            continue
        local_clustering_coefficient = 0
        for neighbor in neighbors:
            common_neighbors = set(neighbors) & set(AllVertex.get(neighbor, []))
            local_clustering_coefficient += len(common_neighbors)
        local_clustering_coefficient /= (len(neighbors) * (len(neighbors) - 1))
        total_clustering_coefficient += local_clustering_coefficient
    average_clustering_coefficient = total_clustering_coefficient / countVertex
    return average_clustering_coefficient

# Функция для вычисления коэффициента ассортативности
def calculate_assortativity_coefficient(data, AllVertex, countVertex):
    multiply_m = 0
    summary_m = 0
    square_summary_m = 0
    cube_summary_m = 0
    visited_pairs = set()
    
    for index, row in data.iterrows():
        pair = (row['in'], row['out'])
        if pair in visited_pairs or pair[::-1] in visited_pairs:
            continue
        j = len(AllVertex.get(row['in'], []))
        k = len(AllVertex.get(row['out'], []))
        multiply_m += j * k
        summary_m += j + k
        square_summary_m += j * j + k * k
        visited_pairs.add(pair)
    
    M = len(visited_pairs)
    M_reverse = 1 / M
    r = (multiply_m - M_reverse * ((0.5 * summary_m) ** 2)) / (0.5 * square_summary_m - M_reverse * ((0.5 * summary_m) ** 2))
    
    return r