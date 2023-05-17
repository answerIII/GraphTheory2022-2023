import math


class Solution:
    def countPaths(self, n, roads):
        graph = self.buildGraph(n, roads)
        return self.dijkstra(graph, 0, n - 1)

    def buildGraph(self, n, roads):
        graph = [[] for _ in range(n)]
        for u, v, t in roads:
            graph[u].append((v, t))
            graph[v].append((u, t))
        return graph

    def dijkstra(self, graph, src, dst):
        mod = 10**9 + 7
        ways = [0] * len(graph)
        dist = [math.inf] * len(graph)

        ways[src] = 1
        dist[src] = 0
        mh = [(dist[src], src)]

        while mh:
            d, u = self.popMin(mh)
            if d > dist[u]:
                continue
            self.relaxNeighbors(graph, u, d, dist, ways, mh, mod)

        return ways[dst]

    def push(self, heap, item):
        heap.append(item)
        self.siftUp(heap, len(heap) - 1)

    def popMin(self, heap):
        heap[0], heap[-1] = heap[-1], heap[0]
        item = heap.pop()
        self.siftDown(heap, 0)
        return item

    def siftUp(self, heap, i):
        while i > 0:
            parent = (i - 1) // 2
            if heap[i] < heap[parent]:
                heap[i], heap[parent] = heap[parent], heap[i]
                i = parent
            else:
                break

    def siftDown(self, heap, i):
        n = len(heap)
        while i < n:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            if left < n and heap[left] < heap[smallest]:
                smallest = left

            if right < n and heap[right] < heap[smallest]:
                smallest = right

            if smallest != i:
                heap[i], heap[smallest] = heap[smallest], heap[i]
                i = smallest
            else:
                break

    def relaxNeighbors(self, graph, u, d, dist, ways, mh, mod):
        for v, t in graph[u]:
            if d + t < dist[v]:
                dist[v] = d + t
                ways[v] = ways[u]
                self.push(mh, (dist[v], v))
            elif d + t == dist[v]:
                ways[v] += ways[u]
                ways[v] %= mod
