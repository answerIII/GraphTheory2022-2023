import random
import math
from collections import deque
from graph import Graph


# Count of vertices
def get_vertices_count(graph: Graph) -> int:
    return graph.number_of_vertices()

# Count of edges
def get_edges_count(graph: Graph) -> int:
    return graph.number_of_edges(without_multiplicity=True)

# Dencity
def get_dencity(graph: Graph) -> float:
    n = graph.number_of_vertices()
    m = graph.number_of_edges(without_multiplicity=True)

    return m / ( n * (n - 1) / 2)

# Count of components
def get_components_count(graph: Graph) -> int:
    return len(__get_components(graph))

# Proportion of vertices in the maximum power component
def get_percentage(graph: Graph) -> float:
    components = __get_components(graph)

    return __percent_of_vertices(components, graph)

# Radius, diameter and 90perc
def get_metrics(graph: Graph) -> dict:
    components = __get_components(graph)
    max_component = __find_max_component(components)

    return __get_distance_properties(max_component, graph)

# Average clustering coefficient
def get_avg_coeff(graph) -> float:
    components = __get_components(graph)
    max_component = __find_max_component(components)
    vertexId = max_component[0]

    return __average_clustering(graph, vertexId)

# Degree assortativity
def get_dg_assortativity(graph: Graph) -> float:
    return __degree_assortativity(graph)


############################################################################################


# BFS for searching component from v
# returns size of component and removes visited vertices from set of not_visited
# WARNING: changes (not_visited)
def __bfs_search_component(graph: Graph, v: int, not_visited: set) -> int:
    count = 0
    q = deque()
    q.append(v)

    while (len(q) != 0):
        v = q.popleft()
        count += 1
        adj = graph.adj(v)

        for node in adj:
            if (node in not_visited):
                not_visited.remove(node)
                q.append(node)

    return count

# Info about components:
# list of tuples [root, size] for each component
def __get_components(graph: Graph) -> list:
    not_visited = graph.vertices()
    components = list()

    while(not_visited):
        v = not_visited.pop()
        component_size = __bfs_search_component(graph, v, not_visited)
        components.append((v, component_size))

    return components

# Max component 
# components: list of tuples [root, size]
# returns tuple [root, size] with max component
def __find_max_component(components: list) -> tuple:
    components_sorted = sorted(components, key=lambda a: a[1], reverse=True)
    return components_sorted[0]

# components: list of tuples [root, size]
# returns percentage of vertices in max component
def __percent_of_vertices(components: list, graph: Graph) -> float:
    root, size = __find_max_component(components)
    n = graph.number_of_vertices()

    return size / n


############################################################################################


# this function add count to list of distances to d - 1 position
# distances = list (array), i-th element represents count of vertices on i+1 distance

# WARNING: this function assumes that new distance d, that is not in list yet, is +1 then
# maximum in list because d comes from BFS, where each level is +1 then previous.
# thus new distance comes to the end of list.
def __add_to_distances_list(d: int, count: int, distances: list):
    if (len(distances) < d):
        distances.append(count)
    else:
        distances[d - 1] += count


# this function collect count of vertices on each possible distance (level) to special list: distances
# distances = list (array), i-th element represents count of vertices on i+1 distance
# returns eccentricity of given vertex

# WARNING: changes (distances)
def __bfs_get_counts_of_vertices_on_distance(v: int, distances: list, graph: Graph) -> int:
    visited = set()
    visited.add(v)
    q = deque()
    d = 0
    q.append((v, d))

    while (q):
        v, d = q.popleft()
        adj = graph.adj(v)
        count_adj = len(adj)

        if (count_adj == 0):
            return d
        
        count_new = 0

        for node in adj:
            if (node not in visited):
                visited.add(node)
                q.append((node, d + 1))
                count_new += 1

        if (count_new != 0):
            d += 1
            __add_to_distances_list(d, count_new, distances)

    return d

# returns set of vertices in given component with root = v
def __get_component_vertices(v: int, graph: Graph) -> set:
    visited = set()
    visited.add(v)
    q = deque()
    q.append(v)

    while (len(q) != 0):
        v = q.popleft()
        adj = graph.adj(v)

        for node in adj:
            if (node not in visited):
                visited.add(node)
                q.append(node)

    return visited


# Radius, diameter and 90-th percentile

