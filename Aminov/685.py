class Solution:
    def find_parents(self, edges: List[List[int]]):
        for node1, node2 in edges:
            if node2 in self.parents:
                self.additional = node1, node2
            else:
                self.parents[node2] = node1

    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[
        int]:
        self.parents = {}
        self.additional = None

        self.find_parents(edges)

        if self.additional:
            node = self.parents[self.additional[1]]
            while node in self.parents and node != self.additional[1]:
                node = self.parents[node]
            if node in self.parents:
                return self.parents[self.additional[1]], self.additional[1]
            else:
                return self.additional

        node = 1
        visited = {}
        path = []

        while node not in visited:
            visited[node] = len(path)
            path.append(node)
            node = self.parents[node]

        for node in path[:visited[node]]:
            del visited[node]

        for node1, node2 in edges[::-1]:
            if node1 in visited and node2 in visited:
                return node1, node2