import csv
from collections import defaultdict
from math import log



# Функция для вычисления общих соседей (Common Neighbours)
def common_neighbors(graph, node1, node2):
    neighbors1 = set(graph[node1])
    neighbors2 = set(graph[node2])
    return len(neighbors1.intersection(neighbors2))

# Функция для вычисления Adamic-Adar
def adamic_adar(graph, node1, node2):
    common_neighbors = set(graph[node1]).intersection(set(graph[node2]))
    score = 0
    for neighbor in common_neighbors:
        degree = len(graph[neighbor])
        if degree > 1:
            score += 1 / (log(degree))
    return score

# Функция для вычисления Jaccard Coefficient
def jaccard_coefficient(graph, node1, node2):
    neighbors1 = set(graph[node1])
    neighbors2 = set(graph[node2])
    intersection_size = len(neighbors1.intersection(neighbors2))
    union_size = len(neighbors1.union(neighbors2))
    return intersection_size / union_size if union_size > 0 else 0

# Функция для вычисления Preferential Attachment
def preferential_attachment(graph, node1, node2):
    return len(graph[node1]) * len(graph[node2])


def calculate_aggregated_features_for_edges(graph, edges):
    aggregated_features = defaultdict(dict)
    
    for edge in edges:
        node1, node2, weight, time = edge
        if (node1, node2) not in aggregated_features:
            aggregated_features[(node1, node2)] = defaultdict(list)
        if (node2, node1) not in aggregated_features:
            aggregated_features[(node2, node1)] = defaultdict(list)
        
        for func in range(1, 9):
            if func not in aggregated_features[(node1, node2)]:
                aggregated_features[(node1, node2)][func] = []
            if func not in aggregated_features[(node2, node1)]:
                aggregated_features[(node2, node1)][func] = []
            
            aggregated_features[(node1, node2)][func].append(weight)
            aggregated_features[(node2, node1)][func].append(weight)


    for edge in aggregated_features:
        for func in range(1, 9):
            if func in aggregated_features[edge]:
                values = aggregated_features[edge][func]
                if func == 1:    # Нулевой квартиль - минимальное значение из набора весов
                    aggregated_features[edge][func] = 0 if len(values) == 0 else min(values)
                elif func == 2:  # Первый квартиль  - разделяет первую четверть (25%) от остальных весов в упорядоченном наборе
                    aggregated_features[edge][func] = 0 if len(values) == 0 else sorted(values)[len(values) // 4]
                elif func == 3:  # Второй квартиль  - разделяет весь набор весов пополам (50%)
                    aggregated_features[edge][func] = 0 if len(values) == 0 else sorted(values)[len(values) // 2]
                elif func == 4:  # Третий квартиль  - разделяет первые три четверти (75%) от остальных весов в упорядоченном наборе
                    aggregated_features[edge][func] = 0 if len(values) == 0 else sorted(values)[3 * len(values) // 4]
                elif func == 5:  # Четвертый квартиль - максимальное значение из набора весов
                    aggregated_features[edge][func] = 0 if len(values) == 0 else max(values)
                elif func == 6:  # Сумма всех весов в наборе
                    aggregated_features[edge][func] = sum(values)
                elif func == 7:  # Среднее значение весов
                    aggregated_features[edge][func] = sum(values) / len(values) if len(values) > 0 else 0
                elif func == 8:  # Дисперсия, которая измеряет разброс весов относительно их среднего значения.
                    mean = sum(values) / len(values) if len(values) > 0 else 0
                    aggregated_features[edge][func] = sum((x - mean) ** 2 for x in values) / len(values) if len(values) > 0 else 0

    return aggregated_features


