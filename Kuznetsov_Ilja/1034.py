from collections import deque
from copy import deepcopy
from typing import List

def get(matrix, x, y):
    return matrix[x][y]

def set_(matrix, x, y, val):
    matrix[x][y] = val

class Solution:
    def colorBorder(self, grid: List[List[int]], row: int, col: int, color: int) -> List[List[int]]:
        output_grid = deepcopy(grid)
        comp_color = grid[row][col]
        
        rows, cols = len(grid), len(grid[0])
        padding = [[-1] * (cols + 2)]
        grid = padding + [[-1] + row + [-1] for row in grid] + padding
        visited = [[False] * (cols + 2) for _ in range(rows + 2)]
        set_(visited, row + 1, col + 1, True)
        
        queue = deque([(row + 1, col + 1)])
        while queue:
            cur_row, cur_col = queue.popleft()
            neighbors = [
                (cur_row + 1, cur_col),
                (cur_row, cur_col + 1),
                (cur_row - 1, cur_col),
                (cur_row, cur_col - 1),
            ]
            
            for neighbor in neighbors:
                neigbor_color = get(grid, *neighbor)
                if neigbor_color == comp_color and not get(visited, *neighbor):
                    queue.append(neighbor)
                    set_(visited, *neighbor, True)
                elif neigbor_color != comp_color:
                    set_(output_grid, cur_row - 1, cur_col - 1, color)
        
        return output_grid
