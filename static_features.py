import math 

def get_static_features(graph, pairs: list[(int,int)]) -> list[(int,int,int,int)]: 
    features = [] # Искомые признаки
    for u, v in pairs: 
        u_border = graph[u]
        v_border = graph[v]
        borders_combining = set(u_border).union(set(v_border))# Объединение соседей u и v
        borders_intersection = [i for i in u_border | v_border if i in u_border and i in v_border] # Пересечение соседей u и v
        CN = len(borders_intersection) # Common Neighbours
        AA = 0.0 # Adamic-Adar 
        for z in borders_intersection:
            AA+=(1/(math.log(len(graph[z]))))
        JC = len(borders_intersection)/len(borders_combining)# Jaccard Coefficient
        PA = len(u_border) * len(v_border)# Preferential Attachment 
        features.append([CN, AA, JC, PA])
        
    return features


def compute_static_features_for_pair(graph):
    # print("Введите первую вершину")
    # u = int(input())
    # print("Введите вторую вершину")
    # v = int(input())
    u = 1
    v = 2
    u_border = graph[u]
    v_border = graph[v]
    borders_combining = set(u_border).union(set(v_border))# Объединение соседей u и v
    borders_intersection = [i for i in u_border | v_border if i in u_border and i in v_border] # Пересечение соседей u и v
    CN = len(borders_intersection) # Common Neighbours
    AA = 0.0 # Adamic-Adar 
    for z in borders_intersection:
        AA+=(1/(math.log(len(graph[z]))))
    JC = len(borders_intersection)/len(borders_combining)# Jaccard Coefficient
    PA = len(u_border) * len(v_border)# Preferential Attachment 
    output = ""
    output+=(f"Common Neighbours: {CN}") + '\n'
    output+=(f"Adamic-Adar : {AA}") + '\n'
    output+=(f"Jaccard Coefficient: {JC}") + '\n'
    output+=(f"Preferential Attachment: {PA}")

    return output
