from graphs_init.graph_read import read_undirected_graph
from tasks.task1_1 import *
from tasks.feature_3 import *
from random import sample
from tasks.regression_model import *
from tasks.static_charecteristics import *

def write_output_to_file(output_filename: str, output: List[str]):
    with open(output_filename, "w") as out:
        for s in output:
            out.write(s + "\n")

if __name__ == '__main__':
    
    output=[]
    filenames=["radoslaw_email_email", #0
               "small-graph",          #1
               "dnc-corecipient",      #2
               "sample",               #3
               "team_9",               #4
               "email-Eu-core-temporal",    #5
               "soc-sign-bitcoinalpha",     #6 
               "munmun_digg_reply",         #7
               "testgraph_1",               #8
               "testgraph_2",               #9
               "testgraph_3",               #10
               "testgraph_4",               #11
               "testgraph_5",               #12
               "testgraph_6",               #13
               "testgraph_7",               #14
               "opsahl-ucsocial",           #15
               "socfb-Middlebury45",        #16
               "socfb-Reed98"]              #17
    
    with_t=[1,1,1,1,0,1,1,1,0,0,0,0,0,0,0,1,0,0]
    index_in_list=2 # это меняем в зависимости от того, какой граф хотим протестить из списка
    restriction_number=350
    filename=filenames[index_in_list]
    graph_with_t=with_t[index_in_list]

    print(filename)
    graph=read_undirected_graph(filename,graph_with_t)
    print("ok")

    output.append("Количество вершин, уникальных рёбер графа, всех рёбер:"+str(graph.v)+","+str(graph.e)+","+str(graph.me))
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

    if graph.v>500:
        part_for_input=random_part
    else:
        part_for_input=mwcc

    acl=average_clustering(graph,part_for_input)
    output.append("Средний кластерный коэффициент:"+str(acl))

    coef=calculate_coef_pirs(graph,part_for_input)
    output.append("Коэффициент ассортативности:"+str(coef))

    if graph_with_t:

        t_s=graph.t_list[math.ceil(2/3*(len(graph.t_list)-1))]
        print(t_s)
        node_activities,graph_part_nodes=get_node_activities(graph,t_s)

        #snowball_for_regression=get_snowball(graph,graph_part_nodes,1,10000)

        if len(mwcc)>1000:
            graph_part_nodes=get_snowball_for_regression(graph,graph_part_nodes,1,restriction_number,t_s)
            # graph_part_nodes=sample(graph_part_nodes,min(len(mwcc),restriction_number))

        print("Node activities calculated")
        print(len(graph_part_nodes))

        X,edges=get_x_edges(graph, node_activities,graph_part_nodes,t_s)

        # for i in range(len(X)):
        #     print("---------------------------------")
        #     print(X[i])
        #     print(len(X[i]))

        Y=get_y(graph,edges,t_s)
        # print(Y)

        auc=regression_model(X,Y,filename)
        output.append("AUC:"+str(auc))
        
    else:
        
        output.append("Для вершин 1 и 2:")
        output.append("Common Neighbours (CN):"+str(common_neigbours(graph,1,2,graph.t_max)))
        output.append("Adamic-Adar (AA):"+str(adamic_adar(graph,1,2,graph.t_max)))
        output.append("Jaccard Coefficient (JC):"+str(jaaccard_coefficient(graph,1,2,graph.t_max)))
        output.append("Preferential Attachment (PA):"+str(preferential_attachment(graph,1,2,graph.t_max)))

    write_output_to_file("output/"+filename+"-output"+".txt", output)
    
