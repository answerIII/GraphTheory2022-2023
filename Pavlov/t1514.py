class Solution:
    def maxProbability(self, n, edges, succProb, start, end):
        p = [0] * n
        p[start] = 1
        changed = True

        while changed:
            changed = False

            for i in range(len(edges)):
                u, v = edges[i]
                w = succProb[i]

                if p[u] * w > p[v]:
                    p[v] = p[u] * w
                    changed = True

                if p[v] * w > p[u]:
                    p[u] = p[v] * w
                    changed = True

        return p[end]
