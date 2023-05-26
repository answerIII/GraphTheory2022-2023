from graphs_init.graph_read import read_undirected_graph
from tasks.task1_1 import *
from tasks.feature_3 import *
from random import sample
from tasks.regression_model import *

def write_output_to_file(output_filename: str, output: List[str]):
    with open(output_filename, "w") as out:
        for s in output:
            out.write(s + "\n")

if __name__ == '__main__':
    output=[]
    filename="radoslaw_email_email"
    graph=read_undirected_graph(filename)
    print("ok")
    output.append("Количество вершин и рёбер графа:"+str(graph.v)+","+str(graph.e))
    dense=(2*graph.e)/((graph.v-1)*graph.v)
    output.append("Плотность графа:"+str(dense))
    mwcc,wcc_count=get_max_weakly_connected_component(graph)
    output.append("Число компонент слабой связности:"+str(wcc_count))
    output.append("Доля вершин:"+str(len(mwcc)/graph.v))
    random_part=sample(mwcc, min(500, len(mwcc)))
    snowball_part=get_snowball(graph,mwcc,3,500)
    r_rand,d_rand,p_rand=calculate_radius_diameter_percentile(graph,random_part)
    r_snow,d_snow,p_snow=calculate_radius_diameter_percentile(graph,snowball_part)
    output.append("Радиус, диаметр, 90 процентиль (случайно выбранные вершины):"+str(r_rand)+","+str(d_rand)+","+str(p_rand))
    output.append("Радиус, диаметр, 90 процентиль (метод snowball):"+str(r_snow)+","+str(d_snow)+","+str(p_snow))
    acl=average_clustering(graph,mwcc)
    output.append("Средний кластерный коэффициент для наибольшей компоненты слабой связности:"+str(acl))
    coef=calculate_coef_pirs(graph,mwcc)
    output.append("Коэффициент ассортативности:"+str(coef))
    write_output_to_file("output/"+filename+".txt", output)
    t_s=graph.t_list[math.ceil(2/3*(len(graph.t_list)-1))]
    print(t_s)
    node_activities,graph_part_nodes=get_node_activities(graph,t_s)
    #snowball_for_regression=get_snowball(graph,graph_part_nodes,1,10000)
    X,edges=get_x_edges(graph, node_activities,graph_part_nodes,t_s)
    # for i in range(len(X)):
    #     print("---------------------------------")
    #     print(X[i])
    #     print(len(X[i]))
    Y=get_y(graph,edges)
    regression_model(X,Y)
    
