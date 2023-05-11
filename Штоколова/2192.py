class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:

        res = []
        for i in range(n):
            res.append([])
        
        if len(edges) == 0:
            return res

        edges.sort()

        num = [0]*n 
        j = 0
        for i in range(0, n): 
          num[i] = j
          while (j < len(edges) and edges[j][0] == i): 
            j += 1
          if edges[j-1][0] != i:
            num[i] = -1 

        def dfs(current_v: int, v:int):
          i = num[current_v]

          while i < len(edges) and edges[i][0] == current_v:
            neighbor_v = edges[i][1]
            size_v = len(res[neighbor_v]) - 1
            if size_v >= 0 and res[neighbor_v][size_v] != v:
              res[neighbor_v].append(v)
              if num[neighbor_v] != -1:
               dfs(neighbor_v, v)
            elif size_v < 0:
              res[neighbor_v].append(v)
        
              if num[neighbor_v] != -1:
                dfs(neighbor_v, v)
            i += 1
            
        for k in range(n):
          if num[k] != -1: #and not use[k]:
            dfs(k, k) 
          

        return res 
