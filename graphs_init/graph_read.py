from graphs_init.undirected_graph import UndirectedGraph
import re

#функция для считывания графа
def read_undirected_graph(filename: str) -> UndirectedGraph:
    symbols=["0","1","2","3","4","5","6","7","8","9","."]
    graph = UndirectedGraph(filename)
    with open("datasets/"+filename+".txt") as file:
        for line in file:
            if line.startswith("%"):
                continue
            list_inp=[]
            if line[-1]=="\n":
                line=line[:-1]
            prev_pos=0
            for i in range(len(line)):
                if line[i] not in symbols:
                    list_inp.append(line[prev_pos:i])
                    prev_pos=i+1
                if len(list_inp)==2:
                    break
            j=len(line)-1
            while line[j] in symbols:
                j-=1
            list_inp.append(line[j+1:])
            node_from, node_to, t=list_inp[0],list_inp[1],list_inp[2]
            t=float(t)
            graph.add_edge(int(node_from), int(node_to), t)
    return graph