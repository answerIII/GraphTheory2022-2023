class Solution:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]: 
        ver = defaultdict(list) 
        out = defaultdict(int) 
        in_v = defaultdict(int) 
        for k, v in pairs:
            ver[k].append(v) 
            out[k] += 1 
            in_v[v] += 1

        curr_v = pairs[0][0] 

        for i in out:
            if out[i] - in_v[i] == 1:
                curr_v = i 

        # if len(k) == 0:
        #     curr_v = pairs[0][0] 
        # else: 
        #     curr_v = k[0]
        #     g = list(set(val).difference(ver.keys()))
        #     if len(g) > 0:
        #         ver[g[0]].append(k[0])
        path = [curr_v]
        res = [] 

        while len(path): 

            if len(ver[curr_v]) > 0: 
            
                neigh_v = ver[curr_v][0] 
                path.append(curr_v) 
                ver[curr_v].remove(neigh_v)
                last = curr_v
                curr_v = neigh_v 
                

            else: 
                res.append([path[-1], curr_v])
                curr_v = path[-1]
                path.pop()

        res.pop() 

        return res[::-1]
