class Solution:
    def gardenNoAdj(self, n: int, paths: List[List[int]]) -> List[int]:
        def makeGraph(paths: List[List]) -> dict:
            G = collections.defaultdict(list)
            for u, v in paths:
                G[u].append(v)
                G[v].append(u)
            return G
        
        graph = makeGraph(paths)
        flowers = [0]*(n+1)
        for v in range(1, n+1):
            flower_in_garden = {1, 2, 3, 4}
            for u in graph[v]:
                flower_in_garden -= {flowers[u]} 
            flowers[v] = flower_in_garden.pop()
        flowers.pop(0)
        return flowers