import collections

class Solution(object):
    def getAncestors(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[List[int]]
        """
        parent = [[] for i in range(n)]
        children = collections.defaultdict(list)
        for i,j in edges:
            print(i,j)
            children[i].append(j)

        def dfs(i, curr):
            for ch in children[curr]:
                if not(i in parent[ch]):
                    parent[ch].append(i)
                    dfs(i, ch)
                    
        for i in range(n):
            dfs(i,i)
            
        print(children)
        return (parent) 