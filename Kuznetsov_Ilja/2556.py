from copy import deepcopy
from typing import List

class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool:
        grid = deepcopy(grid)
        
        return not ( Solution.findAndErasePath(grid) and Solution.findAndErasePath(grid) )
    
    @staticmethod
    def findAndErasePath(grid: List[List[int]], from_row: int = 0, from_col: int = 0) -> bool:
        # returns True if found path
        if from_row == len(grid) - 1 and from_col == len(grid[0]) - 1 and grid[-1][-1]:
            return 1
        
        if from_row >= len(grid) or from_col >= len(grid[0]) or not grid[from_row][from_col]:
            return 0
        
        if from_row or from_col:
            grid[from_row][from_col] = 0
        
        return Solution.findAndErasePath(grid, from_row + 1, from_col) or \
               Solution.findAndErasePath(grid, from_row, from_col + 1)
