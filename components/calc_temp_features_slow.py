from components.calculator import Calculator
import math
from collections import defaultdict
import time

class Temporal_calculator(Calculator):

    def __init__(self, l, tmin, tmax) -> None:
        self.l = l
        self.tmin = tmin
        self.tmax = tmax

    def calc(self, graph):
        print('Начинаю темпоральные вычисления')
        start_time = time.time()
        edge_set = set()

        graph_dict = defaultdict(list)
        for edge in graph.edges: #Преобразуем ориентированный граф в неориентированный, добавляя обратные ребра
            graph_dict[edge.node1].append(edge.node2)
            graph_dict[edge.node2].append(edge.node1)

        for edge in graph.edges:
            edge_set.add((edge.node1, edge.node2))

        pos_counter = 0
        neg_counter = 0
        max = 10000



        for i, node1 in enumerate(graph_dict):
            for j, node2 in enumerate(graph_dict):
                if (i < j) and ((pos_counter < max) or (neg_counter < max)):
                    df = 0
                    if (node1, node2) in edge_set or (node2, node1) in edge_set:
                        pos_counter = pos_counter + 1
                        df = 1 
                    else:
                        neg_counter = neg_counter + 1

                    if (df == 1) and not (pos_counter < max):
                        continue

                    if (df == 0) and not (neg_counter < max):
                        continue
                    t = graph.find_max_edge_time(node1, node2)
                    result = self.temporal_feature_vector(graph, node1,node2, t)

                    print(result)
                    #graph.temporal_features.append(result)


        end_time = time.time()   
        execution_time1 = end_time - start_time
        print(f"Время выполнения: {execution_time1} секунд")    


    def temporal_feature_vector(self, graph, node1,node2, t):
        ans = []
        weight_functions = [self.w_linear, self.w_exponential, self.w_square_root]
        feature_functions = [self.AA_temporal_template, self.CN_temporal_template, self.JC_temporal_template, self.PA_temporal_template]
        for w_function in weight_functions:
            for f_function in feature_functions:
                #print(f"Признак: {f_function} и Вес: {w_function}")
                ans.append(f_function(graph,node1,node2, t, w_function))
        return ans
    
    def CN_temporal_template(self, graph, u, v, t, w_func):
        common_neighbors_weight = 0
        neighbors_u = self.get_neighbors(graph, u)
        neighbors_v = self.get_neighbors(graph, v)
        
        common_neighbors = neighbors_u.intersection(neighbors_v)
        
        for common_neighbor in common_neighbors:
            common_neighbors_weight += w_func(t) + w_func(t)
        
        return common_neighbors_weight


    def AA_temporal_template(self, graph, u, v, t, w_func):
        adamic_adar_temporal = 0
        neighbors_u = self.get_neighbors(graph, u)
        neighbors_v = self.get_neighbors(graph, v)
        common_neighbors = neighbors_u.intersection(neighbors_v)

        
        for common_neighbor in common_neighbors:
            denominator = 1 + sum(w_func(t) for x in self.get_neighbors(graph, common_neighbor))
            adamic_adar_temporal += (w_func(t) + w_func(t)) / math.log(denominator)

        return adamic_adar_temporal

    def JC_temporal_template(self, graph, u, v, t, w_func):
        intersection_weight = 0
        union_weight = 0
        neighbors_u = self.get_neighbors(graph, u)
        neighbors_v = self.get_neighbors(graph, v)
        
        common_neighbors = neighbors_u.intersection(neighbors_v)
        
        for common_neighbor in common_neighbors:
            intersection_weight += w_func(t) + w_func(t)
        
        for neighbor_u in neighbors_u:
            union_weight += w_func(t)
        
        for neighbor_v in neighbors_v:
            union_weight += w_func(t)
        
        if union_weight == 0:
            return 0  # избегаем деления на ноль
        
        jaccard_coefficient_temporal = intersection_weight / union_weight
        
        return jaccard_coefficient_temporal


    def PA_temporal_template(self, graph, u, v, t,  w_func):
        pa_temporal = 0
        neighbors_u = self.get_neighbors(graph, u)
        neighbors_v = self.get_neighbors(graph, v)
        
        for neighbor_u in neighbors_u:
            for neighbor_v in neighbors_v:
                pa_temporal += w_func(t) * w_func(t)
        
        return pa_temporal



    def w_linear(self, t):
        if (t==-1):
            l = 0
        else:
            l = (t - self.tmin) / (self.tmax - self.tmin)

        ans = self.l + (1-self.l) * l
        return ans

    def w_exponential(self, t):
        if (t==-1):
            e = 0
        else:
            e = (3*(t-self.tmin)) / (self.tmax-self.tmin)
        
        ans = self.l + (1-self.l) * (math.exp( e ) - 1) / (math.exp(3) - 1)
        return ans

    def w_square_root(self, t):
        
        if (t==-1):
            sqrt = 0
        else:
            sqrt = math.sqrt((t-self.tmin)/(self.tmax-self.tmin))
        
        ans = self.l + (1-self.l) * sqrt
        return ans
    

    def get_neighbors(self, graph, node):
        neighbors = set()
        for edge in graph.edges:
            n1 = edge.node1
            n2 = edge.node2
            if n1 == node:
                neighbors.add(n2)
            elif n2 == node:
                neighbors.add(n1)
        return neighbors