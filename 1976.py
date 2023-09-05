import heapq

def numWays(n, roads):
    MOD = 10**9 + 7
    graph = [[] for _ in range(n)]
    
    for u, v, time in roads:
        graph[u].append((v, time))
        graph[v].append((u, time))
    
    min_time = [float('inf')] * n
    min_time[0] = 0
    
    ways_count = [0] * n
    ways_count[0] = 1
    min_heap = [(0, 0)] 
    
    while min_heap:
        time, node = heapq.heappop(min_heap)
        
        if time > min_time[node]:
            continue
        
        for neighbor, road_time in graph[node]:
            if min_time[neighbor] > time + road_time:
                min_time[neighbor] = time + road_time
                ways_count[neighbor] = ways_count[node]
                heapq.heappush(min_heap, (min_time[neighbor], neighbor))
            elif min_time[neighbor] == time + road_time:
                ways_count[neighbor] = (ways_count[neighbor] + ways_count[node]) % MOD
    
    return ways_count[-1] % MOD


n = 7
roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]
result = numWays(n, roads)
print(result) #4