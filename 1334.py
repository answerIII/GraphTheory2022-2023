class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:

        previus_weights=[[100000] * n for i in range(n)]
        for i in range(n):
            previus_weights[i][i] = 0

        for edge in edges:
            previus_weights[edge[0]][edge[1]] = edge[2]
            previus_weights[edge[1]][edge[0]] = edge[2]

        for k in range(n):
            current_weights=[[100000] * n for i in range(n)]
            for i in range(n):
                current_weights[i][i] = 0
            for i in range(n):
                for j in range(n):
                    current_weights[i][j] = min(previus_weights[i][j], \
                        previus_weights[i][k] + previus_weights[k][j])
            previus_weights = current_weights
        
        result = 0
        neighbours_count = 10000000
        for i in range(n):
            count = 0
            for j in range(n):
                if previus_weights[i][j] <= distanceThreshold and i != j:
                    count+=1
            if count <= neighbours_count:
                result = i
                neighbours_count = count
        return result
