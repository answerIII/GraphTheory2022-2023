from components.graph import Graph

def testtt(filename):
    filepath = 'datasets/'+ filename +'.csv'
    graph = Graph()

    graph.read_from_file(filepath)
    graph.print_edges() 


