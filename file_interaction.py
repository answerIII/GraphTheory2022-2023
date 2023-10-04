from pathlib import Path


def read_test_file(path: Path):
    f = open(path)
    edges = []
    vertices = set()
    for line in f:
        v1, v2 = map(int, line.split())
        vertices.add(v1)
        vertices.add(v2)
        edges.append((min(v1, v2), max(v1, v2), 0, 0))
    v_num = len(vertices)
    e_num = len(edges)
    print(v_num, e_num)
    edges.sort()
    return v_num, e_num, edges


def read_file(path: Path):
    f = open(path)
    edges = []
    v_num, e_num = map(int, f.readline().split())
    for line in f:
        v1, v2, w, t = map(int, line.split())
        edges.append((v1, v2, w, t))
    f.close()
    return v_num, e_num, edges


def save_results(name: str,
                 vertices_number: int,
                 edges_number: int,
                 density: float,
                 components_number: int,
                 max_component_part: float,
                 radius: int,
                 diameter: int,
                 percentile_90: int,
                 average_cluster_coefficient: float,
                 pearson_coefficient: float,
                 test_flag=False):
    if test_flag:
        p = Path('characteristics', 'test', name + '.txt')
    else:
        p = Path('characteristics', name + '.txt')
    f = open(p, mode='w')
    f.write("Number of vertices: " + str(vertices_number) + '\n')
    f.write("Number of edges: " + str(edges_number) + '\n')
    f.write("Density: " + str(density) + '\n')
    f.write("Number of components: " + str(components_number) + '\n')
    f.write("Max component part: " + str(max_component_part) + '\n')
    f.write("\n---------------FOR MAX COMPONENT---------------\n\n")
    f.write("Radius: " + str(radius) + '\n')
    f.write("Diameter: " + str(diameter) + '\n')
    f.write("90 percentile: " + str(percentile_90) + '\n')
    f.write("Average cluster coefficient: " + str(average_cluster_coefficient) + '\n')
    f.write("Pearson coefficient: " + str(pearson_coefficient) + '\n')
    f.close()
