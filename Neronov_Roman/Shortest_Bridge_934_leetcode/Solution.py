
class Solution:
    
    def shortestBridge(self, grid: List[List[int]]) -> int:
        
        def DFS(x: int, y: int, rows: int, cols: int, grid: List[List[int]], 
            visited: List[List[int]], island_list: List[List[int]]) -> None:
            visited[x][y] = 1 # отметка о посещении вершины
            island_list.extend([(x, y, 0)])# добавляем вершину одного из островов
            directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
            
            # Поиск вершин из того же острова
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < rows and 0 <= new_y < cols and visited[new_x][new_y] == 0 and grid[new_x][new_y] == 1:
                    DFS(new_x, new_y, rows, cols, grid, visited, island_list)

        rows = len(grid)
        cols = len(grid[0])
        visited = [0 for _ in range(cols)]
        visited = [visited[:] for _ in range(rows)]

        island_list = []
        min_distance = float('inf')

        # находим первую вершину,принадлежащую какому-нибудь острову
        for i in range(rows):
            for j in range(cols):
                if visited[i][j] == 0 and grid[i][j] == 1:
                    DFS(i, j, rows, cols, grid, visited, island_list)
                    break
            else:
                continue
            break
        
        # Для каждой вершины из одного острова проводим распространение по всем направлениям
        # до тех пор пока не найдем вершину из другого острова
        while island_list:
            x, y, d = island_list.pop(0)
            directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy # выбираем одно из направлений
                if 0 <= new_x < rows and 0 <= new_y < cols and visited[new_x][new_y] == 0:
                    if grid[new_x][new_y] == 1: # нашли вершину другого острова
                        min_distance = min(min_distance, d)
                        # удаляем участки, которые заведомо не дадут лучше результат
                        island_list = [sector for sector in island_list if sector[2] < min_distance]

                    else: # неостровная вершина
                        island_list.extend([(new_x, new_y, d + 1)])
                        visited[new_x][new_y] = 1
        return min_distance
