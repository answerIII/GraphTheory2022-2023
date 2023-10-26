
import csv

class Graph():

    static_features = [] # Статические признаки: Common Neighbours (CN); Adamic-Adar (AA); Jaccard Coefficient (JC); Preferential Attachment (PA)
    edges = []
    nodes = set()
    dataset = 'none'
    
    #def __init__(self, file_path) -> None:

    def read_from_file(self, filename):
        filepath = 'datasets/'+ filename +'.csv'
        index = 0
        self.dataset = filename
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

    def write_results_to_csv(self):
        filepath = 'done/'+ self.dataset +'.csv'
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = ['Node1', 'Node2', 'Common Neighbours', 'Adamic-Adar', 'Jaccard Coefficient', 'Preferential Attachment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in self.static_features:
                writer.writerow(result)
    

    def print_edges(self):
        for edge in self.edges:
            print(str(edge.index) + ' -- ' +str(edge.node1) + ' ' + str(edge.node2))


