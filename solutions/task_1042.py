import collections

class Solution(object):
    def gardenNoAdj(self, n, paths):
        """
        :type n: int
        :type paths: List[List[int]]
        :rtype: List[int]
        """
        neighbors = [[] for i in range(n)]

        for x,y in paths: 
            neighbors[x-1].append(y-1)
            neighbors[y-1].append(x-1)

        colours = [0] * n
        max_colours = {1, 2, 3, 4}

        for i in range(n):
            colours[i] =  min(max_colours - {colours[j] for j in neighbors[i]})

        return(colours)

