class Solution:
    def containsCycle(self, grid: List[List[str]]) -> bool:
        m = len(grid)
        n = len(grid[0])
        #сетка для отметок о посещенности и принадлежности к определенным группам
        tag_grid = [[0 for _ in range(n)] for _ in range(m)]
        #переменная ответа к задаче
        self.ans = False
        #в дфс отмечаем посещенные клетки и проверяем на принадлежность к текущему поиску
        def dfs(x, y, moove, letter, tag_value):
            if tag_grid[x][y] == tag_value:
                self.ans = True
                return
            tag_grid[x][y] = tag_value
            mooves = [i for i in [[1,0],[-1,0],[0,1],[0,-1]] if i not in [moove]]
            for dx,dy in mooves:
                dx+=x
                dy+=y
                if self.ans:
                    return
                if dx>=0 and dx < m and dy >= 0 and dy < n and grid[dx][dy] == letter: 
                    dfs(dx,dy, [-(dx-x),-(dy-y)], letter, tag_value)
            return
                
        tag_value = 1
        #запускаем дфс на всех непосещенных клетках
        for i in range(m):
            for j in range(n):
                if tag_grid[i][j] == 0:
                    dfs(i,j,[0,0],grid[i][j],tag_value)
                    tag_value+=1
        return self.ans
