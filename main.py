import logreg
import file_interaction
from graph import Graph
from parted_graph import PartedGraph
from pathlib import Path


def main(path='data/digg-friends.txt'):
    test_flag = False
    tmp = path.split('/')
    if tmp[1] == 'test':
        test_flag = True
    path = Path(path)
    name = path.name.split('.')[0]
    print(name)
    print("Reading graph data...")
    if test_flag:
        v_num, e_num, edges = file_interaction.read_test_file(path)
    else:
        v_num, e_num, edges = file_interaction.read_file(path)
    print("Reading completed")
    print("Creating graph...")
    g = Graph(list(range(1, v_num+1)), edges)
    print("Graph created")
    print("Getting max component...")
    sub_g = g.get_max_component_subgraph()
    print("Max component obtained")
    print("Calculating characteristics...")
    file_interaction.save_results(name=name,
                                  vertices_number=g.get_vertices_num(),
                                  edges_number=g.get_edges_num(),
                                  density=g.get_density(),
                                  components_number=g.get_components_count(),
                                  max_component_part=g.get_max_component_part(),

                                  radius=sub_g.get_radius(),
                                  diameter=sub_g.get_diameter(),
                                  percentile_90=sub_g.get_percentile(),
                                  average_cluster_coefficient=sub_g.get_average_cluster_coefficient(),
                                  pearson_coefficient=sub_g.get_pearson_coefficient(),
                                  test_flag=test_flag)

    print('Characteristics saved')
    if test_flag:
        return

    parted_g = PartedGraph(list(range(1, v_num+1)), edges)
    print("Setting static features...")
    parted_g.set_static_features()
    print("Static features are set")
    print("Getting predict based on static features...")
    logreg.train(parted_g.get_static_features_dataframe().dropna(), name)
    logreg.save_figure(name)
    print("Static features predict done")
    print("Setting temporal weights...")
    parted_g.set_temporal_weighting()
    print("Setting node activity...")
    parted_g.set_node_activity()
    print("Combining node activity...")
    parted_g.combine_node_activity()
    print("Getting static topological + node activity predict...")
    df = logreg.concat_dfs(parted_g.get_node_activity_features_dataframe(), parted_g.get_static_features_dataframe())
    logreg.train(df, name)
    logreg.save_figure(name, static_flag=False)
    print("Static topological + node activity predict done")


try:
    main('data/test/testgraph_7.txt')
except Exception as err:
    print('Something went wrong, all collected results saved. Error message:')
    raise err
else:
    print('Completed successfully')
