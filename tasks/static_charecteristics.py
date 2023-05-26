from graphs_init.undirected_graph import UndirectedGraph
from typing import Set, Tuple, List
from math import log

#Функция для нахождения пересечения двух множеств (И)
def conjunction(graph: UndirectedGraph, u: int, v: int,t_s:int) -> List[int]:
    result=[]
    neigbours_1=[]
    neigbours_2=[]
    for i in graph.edge_map[u].keys():
        if min(graph.edge_map[u][i])<=t_s:
            neigbours_1.append(i)
    for i in graph.edge_map[v].keys():
        if min(graph.edge_map[v][i])<=t_s:
            neigbours_2.append(i)
    for k in neigbours_2:
        if k in neigbours_1:
            result.append(k)
    return result


def get_neigbours(graph: UndirectedGraph, u: int,t_s:int):
    neigbours=[]
    for i in graph.edge_map[u].keys():
        if min(graph.edge_map[u][i])<=t_s:
            neigbours.append(i)
    return neigbours

#Функция для нахождения объединения двух множеств (ИЛИ)
def disjunction(graph: UndirectedGraph, u: int, v: int,t_s:int) -> List[int]:
    neigbours_1=get_neigbours(graph,u,t_s)
    neigbours_2=get_neigbours(graph,v,t_s)
    for k in neigbours_2:
        if k not in neigbours_1:
            neigbours_1.append(k)
    return neigbours_1

#Нахождение статических метрик по формулам
def common_neigbours(graph: UndirectedGraph, u: int, v: int,t_s:int) -> int:
    return len(conjunction(graph, u, v,t_s))

def adamic_adar(graph: UndirectedGraph, u: int, v: int,t_s:int) -> float:
    conjunction_set=conjunction(graph,u,v,t_s)
    res=0
    for k in conjunction_set:
        neigbours=get_neigbours(graph,k,t_s)
        res+=(1/log(len(neigbours)))
    return res

def jaaccard_coefficient(graph: UndirectedGraph, u: int, v: int,t_s:int) -> float:
    return len(conjunction(graph,u,v,t_s))/len(disjunction(graph,u,v,t_s))

def preferential_attachment (graph: UndirectedGraph, u: int, v: int,t_s:int) -> int:
    neigbours_1=get_neigbours(graph,u,t_s)
    neigbours_2=get_neigbours(graph,v,t_s)
    return len(neigbours_1)*len(neigbours_2)
