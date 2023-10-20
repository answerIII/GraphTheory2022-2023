import csv
from collections import defaultdict
from math import log
from second_task_functions.data_preporating import read_graph_edges_from_csv, write_results_to_csv, read_edge_features_from_csv
from second_task_functions.static_topological_features import common_neighbors, adamic_adar, jaccard_coefficient, preferential_attachment, calculate_aggregated_features_for_edges
from second_task_functions.bin_clasification import bin_clasification


def feature_vector_construction(filename):

    file = 'datasets/'+ filename +'.csv'   
     # Чтение ребер графа из CSV-файла
    graph_edges = read_graph_edges_from_csv(file)
    # Создание структуры данных для представления графа в виде списка смежности
    graph = defaultdict(list)
    for edge in graph_edges:
        graph[edge[0]].append(edge[1])
        graph[edge[1]].append(edge[0])
    results = []
    
    print('----2.1.1----')
    for node1 in graph:
        for node2 in graph:
            if node1 != node2:
                cn = common_neighbors(graph, node1, node2)
                aa = adamic_adar(graph, node1, node2)
                jc = jaccard_coefficient(graph, node1, node2)
                pa = preferential_attachment(graph, node1, node2)
                result = {
                    'Node1': node1,
                    'Node2': node2,
                    'Common Neighbours': cn,
                    'Adamic-Adar': aa,
                    'Jaccard Coefficient': jc,
                    'Preferential Attachment': pa
                }
                print(result)
                results.append(result)

    file = 'done/'+ filename + '_DONE.csv'   
    write_results_to_csv(results, file)

    print('----2.1.2----')
    aggregated_features = calculate_aggregated_features_for_edges(graph, graph_edges)
    for edge, features in aggregated_features.items():
        node1, node2 = edge
        print(f'Edge ({node1}, {node2}):')
        for func, value in features.items():
            print(f'Function {func}: {value}')
        print('-' * 40)
    print('Function 1: Нулевой квартиль - минимальное значение из набора весов')
    print('Function 2: Первый квартиль  - разделяет первую четверть (25%) от остальных весов в упорядоченном наборе')
    print('Function 3: Второй квартиль  - разделяет весь набор весов пополам (50%)')
    print('Function 4: Третий квартиль  - разделяет первые три четверти (75%) от остальных весов в упорядоченном наборе')
    print('Function 5: Четвертый квартиль - максимальное значение из набора весов')
    print('Function 6: Сумма всех весов в наборе')
    print('Function 7: Среднее значение весов')
    print('Function 8: Дисперсия, которая измеряет разброс весов относительно их среднего значения')


    




