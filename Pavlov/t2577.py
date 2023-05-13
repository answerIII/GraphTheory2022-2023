import heapq
from typing import List


class GridSolver:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.m = len(grid)
        self.n = len(grid[0])
        self.dirs = [0, 1, 0, -1, 0]

    def solve(self) -> int:
        if self.grid[0][1] > 1 and self.grid[1][0] > 1:
            return -1

        minHeap = [(0, 0, 0)]  # (time, row, col)
        seen = set((0, 0))

        while minHeap:
            time, row, col = heapq.heappop(minHeap)

            if row == self.m - 1 and col == self.n - 1:
                return time

            for k in range(4):
                next_row = row + self.dirs[k]
                next_col = col + self.dirs[k + 1]

                if (
                    not self._is_valid(next_row, next_col)
                    or (next_row, next_col) in seen
                ):
                    continue

                extra_wait = 1 if (self.grid[next_row][next_col] - time) % 2 == 0 else 0
                next_time = max(time + 1, self.grid[next_row][next_col] + extra_wait)
                heapq.heappush(minHeap, (next_time, next_row, next_col))
                seen.add((next_row, next_col))

        return -1

    def _is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < self.m and 0 <= col < self.n


class Solution:
    def minimumTime(self, grid: List[List[int]]) -> int:
        solver = GridSolver(grid)
        return solver.solve()
