class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        graph = []
        amount = len(bombs)

        for i in range(amount):
            graph.append([])
            for j in range(amount):
                if i != j and length(bombs[i], bombs[j]) <= bombs[i][2]:
                    graph[i].append(j)

        max_bomb = 1

        for i in range(amount):
            visited = [0] * amount 
            curr_amount = dfs(graph, i, visited)  
            if curr_amount > max_bomb:
                max_bomb = curr_amount

        return max_bomb   
    
def dfs(graph, curr, visited):
    in_count = 1
    if visited[curr] == 0:
        visited[curr] = 1
        for i in graph[curr]:
            in_count += dfs(graph, i, visited)
        return in_count
    return 0

def length(first, second):
        return sqrt((first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2)