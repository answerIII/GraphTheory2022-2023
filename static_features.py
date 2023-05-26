import math
# На вход функции подаются пары вершин и исходный граф, на выходе каждой паре сопоставляется вектор признаков 
def get_static_features(graph, pairs: list[(int,int)]) -> dict[(int,int), (int,int,int,int)]: 
    features = dict() # Искомые признаки
    for u, v in pairs: 
        u_border = graph[u]
        v_border = graph[v]
        borders_combining = [i for i in u_border + v_border if i in u_border or i in v_border ] # Объединение соседей u и v
        borders_intersection = [i for i in u_border + v_border if i in u_border and i in v_border ] # Пересечение соседей u и v
        CN = len(borders_combining) # Common Neighbours
        AA = 0.0 # Adamic-Adar 
        for z in borders_intersection:
            AA+=1/(math.log(graph[z]))
        JC = len(borders_intersection)/len(borders_combining)# Jaccard Coefficient
        PA = len(u_border) * len(v_border)# Preferential Attachment 
        features[(u,v)] = (CN, AA, JC, PA)

    return features
