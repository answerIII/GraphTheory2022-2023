from components.graph import Graph
from components.calc_static_features import Static_calculator
from components.calc_properties import Properties_calculator
def testtt(file):
    
    #graph = Graph()

    #graph.read_from_file(file)
    #graph.print_edges() 

    #c = Static_calculator()
    #c.calc(graph)
    #graph.write_results_to_csv()

    g = Properties_calculator()
    g.calc(file)


