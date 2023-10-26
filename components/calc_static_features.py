import math
from components.calculator import Calculator
from collections import defaultdict
from math import log
import time

class Static_calculator(Calculator):
    
    def calc(self, graph):
        print('Начинаю статические вычисления')
        start_time = time.time()

        graph_dict = defaultdict(list)
        for edge in graph.edges: #Преобразуем ориентированный граф в неориентированный, добавляя обратные ребра
            graph_dict[edge.node1].append(edge.node2)
            graph_dict[edge.node2].append(edge.node1)

        



        for i, node1 in enumerate(graph_dict):
            for j, node2 in enumerate(graph_dict):
                if i < j:
                    cn = self.common_neighbors(graph_dict, node1, node2)
                    aa = self.adamic_adar(graph_dict, node1, node2)
                    jc = self.jaccard_coefficient(graph_dict, node1, node2)
                    pa = self.preferential_attachment(graph_dict, node1, node2)
                    result1 = {
                        'Node1': node1,
                        'Node2': node2,
                        'Common Neighbours': cn,
                        'Adamic-Adar': aa,
                        'Jaccard Coefficient': jc,
                        'Preferential Attachment': pa
                    }
                    result2 = {
                        'Node1': node2,
                        'Node2': node1,
                        'Common Neighbours': cn,
                        'Adamic-Adar': aa,
                        'Jaccard Coefficient': jc,
                        'Preferential Attachment': pa
                    }
                    #print(result1)
                    #print(result2)

                    graph.static_features.append(result1)  #Для ускорения вычислений вычисляем за раз прямое и обратное ребро 
                    graph.static_features.append(result2)

        end_time = time.time()   
        execution_time1 = end_time - start_time
        print(f"Время выполнения: {execution_time1} секунд")

    # Функция для вычисления общих соседей (Common Neighbours)
    def common_neighbors(self, graph, node1, node2):
        neighbors1 = set(graph[node1])
        neighbors2 = set(graph[node2])
        return len(neighbors1 & neighbors2)


    # Функция для вычисления Adamic-Adar
    def adamic_adar(self, graph, node1, node2):
        common_neighbors = set(graph[node1]) & set(graph[node2])
        score = 0
        for neighbor in common_neighbors:
            degree = len(graph[neighbor])
            if degree > 1:
                score += 1 / (log(degree))
        return score

    # Функция для вычисления Jaccard Coefficient
    def jaccard_coefficient(self, graph, node1, node2):
        neighbors1 = set(graph[node1])
        neighbors2 = set(graph[node2])
        intersection_size = len(neighbors1 & neighbors2)
        union_size = len(neighbors1 | neighbors2)
        return intersection_size / union_size if union_size > 0 else 0

    # Функция для вычисления Preferential Attachment
    def preferential_attachment(self, graph, node1, node2):
        return len(graph[node1]) * len(graph[node2])
