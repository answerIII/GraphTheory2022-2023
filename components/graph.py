import pandas as pd
import csv

class Graph():

    static_features = [] # Статические признаки: Common Neighbours (CN); Adamic-Adar (AA); Jaccard Coefficient (JC); Preferential Attachment (PA). Учитываются все пары вершин, т.е. даже несуществующие ребра
    temporal_features = pd.DataFrame({'def': [], 'u': [], 'v': [],
                        'cnwl': [], 'aawl': [], 'jcwl': [], 'pawl': [],
                        'cnws': [], 'aaws': [], 'jcws': [], 'paws': [],
                        'cnwe': [], 'aawe': [], 'jcwe': [], 'pawe': [], 'time': []})
    edges = []
    nodes = set()
    node_neigh_2 = []
    name = 'none'
    tmin = float('inf')
    tmax = float('-inf')
    
    #def __init__(self, file_path) -> None:


    def edge_exist(self, node1, node2):
        for edge in self.edges:
            if ((edge.node1 == node1) and (edge.node2 == node2)) or ((edge.node1 == node2) and (edge.node2 == node1)):
                return 1
        
        return 0
    

    def get_time(self):
        for edge in self.edges:
            time = edge.time
            if time < self.tmin:
                self.tmin = time

            if time > self.tmax:
                self.tmax = time
        
        print(f"tmin: {self.tmin}, tmax: {self.tmax}")

    def find_max_edge_time(self, node1, node2):
        tmax = -1
        for edge in self.edges:
            if (((edge.node1 == node1) and (edge.node2 == node2)) or ((edge.node1 == node2) and (edge.node2 == node1))) and (edge.time > tmax):
                tmax = edge.time
        
        return tmax
        



    def def_edges_static(self): #Определить существует ли ребро в графе к моменту tmax для каждой пары вершин
        edge_set = set()
        static_features_with_def = []
        for edge in self.edges:
            edge_set.add((edge.node1, edge.node2))

        for feature in self.static_features:
            edge_exist = 0
            node1 = feature['Node1']
            node2 = feature['Node2']
            if (node1, node2) in edge_set or (node2, node1) in edge_set:
                edge_exist = 1

            result = {
                'Def': edge_exist,
                'Node1': feature['Node1'],
                'Node2': feature['Node2'],
                'Common Neighbours': feature['Common Neighbours'],
                'Adamic-Adar': feature['Adamic-Adar'],
                'Jaccard Coefficient': feature['Jaccard Coefficient'],
                'Preferential Attachment': feature['Preferential Attachment']
            }
            print (result)
            static_features_with_def.append(result)
        
        self.static_features = static_features_with_def
            








    def read_from_csv(self, filename):
        filepath = 'datasets/'+ filename +'.csv'
        index = 0
        self.name = filename
        from components.edge import Edge
        with open(filepath, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            for row in csvreader:
                node1 = int(row['in'])
                node2 = int(row['out'])
                weight = int(row['weight'])
                time = int(row['time'])

                    #Добавляем номер вершины в список всех вершин
                self.nodes.add(node1)
                self.nodes.add(node2)

                    #Cтроим прямое ребро, у прямого ребра четный индекс
                edge = Edge(index, node1, node2, weight, time)
                self.edges.append(edge)
                index += 1

                    #Cтроим обратное ребро, у обратного ребра нечетный индекс
                #edge = Edge(index, node2, node1, weight, time)
                #self.edges.append(edge)
                #index += 1

    def read_test_from_csv(self, filename):
        filepath = 'datasets/test/'+ filename +'.csv'
        index = 0
        self.name = filename
        print(filepath)
        from components.edge import Edge
        with open(filepath, 'r') as txtfile:
            edges= txtfile.readlines()
            for edge in edges:
                node1, node2 = edge.split()
                edge = Edge(index, int(node1), int(node2), 1, 1)


                self.nodes.add(node1)
                self.nodes.add(node2)
                self.edges.append(edge)
                index += 1



    def write_static_results_to_csv(self):
        filepath = 'done/'+ self.name +'_DONE.csv'
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['Def', 'Node1', 'Node2', 'Common Neighbours', 'Adamic-Adar', 'Jaccard Coefficient', 'Preferential Attachment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in self.static_features:
                writer.writerow(result)


    def read_static_results_from_csv(self):

        filepath = 'done/'+ self.name +'_DONE.csv'
        print('чтение из файла')
        df = pd.read_csv(filepath)
        print('конвертация в dataframe')
        results = df.to_dict(orient='records')
        self.static_features = results 



    

    def print_edges(self):
        for edge in self.edges:
            print(str(edge.node1) + ' ' + str(edge.node2))


    #Обработка файла с графом и сохранение в нужном нам виде
    def prep(self, file):
        if file[-4:] == "prep":
            return file
        else:
            file_path = 'datasets/' + file + '.csv'
            data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['in', 'out', 'weight', 'time'])
            df = {'in': [], 'out': [], 'weight': [], 'time': []}
            
            for index, row in data.iterrows():
                df['in'].append(row['in'])
                df['out'].append(row['out'])
                df['weight'].append(row['weight'])
                df['time'].append(row['time'])

            new_data = pd.DataFrame(df, columns=['in', 'out', 'weight', 'time'])
            new_name = 'datasets/' + file + '_' + '0' + 'prep.csv'
            new_data.to_csv(new_name, sep='\t', header=True, index=False)
            return file + '_' + '0' + 'prep'
        

    def find_neighbors_at_distance_2(self):
        # Создаем словарь, чтобы хранить информацию о соседях на расстоянии 2 для каждой вершины
        node_neigh_2 = {}
        
        # Проходим по каждому ребру в графе
        for edge in self.edges:
            node1 = edge.node1
            node2 = edge.node2
            # Добавляем node2 в соседей node1
            if node1 not in node_neigh_2:
                node_neigh_2[node1] = set()
            node_neigh_2[node1].add(node2)
            
            # Добавляем node1 в соседей node2
            if node2 not in node_neigh_2:
                node_neigh_2[node2] = set()
            node_neigh_2[node2].add(node1)
        
        # Теперь находим соседей второго уровня для каждой вершины
        for node in node_neigh_2:
            second_level_neighbors = set()
            for neighbor in node_neigh_2[node]:
                # Для каждого соседа первого уровня, добавляем его соседей второго уровня
                second_level_neighbors.update(node_neigh_2.get(neighbor, set()))
            # Удаляем из множества соседей второго уровня вершины первого уровня и саму вершину
            second_level_neighbors.discard(node)
            node_neigh_2[node] = list(second_level_neighbors)
        
        #for node, second_level_neighbors in node_neigh_2.items():
            #print(f"Соседи второго уровня для вершины {node}: {second_level_neighbors}")

        self.node_neigh_2 = node_neigh_2


    def print_neigbours_2(self):
        for node, second_level_neighbors in self.node_neigh_2.items():
            print(f"Соседи второго уровня для вершины {node}: {second_level_neighbors}")


