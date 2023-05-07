class Solution(object):
    def __init__(self):
        self.childs = dict({})
        self.ancestors = []
    def dfs(self, ancestor, node):
        if node in self.childs:
            for child in self.childs[node]: #DFS-ом будем передавать предка 
                if ancestor not in self.ancestors[child]:
                    self.ancestors[child].append(ancestor)
                    self.dfs(ancestor, child)
    
    
    def getAncestors(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: List[List[int]]
        """
        # будем для каждого родителя хранить детей
        for parent, child in edges:
            if parent in self.childs:
                self.childs[parent].append(child)
            else:
                self.childs[parent] = []
                self.childs[parent].append(child)

        self.ancestors = [[] for i in range(n)]

        for i in range(n):
            self.dfs(i,i)
        
        return self.ancestors
