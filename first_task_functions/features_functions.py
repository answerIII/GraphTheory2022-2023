from collections import deque

def build_vertex_adjacency(data, is_dvudol): #Вычисление долей вершин, по спискам смежности
    AllVertex = {}
    LeftVertex, RightVertex = set(), set()

    for index, row in data.iterrows():
        if is_dvudol:
            LeftVertex.add(row['in'])
            RightVertex.add(row['out'])
        
        source_vertex = row['in']
        target_vertex = row['out']

        if source_vertex == target_vertex:
            continue

        # Обработка левой вершины
        left_neighbors = AllVertex.get(source_vertex, [])
        if target_vertex not in left_neighbors:
            left_neighbors.append(target_vertex)
            AllVertex[source_vertex] = left_neighbors

        # Обработка правой вершины
        right_neighbors = AllVertex.get(target_vertex, [])
        if source_vertex not in right_neighbors:
            right_neighbors.append(source_vertex)
            AllVertex[target_vertex] = right_neighbors

    return AllVertex, LeftVertex, RightVertex
        
def calculate_edge_count(AllVertex): # Вычисление кол-ва ребер
    count = 0
    for vertex_neighbors in AllVertex.values():
        count += len(vertex_neighbors)
    return count / 2

def calculate_density(M, LeftVertex, RightVertex, countVertex): #Вычисление плотности графа
    if LeftVertex and RightVertex:
        density = M / (len(RightVertex) * len(LeftVertex))
    else:
        density = M / (countVertex * (countVertex - 1) * 0.5)
    return density

def depth_first_search(AllVertex, vertex, visited, component): #DFS
    visited.add(vertex)
    component.append(vertex)
    neighbors = AllVertex.get(vertex, [])
    
    for neighbor in neighbors:
        if neighbor not in visited:
            depth_first_search(AllVertex, neighbor, visited, component)

def find_weak_components(AllVertex, countVertex): #Вычисление компонент слабой связности
    visited = set()
    components = []

    for vertex in AllVertex:
        if len(visited) == countVertex:
            break
        if vertex not in visited:
            component = []
            depth_first_search(AllVertex, vertex, visited, component)
            components.append(component)
    
    return components

def calculate_largest_component_ratio(components, countVertex): #Доля вершин в максимальной по мощности компоненте слабой связности
    largest_component = max(components, key=len)
    ratio = len(largest_component) / countVertex
    return ratio

def bfs_for_snow_subgraph(start_vertex, AllVertex):
    # Ищем подграф с помощью обхода в ширину (BFS)
    subgraph = []
    queue = deque()
    queue.extend(start_vertex)
    visited = set()

    while len(queue) > 0 and len(subgraph) < 750:
        current_vertex = queue.popleft()
        subgraph.append(current_vertex)
        neighbors = AllVertex.get(current_vertex)

        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

    return subgraph