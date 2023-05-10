class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        adj = [[] for i in range(n)]  # adjacency list initialization
        for u, v, t in roads:
            adj[u].append((v, t))
            adj[v].append((u, t))

        times = [float('inf')] * n  # info about time required to arrive at i-th node
        times[0] = 0
        ways = [0] * n  # info about all acceptable roads leading to i-th node
        ways[0] = 1

        # dijkstra's implementation for shortest path
        # using python's priority queue api
        pq = [(0, 0)]  # (time, node)

        while pq:
            time_old, current = heapq.heappop(pq)  # as in dijkstra's, choose node with min time

            for v, t in adj[current]:
                time_new = time_old + t  # calculate time for node v

                if time_new < times[v]:
                    times[v] = time_new
                    ways[v] = ways[current]
                    heapq.heappush(pq, (time_new, v))
                elif time_new == times[v]:
                    ways[v] += ways[current]

        mod = 10 ** 9 + 7

        return ways[n-1] % mod