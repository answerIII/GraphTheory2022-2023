import random
import numpy as np
import networkx as nx

# Считывание данных из файла и создание графа
G = nx.Graph()
with open('5.txt', 'r') as file:
    data = file.readlines()

for edge in data:
    u, v, q, t = map(int, edge.strip().split())
    G.add_edge(u, v, weight=q, time=t)

# 1. Вычисление основных характеристик графа
num_nodes = G.number_of_nodes()  # Число вершин
num_edges = len(data)  # Число ребер
density = nx.density(G)  # Плотность графа

# Вычисление компонент слабой связности
components = list(nx.connected_components(G))
num_components = len(components)  # Число компонент слабой связности
largest_component = max(components, key=len)
largest_component_size = len(largest_component)  # Размер максимальной компоненты
largest_component_fraction = largest_component_size / num_nodes  # Доля вершин в максимальной компоненте

print("1. Характеристики графа:")
print("Число вершин:", num_nodes)
print("Число ребер:", num_edges)
print("Плотность графа:", density)
print("Число компонент слабой связности:", num_components)
print("Доля вершин в максимальной компоненте слабой связности:", largest_component_fraction)

# 2a. Вычисление расстояний между случайно выбранными вершинами из максимальной компоненты слабой связности
num_random_nodes = min(500, largest_component_size)  # Или использовать 1000, если нужно
random_nodes = random.sample(list(largest_component), num_random_nodes)  # Выбор случайных вершин из максимальной компоненты
distances = []

# Поиск расстояний с помощью алгоритма Флойда-Уоршелла
all_pairs_distances = nx.floyd_warshall_numpy(G, weight='time')
for i in range(num_random_nodes):
    for j in range(i + 1, num_random_nodes):
        start = random_nodes[i]
        target = random_nodes[j]
        distances.append(all_pairs_distances[start][target])

max_distance = np.max(distances)
min_distance = np.min(distances)
percentile90 = np.percentile(distances, 90)

print("\n2a. Оценка значений на основе случайно выбранных вершин:")
print("Максимальное расстояние:", max_distance)
print("Минимальное расстояние:", min_distance)
print("90-й процентиль расстояния:", percentile90)

# 2b. Вычисление расстояний по подграфу "снежный ком"
snowball_sample_size = 500  # Размер подграфа "снежный ком"
snowball_sample = random.sample(largest_component, snowball_sample_size)  # Случайный выбор вершин
distances = []

# Поиск расстояний с помощью алгоритма Флойда-Уоршелла
snowball_graph = G.subgraph(snowball_sample)
snowball_pairs_distances = nx.floyd_warshall_numpy(snowball_graph, weight='time')
for i in range(num_random_nodes):
    for j in range(i + 1, num_random_nodes):
        start = random_nodes[i]
        target = random_nodes[j]
        distances.append(snowball_pairs_distances[start][target])

max_snowball_distance = np.max(distances)
min_snowball_distance = np.min(distances)
percentile90_snowball = np.percentile(distances, 90)

print("\n2b. Оценка значений на основе подграфа 'снежный ком':")
print("Максимальное расстояние:", max_snowball_distance)
print("Минимальное расстояние:", min_snowball_distance)
print("90-й процентиль расстояния:", percentile90_snowball)

# 3. Вычисление среднего кластерного коэффициента
cluster_coefficients = nx.clustering(G, weight='time').values()
mean_cluster_coefficient = np.mean(list(cluster_coefficients))

print("\n3. Средний кластерный коэффициент:")
print("Средний кластерный коэффициент:", mean_cluster_coefficient)

# 4. Вычисление коэффициента ассортативности
degree_correlation = nx.degree_pearson_correlation_coefficient(G, weight='time')

print("\n4. Коэффициент ассортативности по степени вершин:")
print("Коэффициент ассортативности:", degree_correlation)
