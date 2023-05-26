import networkx as nx
from graph import Graph
import basic_properties
from config import datasets

def __make_graph_nx(graph: Graph):
    graph_nx = nx.Graph()
    graph_nx.add_nodes_from(graph.vertices())
    for v in graph.vertices():
        adj = graph.adj(v)
        for u in adj:
            edge = (v, u)
            graph_nx.add_edge(*edge)
    return graph_nx

def __make_max_comp(graph: Graph) :
    graph_nx = nx.Graph()
    max_comp_root = basic_properties.__find_max_component(basic_properties.__get_components(graph))
    max_comp = basic_properties.__get_component_vertices(max_comp_root[0], graph)
    graph_nx.add_nodes_from(max_comp)
    for v in max_comp:
        adj = graph.adj(v)
        for u in adj:
            edge = (v, u)
            graph_nx.add_edge(*edge)
    return graph_nx

for current_dataset in datasets:
    file_path = '../data/' + current_dataset['file_name']
    print(f'--- start counting basic props for {file_path}')
    number_of_lines_to_skip = current_dataset['number_of_lines_to_skip']
    timestamp_col = current_dataset['timestamp_col']
    graph = Graph(file_path, timestamp_col, current_dataset['weight_col'], number_of_lines_to_skip)

    graph_nx = __make_graph_nx(graph)

    #v_g = graph.number_of_vertices()
    #ed_g = graph.number_of_edges(without_multiplicity=True)
    #v_nx = graph_nx.number_of_nodes()
    #ed_nx = graph_nx.number_of_edges()
    #print(f'v_g: {v_g}, ed_g: {ed_g}\nv_nx: {v_nx}, ed_nx: {ed_nx}')
    #continue

    properties_graph = {'density': 0, 'count_comps': 0, 'avg': 0, 'assort': 0}
    properties_nx = {'density': 0, 'count_comps': 0, 'radius': 0, 'diameter': 0, 'avg': 0, 'assort': 0}

    properties_graph['density'] = basic_properties.get_dencity(graph)
    properties_nx['density'] = nx.density(graph_nx)

    properties_graph['count_comps'] = basic_properties.get_components_count(graph)
    properties_nx['count_comps'] = nx.number_connected_components(graph_nx)

    # max_comp и percentage не ищется в nx!
    # далее работа только с максимальной компонентой
    metrix = basic_properties.get_metrics(graph)
    print(f'metrix for graph:\n {metrix}')

    properties_graph['avg'] = basic_properties.get_avg_coeff(graph)
    properties_graph['assort'] = basic_properties.get_dg_assortativity(graph)

    if (len(graph.vertices()) < 100000):
        print('make max component in networks')
        max_comp_nx = __make_max_comp(graph)

        # квантилей нет в nx!
        print('--- start count metrix in networkx:')
        radius = nx.radius(max_comp_nx)
        properties_nx['radius'] = radius
        print(f'count radius: {radius}')
        diameter = nx.diameter(max_comp_nx)
        properties_nx['diameter'] = diameter
        print(f'count diameter: {diameter}')
        avg_clust = nx.average_clustering(max_comp_nx)
        properties_nx['avg'] = avg_clust
        print(f'count avg_clust: {avg_clust}')
        assort = nx.degree_assortativity_coefficient(max_comp_nx)
        properties_nx['assort'] = assort
        print(f'count assort: {assort}')

    print(f'dataset: {file_path}\nresult: {properties_graph}\n{metrix}\nexpected: {properties_nx}')
    