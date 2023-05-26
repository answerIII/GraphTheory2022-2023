import numpy as np
import random
from logger import Logger
from graph import Graph
from config import datasets
from collections import deque
from temporal_features import get_temporal_features as get_temporal
from static_features import get_static_properties as get_static


##########################################################__FEATURES__##########################################################

def get_number_of_features(dataset : dict, static : bool) -> list:
    subdir = 'static/' if (static) else 'temporal/'
    features_logger = Logger(dir='../features/' + subdir, logs_file_name=dataset['file_name'] + '.json', safe_mode=True)
    features = features_logger.get_features()
    return [len([f for f in features if f[0] == 0]), len([f for f in features if f[0] == 1])]

def get_features_as_matrix(dataset : dict, static : bool, max_amount : int = None, vectors_equalization : bool = False) -> tuple:
    subdir = 'static/' if (static) else 'temporal/'
    features_logger = Logger(dir='../features/' + subdir, logs_file_name=dataset['file_name'] + '.json', safe_mode=True)
    if (features_logger.is_empty()):
        return None

    features = features_logger.get_features()
    if (max_amount is None):
        if (vectors_equalization):
            max_amount = max([len([f for f in features if f[0] == 0]), len([f for f in features if f[0] == 1])])
        else:
            max_amount = min([len([f for f in features if f[0] == 0]), len([f for f in features if f[0] == 1])])

    counter = [0, 0]
    vector = []
    matrix = []
    for feature in features:
        appearance = feature[0]
        if (counter[appearance] >= max_amount):
            continue
        counter[appearance] += 1

        vector.append(appearance)
        feature.pop(0)
        matrix.append(feature)

    if (vectors_equalization):
        __equalize(matrix, vector, counter, max_amount)

    return np.array(vector), np.nan_to_num(np.array(matrix), posinf=0, neginf=0)

def collect_features_into_files(dataset : dict, static : bool, max_amount : int = None, maximize : bool = False) -> None:
    graph = Graph(file_path = '../data/' + dataset['file_name'], 
                  timestamp_col = dataset['timestamp_col'], 
                  weight_col = dataset['weight_col'],
                  number_of_lines_to_skip = dataset['number_of_lines_to_skip'],  
                  timestamp_filter = dataset['filter'], 
                  is_multigraph = dataset['is_multigraph'])
    features_logger = Logger(dir = '../features/' + ('static/' if (static) else 'temporal/'), 
                             logs_file_name = dataset['file_name'] + '.json', 
                             saving_step = 1000 if (static) else 100)
    pairs_logger = Logger(dir = '../pairs/', 
                          logs_file_name = dataset['file_name'] + '.json', 
                          safe_mode = True)

    pairs_list = pairs_logger.get_pairs()
    if (max_amount is None):
        min_or_max = max if (maximize) else min
        max_amount = min_or_max(len([pair for pair in pairs_list if pair[2] == 0]), 
                                len([pair for pair in pairs_list if pair[2] == 1]))

    features_list = features_logger.get_features()
    features_counter = [len([feature for feature in features_list if feature[0] == 0]), 
                        len([feature for feature in features_list if feature[0] == 1])]

    for pair in pairs_list:
        v1 = pair[0]
        v2 = pair[1]
        appearance = pair[2]

        if (features_counter[appearance] == max_amount) or (features_logger.contains(v1, v2)):
            continue

        print(v1, v2, features_counter)
        features = [appearance] + (get_static(v1, v2, graph) if (static) else get_temporal(v1, v2, graph).tolist()) 
     
        features_logger.log(v1, v2, features)
        features_counter[appearance] += 1

    features_logger.dump()

def __equalize(matrix : list, vector : list, counter : list, max_amount : int) -> None:
    if (counter[0] < max_amount):
        __fill_to_max(matrix, vector, counter, max_amount, appearance=0)
    if (counter[1] < max_amount):
        __fill_to_max(matrix, vector, counter, max_amount, appearance=1)   

def __fill_to_max(matrix : list, vector : list, counter : list, max_amount : int, appearance : int):
    while (True):
        size = len(vector)
        for i in range(size):
            if (counter[appearance] >= max_amount):
                return
            if (vector[i] == appearance):
                counter[appearance] += 1
                vector.append(vector[i])
                matrix.append(__process_vector(matrix[i]))

def __process_vector(vector : list, noise_factor : float = 0.01) -> list:
    for i in range(len(vector)):
        vector[i] += random.randrange(-1, 1) * vector[i] * noise_factor * random.random()
    return vector

##########################################################__PAIRS__##########################################################

def get_number_of_pairs(dataset : dict) -> list:
    logger = Logger(dir='../pairs/', logs_file_name=dataset['file_name'] + '.json', safe_mode=True)
    return __count_appearance(logger)

