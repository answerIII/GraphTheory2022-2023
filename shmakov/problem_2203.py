class Solution(object):

    def minimumWeight(self, n, edges, src1, src2, dest):
        M = [[] for _ in range(n)]
        reversed_M = [[] for _ in range(n)]
        for i,j,k in edges:
            M[i].append([j, k])
            reversed_M[j].append([i, k])
        def dijkastra(M,src):
            R = [float("inf") for _ in range(n)] # список наименьших расстояний
            R[src] = 0 # рассматриваем путь из источника, следовательно наименьшее расстояние из источника в источник = 0
            heap = [(0,src)]
            while heap:
                r,current = heapq.heappop(heap) # r - кратчайшее расстояние до вершины, current - текущая рассматриваемая вершина
                if (R[current] < r):
                    continue
                for neibour in M[current]: # среди соседей найдем такого, до которого будет найменьшее растояние с учетом полученных результатов
                    if R[current]+neibour[1] < R[neibour[0]]:
                        R[neibour[0]] = r + neibour[1]
                        heapq.heappush(heap, (r + neibour[1],neibour[0]))
            return R
        first = dijkastra(M, src1)
        second = dijkastra(M, src2)
        third = dijkastra(reversed_M, dest)
        out = float("inf")
        for i in range(n):
            out = min(out, first[i] + second[i] + third[i])
        if out == float("inf"):
            return -1
        return out
