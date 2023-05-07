
class Solution(object):
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        n = len(grid)
        m = len(grid[0])
        BFS_queue = collections.deque([(0, 0, 0)])
        min_cost = [[100*100 for j in range(m)] for i in range(n)]
        min_cost[0][0] = 0


        #задачу можно воспринимать как поиск длины кратчайшего пути из начальной в конечную точку, где ребра имеют вес либо 0, либо 1
        #для решения данной задачи используется алгоритм BFS 0-1
        #если от вершины a до вершины b можно дойти по пути, состоящему из рёбер веса 0, то кратчайшие расстояния до этих вершин совпадают
        #если в нашем графе оставить только 0-рёбра, то он распадётся на компоненты связности, в каждой из которых ответ одинаковый. 
        #если теперь вернуть 1-рёбра, и сказать, что эти рёбра соединяют не вершины, а компоненты связности, то мы сведём задачу к обычному BFS
        #чтобы решить исходную задачу, надо при посещении первой вершины из компоненты обойти всю компоненту, проставив во всех вершинах такой же ответ, как и у первой вершины. 
        #чтобы обойти всю компоненту, при посещении вершины нужно добавлять всех её непосещённых соседей по 0-рёбрам в начало очереди, чтобы обработать их раньше, чем следующие в очереди.
        while BFS_queue:
            x, y, cost = BFS_queue.popleft()

            if(x == n-1 and y == m-1):
                return cost
        
            if(x+1<n):
                new_x = x+1
                new_y = y
                step_cost = 0 if grid[x][y] == 3 else 1
                new_cost = cost + step_cost
                if(new_cost < min_cost[new_x][new_y]):
                    min_cost[new_x][new_y] = new_cost
                    if step_cost == 0:
                        BFS_queue.appendleft((new_x, new_y ,new_cost))
                    else:
                        BFS_queue.append((new_x, new_y ,new_cost))

            if(x>0):
                new_x = x-1
                new_y = y
                step_cost = 0 if grid[x][y] == 4 else 1
                new_cost = cost + step_cost
                if(new_cost<min_cost[new_x][new_y]):
                    min_cost[new_x][new_y] = new_cost
                    if step_cost == 0:
                        BFS_queue.appendleft((new_x, new_y ,new_cost))
                    else:
                        BFS_queue.append((new_x, new_y ,new_cost))
            if(y+1<m):
                new_x = x
                new_y = y+1
                step_cost = 0 if grid[x][y] == 1 else 1
                new_cost = cost + step_cost
                if(new_cost<min_cost[new_x][new_y]):
                    min_cost[new_x][new_y] = new_cost
                    if step_cost == 0:
                        BFS_queue.appendleft((new_x, new_y ,new_cost))
                    else:
                        BFS_queue.append((new_x, new_y ,new_cost))

            if(y>0):
                new_x = x
                new_y = y-1
                step_cost = 0 if grid[x][y] == 2 else 1
                new_cost = cost + step_cost
                if(new_cost<min_cost[new_x][new_y]):
                    min_cost[new_x][new_y] = new_cost
                    if step_cost == 0:
                        BFS_queue.appendleft((new_x, new_y ,new_cost))
                    else:
                        BFS_queue.append((new_x, new_y ,new_cost))
        
