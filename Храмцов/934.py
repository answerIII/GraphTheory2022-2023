class Solution(object):
    def shortestBridge(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        ans = -1

        moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        n = len(grid)

        queue = []
        for i in range(n):
            for j in range(n):
                if (grid[i][j] == 1):
                    queue.append((i, j))
                    break
            if (len(queue) > 0):
                break

        island = set()
        checked = set()

        while len(queue) > 0:
            u = queue.pop(0)
            island.add(u)
            for move in moves:
                cell = (u[0]+move[0], u[1]+move[1])
                if cell not in checked and (cell[0] >= 0 and cell[0] < n and cell[1] >= 0 and cell[1] < n):
                    checked.add(cell)
                    if grid[cell[0]][cell[1]] == 1 and cell not in island:
                        queue.append(cell)

        queue = []
        queue_next = []

        visited = set()

        for cell in island:
            queue_next.append(cell)

        for i in range(n):
            queue = queue_next
            queue_next = []
            ans += 1
            while len(queue) > 0:
                u = queue.pop(0)
                for move in moves:
                    cell = (u[0]+move[0], u[1]+move[1])
                    if cell not in visited:
                        visited.add(cell)
                        if (cell[0] >= 0 and cell[0] < n and cell[1] >= 0 and cell[1] < n):
                            if grid[cell[0]][cell[1]] == 1 and cell not in island:
                                return (ans)
                            if grid[cell[0]][cell[1]] == 0 and cell not in queue:
                                queue_next.append(cell)

        return False
