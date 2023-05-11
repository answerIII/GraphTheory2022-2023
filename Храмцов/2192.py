class Solution(object):
    def getAncestors(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[List[int]]
        """
        ancestors = [set() for i in range(n)]

        new_edges = [[] for i in range(n)]

        for edge in edges:
            ancestors[edge[1]].add(edge[0])
            new_edges[edge[0]].append(edge[1])

        queue = []

        for i in range(n):
            if (len(ancestors[i]) == 0):
                queue.append(i)

        while len(queue) > 0:
            u = queue.pop(0)
            print(u)
            for v in new_edges[u]:
                ancestors[v] = ancestors[u].union(ancestors[v])
                if (v not in queue):
                    queue.append(v)

        for i in range(n):
            ancestors[i] = list(ancestors[i])
            ancestors[i].sort()
        return ancestors
