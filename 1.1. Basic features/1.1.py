
f = open('datasets\out.prosper-loans.txt', 'r')
#f = open('datasets\small-graph.txt', 'r') 


def bfs(adjList, unvisited):
    WCC = set()  # weakly connected component
    queue = list()  # queue<int>
    
    src_node = unvisited.pop()
    queue.append(src_node)
    
    # loop until the queue is empty
    while queue:
        # pop the front node of the queue and add it to WCC
        current_node = queue.pop(0)
        WCC.add(current_node)
        
        # check all the neighbour nodes of the current node
        for neighbour_node in adjList[current_node]:
            to = neighbour_node[0] # neighbour_node - это tuple(to, weight, time)
            if to in unvisited:
                unvisited.remove(to)
                queue.append(to)

    return WCC


dataset = f.readlines()

# count number of vertexes
uniqueVertexes = set()

for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    uniqueVertexes.add(from_ind)
    uniqueVertexes.add(to_ind)

#print("Vertexes:" , uniqueVertexes)
V = len(uniqueVertexes) + 1

adjList = [[] for _ in range(V)]
#print(adjList)

# transform directed graph to undirected
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    adjList[from_ind].append([to_ind, weight, time])
    adjList[to_ind].append([from_ind, weight, time])

#print(adjList)

for i in range(V):
    set_tuples = {tuple(a_list) for a_list in adjList[i]}
    adjList[i] = list(set_tuples)

# for i in range(V):
#     print(i, ":", end=" ")
#     print(adjList[i])

sum = 0
for _set in adjList:
    sum+=len(_set)
E = sum // 2

# print answer
print("Number of vertexes:", V - 1)
print("Number of edges:", E)

# максимальное число ребер в полном графе с количеством вершин V - 1
max_E = (V - 1)*(V - 2) // 2

print("Density:", E / max_E)

count = 0
max_size = 0
max_WCC = set()
while len(uniqueVertexes) > 0:
    WCC = bfs(adjList, uniqueVertexes)
    size = len(WCC)
    if size > max_size:
        max_size = size
        max_WCC = WCC
    count += 1
    #print("WCC", count, "size", size, ":", WCC)

print("Количество компонент слабой связности: ", count)
#print("Наибольшая КСС: ", max_WCC)
print("Мощность наибольшей КСС: ", max_size)
print("Отношение мощности наибольшей КСС к общему количеству вершин: ", max_size / (V - 1))

f.close()