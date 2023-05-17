class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        from collections import deque
        m, n = len(grid), len(grid[0])
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        queue = deque([(0, 0, 0)])
        visited = set([(0, 0)])

        while queue:
            row, col, obstacles = queue.popleft()

            if (row, col) == (m - 1, n - 1):
                return obstacles

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc

                if (
                    0 <= new_row < m
                    and 0 <= new_col < n
                    and (new_row, new_col) not in visited
                ):
                    visited.add((new_row, new_col))

                    if grid[new_row][new_col] == 0:
                        queue.appendleft((new_row, new_col, obstacles))
                    else:
                        queue.append((new_row, new_col, obstacles + 1))
