from collections import defaultdict
from typing import List


class Solution:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        def dfs(current_time, node):
            nonlocal res
            if node not in graph:
                res = max(res, current_time)
            for child in graph[node]:
                dfs(current_time + informTime[node], child)

        graph = defaultdict(list)
        for i, j in enumerate(manager):
            graph[j].append(i)
        res = 0
        dfs(0, headID)
        return res