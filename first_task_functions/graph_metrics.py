import numpy as np

# Рассчитываем метрики графа, такие как диаметр, радиус и 90-процентиль расстояния

def calculate_graph_metrics(graph, AllVertex):
   
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
