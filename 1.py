import random
import numpy as np
import statistics

def compute_distance(graph, start, end):
    if start not in graph or end not in graph:
        print("Ошибка: введены некорректные номера вершин.")
        return
    visited = set()
    queue = [(start, 0)]
    while queue:
        current_node, distance = queue.pop(0)
        if current_node == end:
            return distance
        if current_node not in visited:
            visited.add(current_node)
            neighbors = graph[current_node]
            queue.extend((neighbor, distance + 1) for neighbor in neighbors)
    return float('inf')


def analyze_graph(file_name):
    output = ""
    # Считывание данных из файла и создание матриц смежности
    with open(file_name, 'r') as file:
        data = file.readlines()

    num_edges = len(data)
    #matrix = [[0] * num_edges for _ in range(num_edges)]
    #time = [[0] * num_edges for _ in range(num_edges)]
    
    # Создание графа в виде словаря смежности
    graph = {}
    edges = set()  # Множество уникальных ребер
    for i, edge in enumerate(data):
        u, v, q, t = map(int, edge.strip().split())
        if u != v:  # Исключаем петли
                edge = (min(u, v), max(u, v))  # Представляем ребро в виде кортежа (u, v), где u < v
                edges.add(edge)
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append(v)
                graph[v].append(u)
        #matrix[u][v] = q
        #time[u][v] = t

    # 1. Вычисление основных характеристик графа
    num_nodes = len(graph)  # Число вершин
    density = num_edges / (num_nodes * (num_nodes - 1) / 2)  # Плотность графа

    # Итеративный алгоритм для поиска компонент слабой связности и максимальной компоненты
    visited = set()
    components = []
    for node in graph:
        if node not in visited:
            component_size = 0
            stack = [node]
            while stack:
                current_node = stack.pop()
                if current_node not in visited:
                    visited.add(current_node)
                    component_size += 1
                    for neighbor in graph[current_node]:
                        stack.append(neighbor)
            components.append(component_size)

    num_components = len(components)  # Число компонент слабой связности
    largest_component_size = max(components)  # Размер максимальной компоненты
    largest_component_fraction = largest_component_size / num_nodes  # Доля вершин в максимальной компоненте

    output += "1. Характеристики графа:\n"
    output += "Число вершин: {}\n".format(num_nodes)
    output += "Число ребер: {}\n".format(num_edges)
    output += "Плотность графа: {}\n".format(density)
    output += "Число компонент слабой связности: {}\n".format(num_components)
    output += "Доля вершин в максимальной компоненте слабой связности: {}\n".format(largest_component_fraction)


    # 2a. Вычисление расстояний между случайно выбранными вершинами из максимальной компоненты слабой связности
    # Получение наибольшей компоненты слабой связности
    largest_component = max(graph.values(), key=len)

    # Выбор случайных вершин из наибольшей компоненты
    random_vertices = random.sample(largest_component, 500)  # Выбор 500 случайных вершин

    # Вычисление расстояний между выбранными вершинами
    distances = []
    for i in range(len(random_vertices)):
        for j in range(i + 1, len(random_vertices)):
            start = random_vertices[i]
            end = random_vertices[j]
            distance = compute_distance(graph, start, end)
            distances.append(distance)

    # Вычисление радиуса, диаметра и 90-процентильного расстояния
    radius = min(distances)
    diameter = max(distances)
    percentile90 = np.percentile(distances, 90)  # 90-процентиль

    # Добавление результатов в вывод
    output += "\n2. a. Оценка значений радиуса, диаметра и 90-процентиля расстояния:\n"
    output += "Радиус: {}\n".format(radius)
    output += "Диаметр: {}\n".format(diameter)
    output += "90-процентиль расстояния: {}\n".format(percentile90)

    # 2b. Вычисление расстояний в подграфе "снежный ком"
    snowball_sample_size = 500  # Размер подграфа "снежный ком"

    snowball_vertices = set(random_vertices)  # Вершины, уже добавленные в подграф "снежный ком"
    queue = list(random_vertices)  # Очередь вершин для обхода
    while len(snowball_vertices) < snowball_sample_size and queue:
        current_vertex = queue.pop(0)
        neighbors = graph[current_vertex]
        for neighbor in neighbors:
            if neighbor not in snowball_vertices:
                snowball_vertices.add(neighbor)
                queue.append(neighbor)

    # Вычисление расстояний в подграфе "снежный ком"
    snowball_distances = []
    snowball_vertices = list(snowball_vertices)  # Преобразование множества в список
    for i in range(len(snowball_vertices)):
        for j in range(i + 1, len(snowball_vertices)):
            start = snowball_vertices[i]
            end = snowball_vertices[j]
            distance = compute_distance(graph, start, end)
            snowball_distances.append(distance)

    # Вычисление радиуса, диаметра и 90-процентильного расстояния в подграфе "снежный ком"
    snowball_radius = min(snowball_distances)
    snowball_diameter = max(snowball_distances)
    snowball_percentile90 = np.percentile(snowball_distances, 90)  # 90-процентиль

    # Добавление результатов расстояний в подграфе "снежный ком" в вывод
    output += "\n2. b. Оценка значений радиуса, диаметра и 90-процентиля расстояния в подграфе 'снежный ком':\n"
    output += "Радиус: {}\n".format(snowball_radius)
    output += "Диаметр: {}\n".format(snowball_diameter)
    output += "90-процентиль расстояния: {}\n".format(snowball_percentile90)


    # 3. Вычисление среднего кластерного коэффициента
    cluster_coefficients = []
    for node in graph:
        neighbors = graph[node]
        num_neighbors = len(neighbors)
        if num_neighbors >= 2:
            num_possible_edges = num_neighbors * (num_neighbors - 1)
            num_actual_edges = 0
            for i in range(num_neighbors):
                for j in range(i + 1, num_neighbors):
                    neighbor1 = neighbors[i]
                    neighbor2 = neighbors[j]
                    if neighbor2 in graph[neighbor1]:
                        num_actual_edges += 1
            cluster_coefficient = (2 * num_actual_edges) / num_possible_edges
            cluster_coefficients.append(cluster_coefficient)

    mean_cluster_coefficient = np.mean(cluster_coefficients)

    output += "\n3. Средний кластерный коэффициент:\n"
    output += "Средний кластерный коэффициент: {}\n".format(mean_cluster_coefficient)


    # 4. Вычисление коэффициента ассортативности
    total_degree_product = 0
    total_edge_weight_product = 0
    total_degree_squared = 0
    total_degree_cubed = 0

    for node in graph.keys():
      ki = len(graph[node])
      total_degree_product += ki
      total_degree_squared += ki * ki
      total_degree_cubed += ki * ki * ki

    for neighbor1 in graph[node]:
        kj = len(graph[neighbor1])
        total_edge_weight_product += ki * kj

    mean_degree_product = total_degree_product / num_nodes
    mean_edge_weight_product = total_edge_weight_product / num_nodes
    mean_degree_squared = total_degree_squared / num_nodes
    mean_degree_cubed = total_degree_cubed / num_nodes

    assortativity_coefficient = (
        (mean_edge_weight_product - (mean_degree_product ** 2) / (2 * num_edges))
        / (mean_degree_squared - (mean_degree_product ** 2) / (2 * num_edges))
    )
    output += "\n4. Коэффициент ассортативности по степени вершин:\n"
    output += "Коэффициент ассортативности: {}\n".format(assortativity_coefficient)

    return output
