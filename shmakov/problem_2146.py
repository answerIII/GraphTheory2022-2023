class Solution(object):
    def highestRankedKItems(self, grid, pricing, start, k):
        """
        :type grid: List[List[int]]
        :type pricing: List[int]
        :type start: List[int]
        :type k: int
        :rtype: List[List[int]]
        """
        # размеры сетки
        m = len(grid) 
        n = len(grid[0])
        # границы интервала цены
        low = pricing[0]
        high = pricing[1]
        visited = set() # множество посещенных вершин
        visited.add((start[0], start[1])) # стартовая вершина считается посещенной
        row = start[0]
        col = start[1]
        answers = [] # множество подходящих вершин
        running_list = deque([(0, grid[row][col], row, col)]) # двусторонняя очередь для перебора вершин

        while running_list: # пока в очереди что-то есть...
            distance, cost, row, col = running_list.popleft() # достаем информацию о рассматриваемой вершине
            if low <= cost <= high: # если цена нам подходит
                answers.append((distance, cost, row, col)) # наша вершина может нам подходить
            
            for x, y in (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1): # перебираем соседей по четырем напрвлениям
                if 0 <= x <= m-1 and 0 <= y <= n-1 and (x, y) not in visited and grid[x][y] != 0: # если сосед в пределах сетки и он не стена
                    running_list.append((distance + 1, grid[x][y], x, y))
                    visited.add((x, y))
        
        answers = sorted(answers)
        # вернем k элементов, в отсортированном списке, согласно условию
        return [[x, y] for _, _, x, y in answers[:k]]
