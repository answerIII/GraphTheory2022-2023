class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        distances = [[inf] * n for _ in range(m)]
        need_to_visit = [(grid[0][0], 0, 0)]

        while(need_to_visit):
            cell, row, col = heappop(need_to_visit)
            if (row, col) == (m - 1, n - 1):
                return cell
            for i, j in (row + 1, col), (row, col + 1), (row - 1, col), (row, col - 1):
                if m > i >= 0 and 0 <= j < n and grid[i][j] + cell < distances[i][j]:
                    distances[i][j] = grid[i][j] + cell
                    heappush(need_to_visit, (distances[i][j], i, j))
