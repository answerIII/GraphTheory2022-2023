from sortedcontainers import SortedList
from typing import List


class Solution:
    def minCost(self, grid: List[List[int]]) -> int:
        dirs_x = [None, 0, 0, 1, -1]
        dirs_y = [None, 1, -1, 0, 0]
        dist = {(0, 0): 0}
        queue = SortedList([(0, 0, 0)])

        while queue:
            c, i, j = queue.pop(0)
            if i == len(grid) - 1 and j == len(grid[0]) - 1:
                return c
            for k in [1, 2, 3, 4]:
                m = i + dirs_x[k]
                n = j + dirs_y[k]
                if 0 <= m < len(grid) and 0 <= n < len(grid[0]):
                    dp = c + (1 if grid[i][j] != k else 0)
                    if (m, n) not in dist or dp < dist[m, n]:
                        dist[m, n] = dp
                        queue.add((dp, m, n))
        return 0
