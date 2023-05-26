import os
from pathlib import Path
from features import temporal_selection_model, static_selection_model
import matplotlib.pyplot as plt
from first import analyze_graph, calculate_distance
from static_features import compute_static_features_for_pair

datasets = [w for w in Path("conf.txt").read_text(encoding="utf-8").replace("\n", " ").split()]

def graph_selection(datasets):
    print("Выберите нужный датасет:")
    for i in range(len(datasets)):
        print(f"{i}. {datasets[i]}")
    s = input()
    if not s.isdigit:
        print("Wrong input")
        graph_selection(datasets)
    elif int(s) > len(datasets) or int(s) < 0:
        print("Wrong input")
        graph_selection(datasets)
    else:
        return graph_info(datasets[int(s)])

def graph_info(dataset):

    if(not os.path.exists("datasets")):
        os.mkdir("datasets")
    try:
        f = open(f'./datasets/{dataset}')
        f.close()
    except FileNotFoundError:
        print('Файл не существует! Проверьте conf.txt')
        return graph_selection(datasets)

    with open(f'./datasets/{dataset}', 'r') as file:
        data = file.readlines()

    graph = {}
    for i, edge in enumerate(data):
        edge = edge.strip().split()
        u = int(edge[0])
        v = int(edge[1])
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    set_graph = {}
    for i, edge in enumerate(data):
        edge = edge.strip().split()
        u = int(edge[0])
        v = int(edge[1])
        if u not in set_graph:
            set_graph[u] = set()
        if v not in set_graph:
            set_graph[v] = set()
        set_graph[u].add(v)
        set_graph[v].add(u)

    print("Выберите какую информацию вы хотите получить:")
    print("1. Основные свойства для статического графа")
    print("2. Подсчет расстояния между двумя вершинами")
    print("3. Предсказание на основе статических характеристик")
    print("4. Предсказание на основе темпоральных характеристик")
    print("5. Подсчет статичесих характеристик для пары вершин")
    print()
    print("-1. Назад")

    command = int(input())

    match command:
        case 1:
            print(analyze_graph(f"datasets/{dataset}"))
        case 2: 
                calculate_distance(graph)
        case 3:
            print(static_selection_model(dataset))
        case 4:
            print(temporal_selection_model(dataset))
        case 5:
            compute_static_features_for_pair(set_graph)
        case -1:
            graph_selection(datasets)
        case _:
            print("Неправильный ввод, слелайде выбор еще раз")


        
if __name__ == "__main__":
    graph_selection(datasets)
