import pandas as pd
import numpy as np
import sys
import random
from collections import deque
from first_task_functions.assortativity_coefficient import calculate_assortativity_coefficient
from first_task_functions.average_clustering_coefficient import calculate_average_clustering_coefficient
from first_task_functions.graph_metrics import calculate_graph_metrics
from first_task_functions.features_functions import calculate_edge_count, build_vertex_adjacency, find_weak_components, calculate_density, calculate_largest_component_ratio, bfs_for_snow_subgraph

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

    AllVertex, LeftVertex, RightVertex = build_vertex_adjacency(data, dvudol) #вычисление вершин, учитывается двудольность графа
    countVertex = len(AllVertex)

    print('----1.1----')
    print('Количество вершин в графе: ' + str(countVertex))
    M = calculate_edge_count(AllVertex)
    print('Количество ребер в графе: ' + str(M))
    sys.setrecursionlimit(1000000)
    density = calculate_density(M, LeftVertex, RightVertex, countVertex) #вычисление плотности графа
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
        print(f'Диаметр графа: {random_diameter}') #наибольшее расстояние между всеми парами вершин графа
        print(f'Радиус графа: {random_radius}') #минимальный эксцентриситет среди всех вершин графа
        print(f'90 процентиль расстояния в графе: {random_percentile}')
    
        print('Метрики расстояний на подграфе методом снежный ком:')
        snow_diameter, snow_radius, snow_percentile = calculate_graph_metrics(snow_component, AllVertex)
        print(f'Диаметр графа: {snow_diameter}')
        print(f'Радиус графа: {snow_radius}')
        print(f'90 процентиль расстояния в графе: {snow_percentile}')
    else: # В противном случае рассчитываем метрики для макс компоненты
    
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











