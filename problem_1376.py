class Solution:

    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        def makeDict(mng: list, infTm: list) -> dict:
            new_dict = dict()
            for i, val in enumerate(mng):
                if val in new_dict.keys():
                    new_dict[val].append((i, infTm[i]))
                else:
                    new_dict[val] = [(i, infTm[i]), ]
            return new_dict
        

        def maxWay(G: dict, curr_nodes: list, ) -> int:
            visited = dict()
            while curr_nodes:
                u, time = curr_nodes.pop()

                if u in visited:
                    continue
                
                visited[u] = time
                
                if u in G.keys():
                    for v, way_time in G[u]:
                        if v in visited:
                            continue
                        curr_nodes.append((v, time + way_time))
            
            return max(visited.values())
        
        G = makeDict(manager, informTime)
        curr_nodes = [(headID, informTime[headID])]
        return maxWay(G, curr_nodes)