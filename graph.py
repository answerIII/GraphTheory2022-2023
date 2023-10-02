import queue
import random
from functools import reduce


class Graph:
    def __init__(self, vertices, edges=None):
        self.buf_distances = {}
        self.buf_eccs = None
        self.components = None
        if edges is None:
            edges = {}
        self.adj_list = {}
        self.edges = {}
        for i in vertices:
            self.adj_list[i] = set()
        for edge in edges:
            self.adj_list[edge[0]].add(edge[1])
            self.adj_list[edge[1]].add(edge[0])
            self.edges[(min(edge[0], edge[1]), max(edge[0], edge[1]))] = edge[3]

    def get_vertices_num(self):
        return len(self.adj_list)

    def get_edges_num(self):
        return len(self.edges)

    def get_density(self):
        n = self.get_vertices_num()
        return self.get_edges_num() / (n * (n - 1) / 2)

    def bfs(self, start_vertex, visited: set, func):
        q = queue.Queue()
        q.put(start_vertex)
        curr_visited = set()
        visited.add(start_vertex)
        func(start_vertex, start_vertex)
        while not q.empty():
            m = q.get()
            for neighbour in self.adj_list[m]:
                if neighbour not in curr_visited:
                    curr_visited.add(neighbour)
                    visited.add(neighbour)
                    q.put(neighbour)
                    func(m, neighbour)
        return curr_visited

    def find_components(self):
        if self.components is not None:
            return self.components
        visited = set()
        self.components = []
        for v in self.adj_list:
            if v not in visited:
                component = self.bfs(v, visited, lambda x, y: x)
                self.components.append(list(component))
        return self.components

    def get_components(self):
        return self.find_components()

    def get_components_count(self):
        return len(self.get_components())

    def get_max_component(self):
        return reduce(lambda x, y: x if len(x) > len(y) else y, self.get_components())

    def get_max_component_part(self):
        return len(self.get_max_component()) / len(self.adj_list)

    def get_max_component_subgraph(self):
        vertices = self.get_max_component()
        sub_g = Graph(vertices)
        sub_g.components = [vertices]
        vertices = set(vertices)
        for v in self.adj_list:
            if v in vertices:
                for u in self.adj_list[v]:
                    if u < v:
                        continue
                    if u in vertices:
                        sub_g.adj_list[v].add(u)
                        sub_g.adj_list[u].add(v)
                        sub_g.edges[(v, u)] = self.edges[(v, u)]
        return sub_g

    def get_distances(self, vertex):
        distances = {}

        def set_distance(parent, child):
            if parent == child:
                distances[child] = 0
            else:
                distances[child] = distances[parent] + 1

        visited = set()

        self.bfs(vertex, visited, set_distance)

        del distances[vertex]
        return distances

    def get_eccentricity(self, vertex):
        tmp = self.get_distances(vertex).values()
        for i in tmp:
            self.buf_distances[i] = 1 if i not in self.buf_distances.keys() else self.buf_distances[i] + 1
        return max(tmp)

    def set_eccentricities(self):
        if self.buf_eccs is not None:
            return
        self.buf_eccs = set()
        nums = set()
        vertices = set()
        tmp = list(self.adj_list.keys())
        if self.get_vertices_num() > 4096 or self.get_vertices_num() * self.get_edges_num() > 33554432:
            while len(nums) < 512:
                nums.add(random.randint(0, self.get_vertices_num()))
            while len(nums) > 0:
                vertices.add(tmp[nums.pop()])
        else:
            vertices = tmp
        c = 0
        n = len(vertices)
        for v in vertices:
            self.buf_eccs.add(self.get_eccentricity(v))
            c += 1
            print("Calculating eccentricities " + str(c) + " of " + str(n))

    def get_diameter(self):
        self.set_eccentricities()
        return max(self.buf_eccs)

    def get_radius(self):
        self.set_eccentricities()
        return min(self.buf_eccs)

    def get_percentile(self, perc=0.9):
        self.set_eccentricities()
        tmp = sum(self.buf_distances.values()) * perc
        for i in self.buf_distances:
            tmp -= self.buf_distances[i]
            if tmp < 0:
                return i

    def get_local_cluster_coefficient(self, vertex):
        k = len(self.adj_list[vertex])
        if k < 2:
            return 0
        neighbours = set(self.adj_list[vertex])
        double_e = 0
        for v in neighbours:
            tmp_neighbours = set(self.adj_list[v])
            double_e += len(tmp_neighbours.intersection(neighbours))
        return double_e / (k * (k - 1))

    def get_average_cluster_coefficient(self):
        cluster_sum = 0
        for v in self.adj_list:
            cluster_sum += self.get_local_cluster_coefficient(v)
        return cluster_sum / len(self.adj_list)

    def get_pearson_coefficient(self):
        R1 = 2 * self.get_edges_num()
        ks = {}
        for v in self.adj_list:
            ks[v] = len(self.adj_list[v])
        R2 = sum(map(lambda x: x * x, ks.values()))
        squared_R2 = R2 * R2
        R3 = sum(map(lambda x: x * x * x, ks.values()))
        Re = 0
        for v in self.adj_list:
            tmp = 0
            for u in self.adj_list[v]:
                tmp += ks[u]
            Re += tmp * ks[v]
        return (Re * R1 - squared_R2) / (R3 * R1 - squared_R2)
