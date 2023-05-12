class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        import heapq

        # Представляем граф в виде списков смежности 
        # u -> [(x_1,y_1),...,(x_l,y_l)], l<= 4
        # x_1 - номер вершины, x_2 - вес ребра из вершины номер u в вершину номер x_1
        # Вес в условиях данной задачи - вероятность перехода по данному ребру
        def adj_list(n,edges,succProb):
            t = [ [] for _ in range(n)]  
            # Добавляем неориентированные ребра с весами - вероятностями перехода
            for i,e in enumerate(edges):
                t[ e[0] ].append((e[1], succProb[i]))
                t[ e[1] ].append((e[0], succProb[i]))
            return t

        # Воспользуемся алгоритмом Дейкстры, немного изменив его для нашей задачи
        # Воспользуемся алгоритмом Дейкстры, немного изменив его для нашей задачи
        def dijkstras(g, root, n): # На вход подается граф в виде списков смежности
            dist = [0 for _ in range(n)] # Изначальное вероятность достижения других вершин = 0
            dist[root] = 1 # Вероятность достичь начальную вершину = 1
            visited = [False for _ in range(n)]
            pq = [(-1, root)] # Очередь с приоритетами (dist[node],node), первый элемент - корневой узел
            # Делаем отрицательные значения вероятностей, чтобы сделать из приоритет для большего по модулю значения

            while pq:
                _, u = heapq.heappop(pq) # Рассматриваем текущий узел
                # Если узел посещали - пропускаем
                if visited[u]:
                    continue
                visited[u] = True

                for i in range(len(g[u])):
                    # Вытаскиваем номер вершины, которую мы хотим посетить
                    v = g[u][i][0] 
                    # Если текущая вероятность достижения рассматриваемого узла * вероятность достижения узла, которого мы хотим посетить
                    # больше, чем текущая вероятность достижения посещяемой вершины
                    # то заменяем значение расстояния и добавляем узел в очередь с приоритетом
                    if (abs(dist[u]*g[u][i][1]) > abs(dist[v])):
                        dist[v] = -1 * abs(dist[u]*g[u][i][1])
                        heapq.heappush(pq, (dist[v], v))
            return dist
        a = adj_list(n,edges,succProb)
        probability = dijkstras(a, start,n)
        return -probability[end]