def collect_pairs_into_files(dataset : dict, max_amount : int = 10000) -> None:
    logger = Logger(dir='../pairs/', logs_file_name=dataset['file_name'] + '.json', saving_step=100)

    file_path = '../data/' + dataset['file_name']
    timestamp_col = dataset['timestamp_col']
    weight_col = dataset['weight_col']
    number_of_lines_to_skip = dataset['number_of_lines_to_skip']
    filter = dataset['filter']
    is_multigraph = dataset['is_multigraph']

    graph_full = Graph(file_path=file_path, timestamp_col=timestamp_col, weight_col=weight_col, 
                       number_of_lines_to_skip=number_of_lines_to_skip, is_multigraph=is_multigraph)
    graph_cut = Graph(file_path=file_path, timestamp_col=timestamp_col, weight_col=weight_col, 
                       number_of_lines_to_skip=number_of_lines_to_skip, timestamp_filter=filter, is_multigraph=is_multigraph)

    found = __approximate_pairs_collection(graph_full, graph_cut, logger)
    if (found[1] < max_amount):
        __add_pairs_wich_will_appear(graph_cut, logger, filter)
    __check_correctness(graph_full, graph_cut, logger)
    print(__count_appearance(logger))

def __check_correctness(graph_full : Graph, graph_cut : Graph, logger : Logger) -> None:
    pairs = logger.get_pairs()
    for pair in pairs:
        v1 = pair[0]
        v2 = pair[1]
        appearance = pair[2]

        if (graph_cut.has_edges_between(v1, v2)):
            print('Has edge between:', v1, v2, appearance)
            input()
        if (appearance == 0) and (graph_full.has_edges_between(v1, v2)):
            print('Edge will appear:', v1, v2, appearance)
            input()
        if (appearance == 1) and not (graph_full.has_edges_between(v1, v2)):
            print('Edge will not appear:', v1, v2, appearance)
            input()

def __count_appearance(logger : Logger) -> list:
    pairs = logger.get_pairs()
    cnt = [0, 0]
    for pair in pairs:
        appearance = pair[2]
        cnt[appearance] += 1

    return cnt

def __find_double_neighbors(graph_full : Graph, graph_cut : Graph, src : int, logger : Logger, 
                          found_0 : int = 0, found_1 : int = 0, max_amount : int = 10000) -> tuple:
    
    visited = [False for _ in range(graph_full.max_vertex_id() + 1)]
    prev = [-1 for _ in range(graph_full.max_vertex_id() + 1)]
    
    queue = deque()  
    queue.append(src)
    visited[src] = True

    while (queue):
        current = queue.popleft()

        for child in graph_cut.adj(current):
            if not (visited[child]):
                visited[child] = True
                prev[child] = current
                queue.append(child)

            parent = prev[current]
            if (parent == -1) or (parent == child):
                continue
            if (logger.contains(parent, child)) or (graph_cut.has_edges_between(child, parent)):
                continue
           
            if (graph_full.has_edges_between(parent, child)):
                if (found_1 >= max_amount):
                    continue
                logger.log(parent, child, [1])
                found_1 += 1
            else:
                if (found_0 >= max_amount):
                    continue
                logger.log(parent, child, [0])
                found_0 += 1
    
    return found_0, found_1    

def __approximate_pairs_collection(graph_full : Graph, graph_cut : Graph, logger : Logger, max_amount : int = 10000) -> list:
    logs = logger.get_pairs()
    found_0 = len([pair for pair in logs if pair[2] == 0])
    found_1 = len([pair for pair in logs if pair[2] == 1])

    for _ in range(1000):
        src = random.randint(1, graph_full.max_vertex_id())
        found_0, found_1 = __find_double_neighbors(graph_full, graph_cut, src, logger, found_0, found_1, max_amount)
        print(found_0, found_1)
        if (found_0 >= max_amount) and (found_1 >= max_amount):
            logger.dump()
            return [found_0, found_1]
    
    logger.dump()
    return [found_0, found_1]


def __add_pairs_wich_will_appear(graph_cut : Graph, logger : Logger, filter : int) -> None:
    for edge in graph_cut.edges_that_will_appear(filter):
        v1 = edge[0]
        v2 = edge[1]
        if graph_cut.has_edges_between(v1, v2):
            continue

        v1_neighbors = graph_cut.adj(v1)
        v2_neighbors = graph_cut.adj(v2)

        if (len(v1_neighbors.intersection(v2_neighbors)) > 0) and (not logger.contains(v1, v2)):
            print(v1, v2)
            logger.log(v1, v2, [1])

    logger.dump()

##########################################################__COLLECTION__##########################################################

def check_patrition():
    for dataset in datasets:
        print(dataset['file_name'])
        file_path = '../data/' + dataset['file_name']
        timestamp_col = dataset['timestamp_col']
        weight_col = dataset['weight_col']
        number_of_lines_to_skip = dataset['number_of_lines_to_skip']
        filter = dataset['filter']
        is_multigraph = dataset['is_multigraph']

        graph_full = Graph(file_path=file_path, timestamp_col=timestamp_col, weight_col=weight_col, 
                        number_of_lines_to_skip=number_of_lines_to_skip, timestamp_filter=filter, is_multigraph=is_multigraph)
        print(graph_full.cut_proportion())
        

def collect_all_data():
    for dataset in datasets:
        collect_pairs_into_files(dataset)
    for dataset in datasets:
        collect_features_into_files(dataset, static=True, maximize=True)
    for dataset in datasets:
        collect_features_into_files(dataset, static=False, maximize=True)
