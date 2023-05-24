import numpy as np 
import queue

def number_of_vertexes(dataset):
    uniqueVertexes = set()
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        uniqueVertexes.add(from_ind)
        uniqueVertexes.add(to_ind)
    return len(uniqueVertexes) + 1

def get_edgeList(dataset):
     edgeList = []
     for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        edgeList.append([from_ind, to_ind, time])
        edgeList.append([to_ind, from_ind, time])
     return edgeList



def prepare_data_all(dataset, s = 75, display_interm_results = False):
    """Выборка всех ребер, которые пока не существуют. Только для небольших графов. \n
        s - это номер процентиля (в каком отношении разделяем темпоральный граф)"""

    V = number_of_vertexes(dataset)
    edgeList = get_edgeList(dataset)

    time_list = [edge[2] for edge in edgeList]
    qs = np.percentile(time_list, s) # qs - s-й процентиль списка timestamp'ов
    t_min = min(time_list)
    t_max = max(time_list)
    if display_interm_results: print("time_list:", time_list)
    print("t_min:", t_min)
    print("t_max:", t_max)
    print("qs:", qs)


    adjList = [[] for _ in range(V)]
    # transform directed graph to undirected
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        if time <= qs:
            adjList[from_ind].append(to_ind)
            adjList[to_ind].append(from_ind)

    # delete duplicate edges
    for i in range(V):
        _set = set(adjList[i])
        adjList[i] = list(_set)
    


    adjM_till_qs = np.full((V, V), 0)
    adjM_after_qs = np.full((V, V), 0)
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        if time <= qs:
            adjM_till_qs[from_ind][to_ind] = 1
            adjM_till_qs[to_ind][from_ind] = 1
        else:
            adjM_after_qs[from_ind][to_ind] = 1
            adjM_after_qs[to_ind][from_ind] = 1


    edgeL_till_qs = []
    edgeL_after_qs = []
    for i in range(1, V):
        for j in range(i, V):
            if adjM_till_qs[i][j] == 1:
                edgeL_till_qs.append((i,j))
            if adjM_after_qs[i][j] == 1:
                edgeL_after_qs.append((i,j))

    edgeL_after_qs = [item for item in edgeL_after_qs if item not in edgeL_till_qs]

    if display_interm_results: print("edgeL_till_qs:", edgeL_till_qs)
    print("size of edgeL_till_qs:", len(edgeL_till_qs), end='\n\n')

    if display_interm_results: print("edgeL_after_qs:", edgeL_after_qs)
    print("size of edgeL_after_qs:", len(edgeL_after_qs), end='\n\n')


    all_possible_edges = []
    for i in range(1, V):
        for j in range(i + 1, V):
            all_possible_edges.append((i,j))


    if display_interm_results: print("all_possible_edges:", all_possible_edges)
    print("size of all_possible_edges:", len(all_possible_edges), end='\n\n')


    # это и есть список ребер, для которых нужно предсказать, появятся ли они во время qs < t < t_max
    nonexistent_edges = [item for item in all_possible_edges if item not in edgeL_till_qs]
    if display_interm_results: print("nonexistent_edges:", nonexistent_edges)
    print("size of nonexistent_edges:", len(nonexistent_edges), end='\n\n')


    y = [0] * len(nonexistent_edges)
    for i in range(len(nonexistent_edges)):
        if nonexistent_edges[i] in edgeL_after_qs:
            y[i] = 1


    # for i in range(len(nonexistent_edges)):
    #     print(i, ":", end=" ")
    #     print(nonexistent_edges[i], end=" ")
    #     print(y[i])



    return [V, adjList, nonexistent_edges, y]



def prepare_data_at_dist_2(dataset, s = 75, display_interm_results = False):
    
    def dijkstra_algo(adjList: list[list], start) -> list:
        min_queue = queue.PriorityQueue()
        distance = [np.inf] * V

        min_queue.put((0, start))
        distance[start] = 0
        
        while not min_queue.empty():
            u = min_queue.get()[1]
            for v in adjList[u]:
                weight = 1

                if distance[v] > distance[u] + weight:
                    distance[v] = distance[u] + weight
                    min_queue.put((distance[v], v))


        pairs_of_vertexes = [] # at distance = 2
        for i in range(start, V):
            if distance[i] == 2:
                pairs_of_vertexes.append((start, i))

            # print(i, ":", distance[i])

        # print(pairs_of_vertexes)
        # print()


        return pairs_of_vertexes
    
    V = number_of_vertexes(dataset)
    edgeList = get_edgeList(dataset)

    time_list = [edge[2] for edge in edgeList]
    qs = np.percentile(time_list, s) # qs - s-й процентиль списка timestamp'ов
    t_min = min(time_list)
    t_max = max(time_list)
    if display_interm_results: print("time_list:", time_list)
    print("t_min:", t_min)
    print("t_max:", t_max)
    print("qs:", qs)


    adjList = [[] for _ in range(V)]
    # transform directed graph to undirected
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        if time <= qs:
            adjList[from_ind].append(to_ind)
            adjList[to_ind].append(from_ind)

    # delete duplicate edges
    for i in range(V):
        _set = set(adjList[i])
        adjList[i] = list(_set)


    adjM_till_qs = np.full((V, V), 0)
    adjM_after_qs = np.full((V, V), 0)
    for line in dataset:
        [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
        if time <= qs:
            adjM_till_qs[from_ind][to_ind] = 1
            adjM_till_qs[to_ind][from_ind] = 1
        else:
            adjM_after_qs[from_ind][to_ind] = 1
            adjM_after_qs[to_ind][from_ind] = 1


    edgeL_till_qs = []
    edgeL_after_qs = []
    for i in range(1, V):
        for j in range(i, V):
            if adjM_till_qs[i][j] == 1:
                edgeL_till_qs.append((i,j))
            if adjM_after_qs[i][j] == 1:
                edgeL_after_qs.append((i,j))

    edgeL_after_qs = [item for item in edgeL_after_qs if item not in edgeL_till_qs]

    if display_interm_results: print("edgeL_till_qs:", edgeL_till_qs)
    print("size of edgeL_till_qs:", len(edgeL_till_qs), end='\n\n')

    if display_interm_results: print("edgeL_after_qs:", edgeL_after_qs)
    print("size of edgeL_after_qs:", len(edgeL_after_qs), end='\n\n')



    # Выборка пар вершин, расстояние между которыми равно 2
    # без симметричных ребер, так как граф неориентированный и статические метрики симметричные (то есть для ребер (u,v) и (v,u) значения метрик равны)
    pairs_at_dist_2 = [] # то же самое что all_possible_edges в функции prepare_data_all()
    for i in range(1, V):
        pairs_at_dist_2 += dijkstra_algo(adjList, i)

    if display_interm_results: print("pairs_at_dist_2:", pairs_at_dist_2)
    print("size of pairs_at_dist_2:", len(pairs_at_dist_2), end='\n\n')


    # это и есть список ребер, для которых нужно предсказать, появятся ли они во время qs < t < t_max
    nonexistent_edges = pairs_at_dist_2 + [item for item in edgeL_after_qs if item not in pairs_at_dist_2]
    if display_interm_results: print("nonexistent_edges:", nonexistent_edges)
    print("size of nonexistent_edges:", len(nonexistent_edges), end='\n\n')


    y = [0] * len(nonexistent_edges)
    for i in range(len(nonexistent_edges)):
        if nonexistent_edges[i] in edgeL_after_qs:
            y[i] = 1


    return [V, adjList, nonexistent_edges, y]




        


        