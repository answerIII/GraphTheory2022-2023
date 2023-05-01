class Solution:
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        res = 0
        seen  = set()
        neighbors = collections.defaultdict(set)

        for x,y in edges: 
            neighbors[x].add(y)
            neighbors[y].add(x)

        def dfs(i,t_i, probability):
            nonlocal res
            print(i, t_i, probability)
            if t_i >= t:
                if i == target:
                    res = probability
                print("return")
                return
            seen.add(i)
            neighbors[i] = neighbors[i] - seen

            for n in neighbors[i] or [i]:
                dfs(n, t_i + 1, probability / (len(neighbors[i]) or 1) )

        dfs(1,0,1)        
        return res