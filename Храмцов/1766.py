class Solution(object):
    def getCoprimes(self, nums, edges):
        """
        :type nums: List[int]
        :type edges: List[List[int]]
        :rtype: List[int]
        """
        n = len(nums)

        closest = [-1 for i in range(n)]
        closest_range = [-1 for i in range(n)]

        new_edges = [[] for i in range(n)]
        for edge in edges:
            new_edges[edge[0]].append(edge[1])
            new_edges[edge[1]].append(edge[0])

        def gcd(p, q):
            while q != 0:
                p, q = q, p % q
            return p

        coprimes = [set() for i in range(51)]

        for i in range(1, 51):
            for j in range(1, 51):
                if gcd(i, j) == 1:
                    coprimes[i].add(j)

        def coprime(x, y):
            return y in coprimes[x]

        paths = [[set(), [(0, -1) for i in range(51)]] for i in range(n)]

        queue = [0]

        visited = [0 for i in range(n)]

        while len(queue) > 0:
            u = queue.pop(-1)
            visited[u] = 1
            for v in new_edges[u]:
                if visited[v] == 0:
                    for case in paths[u][0]:
                        if case not in paths[v][0] or (paths[u][1][case][0] + 1 < paths[v][1][case][0]):
                            paths[v][1][case] = (
                                paths[u][1][case][0] + 1, paths[u][1][case][1])
                            paths[v][0].add(case)
                    paths[v][1][nums[u]] = (1, u)
                    paths[v][0].add(nums[u])
                    queue.append(v)
                    for case in paths[v][0]:
                        if coprime(nums[v], case):
                            if closest[v] == -1 or paths[v][1][case][0] < closest_range[v]:
                                closest[v] = paths[v][1][case][1]
                                closest_range[v] = paths[v][1][case][0]

        return closest
