#средний кластерный коэффициент
def calculate_average_clustering_coefficient(AllVertex, countVertex):
    total_clustering_coefficient = 0
    for vertex, neighbors in AllVertex.items():
        if len(neighbors) < 2:
            continue
        local_clustering_coefficient = 0
        for neighbor in neighbors:
            common_neighbors = set(neighbors) & set(AllVertex.get(neighbor, []))
            local_clustering_coefficient += len(common_neighbors)
        local_clustering_coefficient /= (len(neighbors) * (len(neighbors) - 1))
        total_clustering_coefficient += local_clustering_coefficient
    average_clustering_coefficient = total_clustering_coefficient / countVertex
    return average_clustering_coefficient