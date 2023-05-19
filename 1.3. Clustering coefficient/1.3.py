f = open('datasets/small-graph.txt', 'r')
#f = open('datasets\out.prosper-loans.txt', 'r') 


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

print("Vertexes:" , uniqueVertexes)
V = len(uniqueVertexes) + 1

adjList = [[] for _ in range(V)]

# transform directed graph to undirected
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    adjList[from_ind].append([to_ind, weight, time])
    adjList[to_ind].append([from_ind, weight, time])

# delete duplicate edges
for i in range(V):
    set_tuples = {tuple(a_list) for a_list in adjList[i]}
    adjList[i] = list(set_tuples)

for i in range(V):
    print(i, ":", end=" ")
    print(adjList[i])

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
    print("WCC", count, "size", size, ":", WCC)

print("Количество компонент слабой связности: ", count)
print("Наибольшая КСС: ", max_WCC)
print("Мощность наибольшей КСС: ", max_size)
print("Отношение мощности наибольшей КСС к общему количеству вершин: ", max_size / (V - 1))


### 1.3. Посчитать средний кластерный коэффициент для наибольшей КСС

def local_clustering_coefficient(adjList, u):
    print("u =", u, end=": ")

    # сет соседей вершины u
    adj2u_set = set()
    for v_tuple in adjList[u]:
        to = v_tuple[0]
        adj2u_set.add(to)

    gamma_u = len(adj2u_set)
    print("length of adj2u =", gamma_u, end=", ")
    if (gamma_u < 2):
        print("Only one adj node => Return 0")
        return 0

    L_u = countEdgesInSet(adjList, adj2u_set)

    print("L_u =", L_u, end=", ")

    Cl_u = 2 * L_u / (gamma_u * (gamma_u - 1))

    print("Cl_u =", Cl_u)

    return Cl_u

# считает количество ребер между вершинами в сете
def countEdgesInSet(adjList, vertexes_set):
    sum = 0
    for node in vertexes_set:
        for neighbour_node in adjList[node]:
            to = neighbour_node[0] # neighbour_node - это tuple(to, weight, time)
            if to in vertexes_set:
                sum+=1
    return sum // 2

sum_Cl = 0
for vertex in max_WCC:
    sum_Cl+=local_clustering_coefficient(adjList, vertex)

average_Cl = sum_Cl / len(max_WCC)

print("Средний кластерный коэффициент для наибольшей КСС:", average_Cl)

f.close()