class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        import numpy as np
        import heapq
        # Представляем граф в виде списков смежности 
        # u -> [(x_1,y_1),...,(x_l,y_l)], l<= 4
        # x_1 - номер вершины, x_2 - вес ребра из вершины номер u в вершину номер x_1
        def adj_list(g):
            m = len(g)
            n = len(g[0])
            v = n*m
            t = [ [] for _ in range(v)]
            k = 0
            for i in range(m):
                for j in range(n):
                # Вместо k можно вычислять номер узла как i*n + j

                # Вес ребер между смежными, но не на них направленными = 1
                # Вес ребер, которые находятся в направлении стрелок = 0

                # Если значение узла = 1
                    if (g[i][j] == 1):
                        if (j < n - 1):
                            t[k].append((k+1,0)) # Вес ребра k -> (k+1) = 0 >
                        if (j > 0):
                            t[k].append((k-1,1))
                        if (i < m - 1):
                            t[k].append((k+n,1))
                        if (i > 0):
                            t[k].append((k-n,1))
                    # Если значение узла = 2
                    elif (g[i][j] == 2):
                        if (j < n - 1):
                            t[k].append((k+1,1))
                        if (j > 0):
                            t[k].append((k-1,0)) # Вес ребра k -> (k-1) = 0 <
                        if (i < m - 1):
                            t[k].append((k+n,1))
                        if (i > 0):
                            t[k].append((k-n,1))
                    # Если значение узла = 3
                    elif (g[i][j] == 3):
                        if (j < n - 1):
                            t[k].append((k+1,1))
                        if (j > 0):
                            t[k].append((k-1,1))
                        if (i < m - 1):
                            t[k].append((k+n,0)) # Вес ребра k -> (k+n) = 0 v
                        if (i > 0):
                            t[k].append((k-n,1))
                    # Если значение узла = 4
                    elif (g[i][j] == 4):
                        if (j < n - 1):
                            t[k].append((k+1,1))
                        if (j > 0):
                            t[k].append((k-1,1))
                        if (i < m - 1):
                            t[k].append((k+n,1))
                        if (i > 0):
                            t[k].append((k-n,0)) # Вес ребра k -> (k-n) = 0 ^
                        
                    k += 1 # Переходим к следующему узлу
                
            return t

        def dijkstras(g, root): # На вход подается граф в виде списков смежности
            v = len(g)
            dist = [1000000 for _ in range(v)] # Изначальное расстояния до других вершин - что-то большое
            dist[root] = 0 # До вершины, с которой мы начинаем, расстояние = 0
            visited = [False for _ in range(v)]
            pq = [(0, root)] # Очередь с приоритетами (dist[node],node), первый элемент - корневой узел

            while pq:
                _, u = heapq.heappop(pq) # Рассматриваем текущий узел
                # Если узел посещали - пропускаем
                if visited[u]:
                    continue
                visited[u] = True

                for i in range(len(g[u])):
                    # Вытаскиваем номер вершины, которую мы хотим посетить
                    v = g[u][i][0] 
                    # Если текущее расстояние до узла + расстояние до узла, которого мы хотим посетить
                    # меньше, чем текущее расстояние до посещяемой вершины
                    # то заменяем значение расстояния и добавляем узел в очередь с приоритетом
                    #print(g[u][i][1])
                    if (dist[u] + g[u][i][1] < dist[v]):
                        dist[v] = dist[u] + g[u][i][1]
                        heapq.heappush(pq, (dist[v], v))
            return dist

        a = adj_list(grid)
        cost = dijkstras(a,0)
        v = len(a)
        # Возвращаем цену расстояния от узла (0;0) до узла (m-1;n-1)
        return int(cost[v-1])