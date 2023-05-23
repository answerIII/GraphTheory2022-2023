import math

def calc_four_static_properties(adjList: list[list], edge: tuple, display_interm_results = False) -> list:
    """Считает 4 статических топологических признака, возвращает список [CN, AA, JC, PA]"""

    def Common_Neighbours(adjList, edge):
        u = edge[0]
        v = edge[1]
        
        intersection = set(adjList[u]) & set(adjList[v])
        
        return len(intersection)


    def Adamic_Adar(adjList, edge):
        u = edge[0]
        v = edge[1]

        intersection = set(adjList[u]) & set(adjList[v])
        
        sum = 0
        for vertex in intersection:
            vertex_degree = len(adjList[vertex]) # количество вершин, смежных вершине vertex

            if vertex_degree != 0 and vertex_degree != 1:
                sum += 1 / (math.log(vertex_degree, 2))

        return sum


    def Jaccard_Coef(adjList, edge):
        u = edge[0]
        v = edge[1]

        intersection = set(adjList[u]) & set(adjList[v])
        union = set(adjList[u]) | set(adjList[v])

        if len(union) == 0:
            return 0

        result = len(intersection) / len(union)
    
        return result


    def Preferential_Attachment(adjList, edge):
        u = edge[0]
        v = edge[1]

        degree_u = len(adjList[u])
        degree_v = len(adjList[v])

        result = degree_u * degree_v
    
        return result

    CN = Common_Neighbours(adjList, edge)
    AA = Adamic_Adar(adjList, edge)
    JC = Jaccard_Coef(adjList, edge)
    PA = Preferential_Attachment(adjList, edge)


    if display_interm_results:
        print("for edge:", edge)
        print("CN:" , Common_Neighbours(adjList, edge))
        print("AA:" ,Adamic_Adar(adjList, edge))
        print("JC:" ,Jaccard_Coef(adjList, edge))
        print("PA:" ,Preferential_Attachment(adjList, edge))

    return [CN, AA, JC, PA]
    


    