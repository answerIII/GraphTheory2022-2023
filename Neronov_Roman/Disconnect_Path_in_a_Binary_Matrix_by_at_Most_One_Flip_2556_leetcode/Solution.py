class Solution:
    def isPossibleToCutPath(self, grid: List[List[int]]) -> bool: 

        row = len(grid)
        col = len(grid[0])
      
        if row==1:
          if col<=2:
            return False
          else:
            return True
        if col==1:
          if row==2:
            return False
          else:
            return True
        
        def DFS(i=0,j=0):
            if i == row-1 and j == col-1: # добрались до конца
                return True
            
            grid[i][j]=0 # помечаем пройденную клетку, чтобы через нее не ходить
           
            if i != 0 or j != 0: # не стартовая точка
              
                if i+1<row and grid[i+1][j]!=0: # не ушли за границу и след клетка не 0
                  # сделаем обход в глубину, если нашелся путь возвращаем True, иначе
                  # делаем другой шаг и новый обход в глубину
                  if DFS(i+1, j): 
                    return True
                if j+1<col and grid[i][j+1]!=0: # не ушли за границу и след клетка не 0
                  return DFS(i, j+1)
                return False

            # отрабатывает для стартовой вершины для проверки существования двух путей
            return not(DFS(i+1, j) and DFS(i, j+1))
            
        return DFS(0,0)
            
