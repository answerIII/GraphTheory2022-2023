class Solution:
    def hasValidPath(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: bool
        """
        next_step = {
            1: [[0, -1], [0, +1]],
            2: [[-1, 0], [+1, 0]],
            3: [[0, -1], [+1, 0]],
            4: [[0, +1], [+1, 0]],
            5: [[0, -1], [-1, 0]],
            6: [[0, +1], [-1, 0]],
        }
        BFS_queue = collections.deque([tuple((0, 0))])
        visited = {tuple((0,0))}
        n = len(grid) - 1
        m = len(grid[0]) - 1
        #цикл для BFS
        while(BFS_queue):
            current = BFS_queue.popleft()
            i = current[0]
            j = current[1]

            if(i == n and j == m): #достигли финальной точки
                return True

            for step in next_step[grid[i][j]]: #рассматриваем возможные дальнейшие пути
                new_i = i+step[0]
                new_j = j+step[1]

                if(new_i>=0 and new_i<=n and new_j>=0 and new_j<=m and [-step[0], -step[1]] in next_step[grid[new_i][new_j]]  and tuple((new_i, new_j)) not in visited):

                    BFS_queue.append(tuple((new_i, new_j))) 
                    visited.add(tuple((new_i, new_j)))


        return False
