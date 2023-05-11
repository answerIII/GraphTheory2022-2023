from queue import Queue

class Solution:
    def gardenNoAdj(self, n: int, paths: List[List[int]]) -> List[int]: 
        ver = defaultdict(list)
        for k, v in paths:
            ver[k].append(v)
            ver[v].append(k)
        
        q = Queue()
        q.put(1) 

        color = [0] * (n + 1)
        color[0] = 500 

        color_neigh = [False] * (n + 1) 
        color_neigh[0] = True 

        while 0 in color: 
            if q.empty: 
                curr_v = color.index(0) 
            else:
                curr_v = q.get() 

            if color[curr_v] > 0: continue

            for j in ver[curr_v]: 
                if color[j] == 0:
                    q.put(j) 
                else:
                    color_neigh[color[j]] = True 
            color[curr_v] = color_neigh.index(False) 
            color_neigh = [False] * (n+1)
            color_neigh[0] = True 
        
        return color[1:] 