# distances = list (array), i-th element represents count of vertices on i+1 distance
# max_distances = not sorted list of eccentricities
# returns d_metrics = {'radius', 'diameter', 'perc90'}

# TODO: percentile is int (checked with numpy) while in dataset properties it is float???
def __get_metrics_from_distances_list(distances: list, max_distances: list) -> dict:
    d_metrics = {'radius': 0, 'diameter': 0, 'perc90': '0'}

    max_distances.sort()
    d_metrics['radius'] = max_distances[0]
    d_metrics['diameter'] = max_distances[-1]

    #sequence = list()
    #for d, count in enumerate(distances):
    #    sequence += [d + 1] * count
    #perc = numpy.percentile(sequence, 90)
    #print(perc)

    selection_size = sum(distances)
    idx_proc90 = math.ceil(selection_size * 0.9)
    idx = 0

    for d, count in enumerate(distances):
        if (count + idx < idx_proc90):
            idx += count
            continue
        else:
            d_metrics['perc90'] = d + 1
            return d_metrics

# returns subgraph made by snowball method with root = v and size ~max_count
def __snowball_BFS(v: int, graph: Graph, max_count: int) -> set:
    visited = set()
    visited.add(v)
    q = deque()
    q.append(v)

    while (q):
        v = q.popleft()
        adj = graph.adj(v)

        if (len(visited) >= max_count):
            return visited
        
        for node in adj:
            if (node not in visited):
                visited.add(node)
                q.append(node)

                if (len(visited) >= max_count):
                    return visited
                
    return visited

# returns list of randomly picked v from vertices
# сделать сравнение с наличием в выбранных и не удалять!
def __pick_vertexes(vertices: set, count: int) -> list:
    vertexes_copy = list(vertices)
    chosen = list()

    for _ in range(0, count):
        random_idx = random.randint(0, len(vertexes_copy) - 1)
        random_v = vertexes_copy[random_idx]
        chosen.append(random_v)
        vertexes_copy.remove(random_v)

    return chosen

# Estimate radius, diameter and 90-th percentile not by snow method
# it takes 500 random vertices and counts distances for them to all other vertices in component
# returns d_metrics = {'radius', 'diameter', 'perc90'}
def __estimate_metrics_not_snow(vertices: set, graph: Graph) -> dict:
    random_count = 500  # count of v for random picking
    loop_count = 3  # count of times for estimation

    distances = list()
    max_distances = list()
    radius = 0
    diameter = 0
    perc90 = 0

    for i in range(0, loop_count):
        print(f"loop {i + 1}/{loop_count}")
        chosen = __pick_vertexes(vertices, random_count)

        for idx, v in enumerate(chosen):
            max_distances.append(__bfs_get_counts_of_vertices_on_distance(v, distances, graph))

            if ((idx + 1) % 100 == 0):
                print(f"{idx + 1}/{len(chosen)}")

        metrix = __get_metrics_from_distances_list(distances, max_distances)

        print(f"intermediate distance statistics: {distances}")
        print(f"intermediate metrix: {metrix}")

        radius += metrix['radius']
        diameter += metrix['diameter']
        perc90 += metrix['perc90']

    # count arithmetical mean
    return {'radius': radius * 1.0 / loop_count, 
            'diameter': diameter * 1.0 / loop_count,
            'perc90': perc90 * 1.0 / loop_count}


# Estimate radius, diameter and 90-th percentile by snow method

# it takes 2 random vertices, makes subgraph with 500 vertices by snowball method
# and counts distances for them to all other vertices in component
# returns d_metrics = {'radius', 'diameter', 'perc90'}
def __estimate_metrics_snow(vertexes, graph):
    snowball_count = 3  # count of roots for snowball
    random_count = 500  # max count of v in snowball subgraph

    distances = list()
    max_distances = list()
    radius = 0
    diameter = 0
    perc90 = 0

    for i in range(0, snowball_count):
        print(f"loop {i + 1}/{snowball_count}")
        chosen = __pick_vertexes(vertexes, 1)
        vertexes_in_snowboll = (__snowball_BFS(chosen[0], graph, random_count))

        for idx, v in enumerate(vertexes_in_snowboll):
            max_distances.append(__bfs_get_counts_of_vertices_on_distance(v, distances, graph))

            if ((idx + 1) % 100 == 0):
                print(f"{idx + 1}/{len(vertexes_in_snowboll)}")

        metrix = __get_metrics_from_distances_list(distances, max_distances)

        print(f"intermediate distance statistics: {distances}")
        print(f"intermediate metrix: {metrix}")

        radius += metrix['radius']
        diameter += metrix['diameter']
        perc90 += metrix['perc90']

    # count arithmetical mean
    return {'radius': radius * 1.0 / snowball_count, 'diameter': diameter * 1.0 / snowball_count,
            'perc90': perc90 * 1.0 / snowball_count}


