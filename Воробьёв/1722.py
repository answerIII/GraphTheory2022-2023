from collections import defaultdict, Counter
from typing import List


class Solution:
    def dfs(self, graph, node, visited):
        for i in graph[node]:
            if i not in visited:
                visited.add(i)
                self.dfs(graph, i, visited)

    def hamming_dist(self, a, b, n):
        cnt = 0
        for j in a:
            cnt += min(a[j], b[j])
        return n - cnt

    def minimumHammingDistance(self, source: List[int], target: List[int], allowedSwaps: List[List[int]]) -> int:
        graph = defaultdict(list)
        n = len(source)
        dist = 0
        for a, b in allowedSwaps:
            graph[a].append(b)
            graph[b].append(a)
        visited = set()

        for x in graph:
            if x not in visited:
                current = {x}
                self.dfs(graph, x, current)
                nv = len(current)
                source_num = Counter([source[p] for p in current])
                target_num = Counter([target[p] for p in current])
                dist += self.hamming_dist(source_num, target_num, nv)
                visited.update(current)
        for i in range(n):
            if i not in visited and source[i] != target[i]:
                dist += 1
        return dist
