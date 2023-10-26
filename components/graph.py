from components.edge import Edge
import csv

class Graph():

    edges = []
    
    #def __init__(self, file_path) -> None:

    def read_from_file(self, file_path):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            for row in csvreader:
                node1 = int(row['in'])
                node2 = int(row['out'])
                weight = int(row['weight'])
                time = int(row['time'])
                edge = Edge(node1, node2, weight, time)
                self.edges.append(edge)


    def print_edges(self):
        for edge in self.edges:
            print (edge.node1 + ' ' + edge.node2)


