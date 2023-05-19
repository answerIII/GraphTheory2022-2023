import networkx as nx

#f = open('datasets\out.radoslaw_email_email', 'r')
f = open('datasets\out.opsahl-ucsocial', 'r') 
#f = open('datasets\out.soc-sign-bitcoinalpha.txt', 'r')
#f = open('datasets\out.munmun_digg_reply', 'r')
#f = open('datasets\out.sx-mathoverflow', 'r')
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

#print("Vertexes:" , uniqueVertexes)
V = len(uniqueVertexes) + 1

adjList = [[] for _ in range(V)]

# transform directed graph to undirected
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    adjList[from_ind].append([to_ind, 1, 1])
    adjList[to_ind].append([from_ind, 1, 1])

# delete duplicate edges
for i in range(V):
    set_tuples = {tuple(a_list) for a_list in adjList[i]}
    adjList[i] = list(set_tuples)

# for i in range(V):
#     print(i, ":", end=" ")
#     print(adjList[i])

sum_E = 0
for _set in adjList:
    sum_E+=len(_set)
E = sum_E // 2

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


### 1.3. Посчитать средний кластерный коэффициент для наибольшей КСС

def local_clustering_coefficient(adjList, u):
    #print("u =", u, end=": ")

    # сет соседей вершины u
    adj2u_set = set()
    for v_tuple in adjList[u]:
        to = v_tuple[0]
        adj2u_set.add(to)

    gamma_u = len(adj2u_set)
    #print("length of adj2u =", gamma_u, end=", ")
    if (gamma_u < 2):
        #print("Only one adj node => Return 0")
        return 0

    L_u = countEdgesInSet(adjList, adj2u_set)

    #print("L_u =", L_u, end=", ")

    Cl_u = 2 * L_u / (gamma_u * (gamma_u - 1))

    #print("Cl_u =", Cl_u)

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


### 1.4. Посчитать коэффициент ассортативности по степени вершин
### Использовался алгоритм из данного видео https://www.youtube.com/watch?v=gzWlSPxpHZE&t=191s

def pearson_correlation_coefficient_by_degree(adjList, edge_list):
    X = []
    Y = []
    
    for edge in edge_list:
        x = edge[0]
        y = edge[1]
        X.append(len(adjList[x]))
        Y.append(len(adjList[y]))
    
    avg_x = sum(X) / len(X)
    avg_y = sum(Y) / len(Y)

    XminusAvg_x = [k - avg_x for k in X]
    YminusAvg_y = [k - avg_y for k in Y]

    Z = [x * y for x, y in zip(XminusAvg_x, YminusAvg_y)]

    XminusAvg_x = [k - avg_x for k in X]
    YminusAvg_y = [k - avg_y for k in Y]

    sq_XminusAvg_x = [x ** 2 for x in XminusAvg_x]
    sq_YminusAvg_y = [y ** 2 for y in YminusAvg_y]

    sum_sq_x = sum(sq_XminusAvg_x)
    sum_sq_y = sum(sq_YminusAvg_y)
    sum_Z = sum(Z)

    if (sum_sq_x == 0 or sum_sq_y == 0):
        print("correlation coef is not defined!")
        return 0

    # for i in range(len(edge_list)):
    #     print(edge_list[i], ":", X[i], Y[i], XminusAvg_x[i], YminusAvg_y[i], Z[i], sep="  ")
    #print(sum_sq_x, sum_sq_y, sum_Z)

    r = sum_Z / ((sum_sq_x * sum_sq_y) ** 0.5)

    return r

# считываем из датасета список ребер, игнорируя их направленность и дубликаты (вес и время тоже игнорируем)
edge_list = set()
for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    edge_list.add((from_ind, to_ind))
    edge_list.add((to_ind, from_ind))

#print("edge_list:", edge_list)

# Сравнение результатов с алгоритмом из библиотеки networkx
my_r = pearson_correlation_coefficient_by_degree(adjList, edge_list)
print("my_pearson_correlation_coefficient_by_degree:", my_r)

G = nx.Graph(edge_list)
nx_r = nx.degree_pearson_correlation_coefficient(G)
print("nx_pearson_correlation_coef: ", nx_r)

print("error: ", abs(nx_r - my_r))







f.close()