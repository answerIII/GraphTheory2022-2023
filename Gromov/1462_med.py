import numpy as np
class Solution:

    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        # Реализация построения транзитивного замыкания с помощью метода Флойда-Уоршелла
        def transitiveClosure(adj,v): # На вход подаются матрица смежности и количество вершин
            # Изначально - матрица смежности
            reach = adj
            for k in range(v):
                # Выбираем все вершины как источники
                for i in range(v):
                    # Выбираем вершины-стоки для вышевыбранных вершин
                    for j in range(v):
                        # Проверяем, есть ли какой-то путь между ними
                        # Это может быть прямое ребро или путь, проходящий через вершину-посредника k 
                        reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
            return reach
        # Построение матрицы смежности для графа
        def adjacencyMatrix(g, v):
            m = np.zeros((v,v))
            for i in range(len(g)):
                m[ g[i][0] ][ g[i][1] ] = 1
            return m
        
        m = adjacencyMatrix(prerequisites, numCourses)
        t = transitiveClosure(m, numCourses)

        lst = []
        if (len(prerequisites) == 0):
            for i in range(len(queries)):
                lst.append(False) 
        else: 
            for i in range(len(queries)):
                if (t[ queries[i][0] ][ queries[i][1]] ):
                    lst.append(True)
                else:
                    lst.append(False)
        return lst