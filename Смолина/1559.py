def bfs(grid, i, j, visited):
    q = [[i, j, -1, -1]]
    symbol = grid[i][j]
    while len(q) != 0:
        pos = q[0]
        q.pop(0)
        current_i, current_j, parent_i, parent_j = pos[0], pos[1], pos[2], pos[3]
        
        if visited[current_i][current_j]:
            return True
        visited[current_i][current_j] = True

        if current_i - 1 >= 0 and grid[current_i - 1][current_j] == symbol and not (current_i -1 == parent_i and current_j == parent_j):
            q.append([current_i - 1, current_j, current_i, current_j])

        if current_i + 1 < len(grid) and grid[current_i + 1][current_j] == symbol and not(current_j == parent_j and current_i + 1 == parent_i):
            q.append([current_i + 1, current_j, current_i, current_j])

        if current_j - 1 >= 0 and grid[current_i][current_j - 1] == symbol and not (current_j - 1 == parent_j and current_i == parent_i):
            q.append([current_i, current_j - 1, current_i, current_j])

        if current_j + 1 < len(grid[0]) and grid[current_i][current_j + 1] == symbol and not (current_j + 1 == parent_j and current_i == parent_i):
            q.append([current_i, current_j + 1, current_i, current_j])

    return False


class Solution(object):

    def containsCycle(self, grid):
        rows = len(grid)
        cols = len(grid[0])
        visited = [[False] * cols for i in range(rows)]
        for i in range(0, rows):
            for j in range(0, cols):
                if visited[i][j]:
                    continue
                b=bfs(grid, i, j, visited)
                if b:
                    return True

        return False
