class Solution:
    def minimumTime(self, grid: List[List[int]]) -> int:
        if grid[0][1] > 1 and grid[1][0] > 1:
            return -1

        curr_nodes = [(0, (0, 0))]
        available_moving = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        len_row = len(grid)
        len_col = len(grid[0])

        visited = [[False] * len_col for _ in range(len_row)]

        while curr_nodes:
            time, pos = heappop(curr_nodes)
            if (len_row - 1, len_col - 1) == pos:
                return time
            
            if visited[pos[0]][pos[1]]:
                continue
            
            visited[pos[0]][pos[1]] = True

            for r, c in available_moving:
                c_r, c_c = pos
                if not (0 <= r + c_r < len_row and 0 <= c + c_c < len_col) or visited[r + c_r][c + c_c]:
                    continue
                w = (grid[r + c_r][c + c_c] - time) % 2 == 0
                if grid[r + c_r][c + c_c] + w > time + 1:
                    heappush(curr_nodes, (grid[r + c_r][c + c_c] + w, (r + c_r, c + c_c)))
                else:
                    heappush(curr_nodes, ((time + 1, (r + c_r, c + c_c))))
        
        return -1