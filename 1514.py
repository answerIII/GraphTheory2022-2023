import heapq

def maxProbability(n, edges, succProb, start_node, end_node):
    graph = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        graph[a].append((b, succProb[i]))
        graph[b].append((a, succProb[i]))
    
    probability = [0.0] * n
    probability[start_node] = 1.0
    

    pq = [(-1.0, start_node)]
    
    while pq:
        prob, node = heapq.heappop(pq)
        prob = -prob  
        
        if prob < probability[node]:
            continue
        
        for neighbor, edge_prob in graph[node]:
            new_prob = prob * edge_prob
            if new_prob > probability[neighbor]:
                probability[neighbor] = new_prob
                heapq.heappush(pq, (-new_prob, neighbor))
    
    return probability[end_node]

# Для решения используем измененный алгоритм Дейкстры :
n = 4
edges = [[0,1],[1,2],[0,2]]
succProb = [0.5,0.5,0.2]
start = 0
end = 3

result = maxProbability(n, edges, succProb, start, end)
print(result)  #0.25