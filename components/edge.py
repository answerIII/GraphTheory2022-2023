from components.graph import Graph
from math import log


# Ребро неориентированного графа
class Edge(Graph):
    #node1 = -1
    #node2 = -1
    #weight = -1
    #time = -1
    def __init__(self, node1, node2, weight, time) -> None:
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.time = time

    def calc_static_features():
        print ('')


    # Функция для вычисления общих соседей (Common Neighbours)
    def common_neighbors(self):
        neighbors1 = set(self.graph[self.node1])
        neighbors2 = set(self.graph[self.node2])
        return len(neighbors1 & neighbors2)


    # Функция для вычисления Adamic-Adar
    def adamic_adar(self):
        common_neighbors = set(self.graph[self.node1]) & set(self.graph[self.node2])
        score = 0
        for neighbor in common_neighbors:
            degree = len(self.graph[neighbor])
            if degree > 1:
                score += 1 / (log(degree))
        return score

    # Функция для вычисления Jaccard Coefficient
    def jaccard_coefficient(self):
        neighbors1 = set(self.graph[self.node1])
        neighbors2 = set(self.graph[self.node2])
        intersection_size = len(neighbors1 & neighbors2)
        union_size = len(neighbors1 | neighbors2)
        return intersection_size / union_size if union_size > 0 else 0

    # Функция для вычисления Preferential Attachment
    def preferential_attachment(self):
        return len(self.graph[self.node1]) * len(self.graph[self.node2])

    
        