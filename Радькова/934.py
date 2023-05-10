class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        N = len(grid)
        directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        visited = set()

        # check whether staying on grid or not
        def offbounds(row, col):
            return row < 0 or col < 0 or row == N or col == N

        # use dfs idea to find one of the islands
        def dfs(row, col):
            if offbounds(row, col) or not grid[row][col] or (row, col) in visited:
                return

            # we add only if it's land
            visited.add((row, col))

            # run dfs to find adjacent pieces of land
            for drow, dcol in directions:
                dfs(row + drow, col + dcol)

        def bfs():
            res = 0  # store shortest path info
            Q = list(visited)  # standard bfs queue but we're making bfs from all island 1's

            while Q:
                qlen = len(Q)

                for i in range(qlen):
                    row, col = Q.pop(0)

                    for drow, dcol in directions:
                        cRow = row + drow
                        cCol = col + dcol

                        if offbounds(cRow, cCol) or (cRow, cCol) in visited:
                            continue
                        if grid[cRow][cCol]:
                            return res

                        Q.append((cRow, cCol))
                        visited.add((cRow, cCol))

                res += 1

        for rows in range(N):
            for cols in range(N):
                if grid[rows][cols]:
                    dfs(rows, cols)

                    return bfs()