# component = [root, size] of max component (requires to be found outside from this function)
# counts distance properties: for small / big graphs
# returns:
# d_metrics = {'radius', 'diameter', 'perc90'} for SMALL
# d_metrics = {'snow': {'radius', 'diameter', 'perc90'}, 'not_snow': {'radius', 'diameter', 'perc90'}} for BIG
def __get_distance_properties(component, graph):
    small_graph_size = 500
    root, size = component
    vertices = __get_component_vertices(root, graph)

    # small graph
    if (size < small_graph_size):
        distances = list()
        max_distances = list()
        print("--- start counting distance metrix for small graph ---")

        for idx, v in enumerate(vertices):
            max_distances.append(__bfs_get_counts_of_vertices_on_distance(v, distances, graph))

            if ((idx + 1) % 10 == 0):
                print(f"{idx + 1}/{len(vertices)}")

        return __get_metrics_from_distances_list(distances, max_distances)
    
    # big graph
    else:
        print("--- start not snow estimation ---")
        metrics_not_snow = __estimate_metrics_not_snow(vertices, graph)

        print("--- start snow estimation ---")
        metric_snow = __estimate_metrics_snow(vertices, graph)

        return {'not_snow': metrics_not_snow, 'snow': metric_snow}

#small
#graph = Graph(file_path="out .soc-sign-test", timestamp_col=2, skip_first_line=True)

#big
#graph = Graph(file_path="out.soc-sign-bitcoinotc", timestamp_col=2, skip_first_line=True)
#comps = __get_components(graph)
#max_comp = __find_max_component(comps)
#print("start count\n")
#print(__get_distance_properties(max_comp, graph))


############################################################################################


# BFS for component to find traversal
def __bfs(graph: Graph, src: int) -> list:
    visited = set()
    bfs_traversal = list()
    queue = deque()

    queue.append(src)
    visited.add(src)

    while (queue):
        curr_vertex = queue.popleft()
        bfs_traversal.append(curr_vertex)
        edges = graph.adj(curr_vertex)

        if (not edges):
            continue

        for neighbour in edges:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    return bfs_traversal


# Average clustering coefficient
# vertexId: vertexId in max component
def __average_clustering(graph: Graph, vertexId: int) -> float:
    print('--- start calculating average clustering coefficient ---')
    
    cl = 0
    vertices = __bfs(graph, vertexId)

    for vertex in vertices:
        neighbors = graph.adj(vertex)
        degree = len(neighbors)

        if (degree < 2):
            continue

        edges_neighbors_count = 0
        visited_neighbors = set()

        for neighbor in neighbors:
            curr_neighbors = graph.adj(neighbor)

            for item in curr_neighbors:
                if ((item not in visited_neighbors) and (item in neighbors)):
                    edges_neighbors_count += 1
            
            visited_neighbors.add(neighbor)

        cl += (2 * edges_neighbors_count)/(degree * (degree - 1))

    cl /= len(vertices)

    return cl


############################################################################################


# Degree assortativity
def __degree_assortativity(graph: Graph) -> float:
    print('--- start calculating degree assortativity ---')

    edges_count = 0
    vertices = graph.vertices()
    visited = set()
    sum_mult = 0
    sum_sum = 0
    sum_sumsquares = 0

    for vertex in vertices:
        neighbors = graph.adj(vertex)
        degree = len(neighbors)

        for neighbor in neighbors:
            if (neighbor in visited):
                continue

            curr_degree = len(graph.adj(neighbor))

            sum_mult += degree * curr_degree
            sum_sum += degree + curr_degree
            sum_sumsquares += degree ** 2 + curr_degree ** 2

            edges_count += 1

        visited.add(vertex)

    M = 1 / edges_count
    arg = M * ((0.5 * sum_sum) ** 2)
    r = (sum_mult - arg) / (0.5 * sum_sumsquares - arg)

    return r
