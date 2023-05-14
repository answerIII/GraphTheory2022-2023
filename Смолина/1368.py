class Solution(object):
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        rows = len(grid)
        cols = len(grid[0])
        dxy = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        matrix_cost = [[False] * cols for i in range(rows)]
        matrix_cost[0][0] = 0
        visited = [[False] * cols for i in range(rows)]
        q = [[0, 0, 0]]


        while q:
            i, j, cost = q.pop(0)
            for d in dxy:
                if d == dxy[grid[i][j] - 1]:
                    curr_cost = 0
                else:
                    curr_cost = 1
                curr_x = i + d[0]
                curr_y = j + d[1]
                if curr_x >= 0 and curr_x < rows and curr_y >= 0 and curr_y < cols:
                    if visited[curr_x][curr_y] is not True and cost + curr_cost < matrix_cost[curr_x][curr_y] or matrix_cost[curr_x][curr_y] is False:
                        q.append([curr_x, curr_y, cost + curr_cost])
                        matrix_cost[curr_x][curr_y] = cost + curr_cost

        return matrix_cost[rows - 1][cols - 1]
