class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        #Для вершин src1 src2 необходимо найти найти кратчейшее расстрояние до их некоторого общего узла
        #Затем кратчейшее от этого узла до dest (с помощью обратного графа)
        #Для поиска путей - алгоритм Дейкстры ( тк в условии сказано, что веса положит)
        graph = defaultdict(list)
        rev_graph = defaultdict(list)
        for i, j, d in edges:
            graph[i].append([j, d])
            rev_graph[j].append([i, d])

        def Dijkstra(graph, src):
            visited = set()
            dist = [float("inf") for k in range(n)]
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                weight, node = heappop(heap)
                if node in visited: continue
                visited.add(node)
                for neib, neib_weight in graph[node]:
                    if dist[node] + neib_weight < dist[neib]:
                        dist[neib] = weight + neib_weight
                        heappush(heap, (dist[neib], neib))
            return dist

        G_src1 = Dijkstra(graph, src1)
        G_src2 = Dijkstra(graph, src2)
        rG_dest = Dijkstra(rev_graph, dest)

        res = float("inf")
        for i in range(n):
            res = min(res, G_src1[i] + G_src2[i] + rG_dest[i])

        return res if res != float("inf") else -1
