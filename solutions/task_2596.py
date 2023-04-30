class Solution(object):
    def checkValidGrid(self, grid):
        """
        оооооо:0type grid: List[List[int]]
        :rtype: bool
        """
        if grid[0][0]:
          return False

        curr = (0,0)
        count = 0 # счетчик 
        n = len(grid)

        steps_x = (-2,-2,2,2, -1,-1,1,1)
        steps_y = (-1,1,-1,1,-2,2,-2,2)
        print(steps_x[0]) 
        for count in range (1, n**2):
          for j in range(8):
            x,y = steps_x[j]+curr[0],steps_y[j]+curr[1]
            if 0 <= x < n and 0 <= y < n and grid[x][y] == count:
              curr = (x,y)
              break
          else:
            return False
          
        return True