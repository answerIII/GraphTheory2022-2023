class Solution:
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        rows_grid = len(grid)-1
        cols_grid = len(grid[0])-1
        # Куча нужна для эффективного извлечения минимального по стоимости подпути,
        # чтобы быстрее получить конечный минимальный путь без окончания всех возможных вариантов
        heap = [[0,0,0]] # стартовая точка
        while heap:
            cost,row,col = heapq.heappop(heap)
            
            if grid[row][col]==-1: # уже были в этой точке
                continue

            grid[row][col] = -1
           
            if row==rows_grid and col==cols_grid: # пришли в конечную точку
                return cost # возвращаемый путь будет минимальной стоимости, т к до этого брался подпуть минимальной стоимости
            
            for next_row,next_col in ((row+1,col),(row-1,col),(row,col+1),(row,col-1)):
                if 0<=next_row<=rows_grid and 0<=next_col<=cols_grid:
                    if grid[next_row][next_col] != -1:
                      heapq.heappush(heap,[cost+grid[next_row][next_col],next_row,next_col])
        return -1
