from math import inf
#класс определяющий неориентированный граф
class UndirectedGraph:
    def __init__(self, name="Untitled undirected graph"):
        self.name = name #название графа
        self.edge_map = {} #словарь рёбер по типу {node_begin:{node_end:[t1,t2,...]}}, где t1,t2 и т.д время добавления ребра
        self.v = 0 #количество вершин
        self.e = 0 #количество рёбер без мультирёбер
        self.me=0 #количество рёбер, учитывая мультирёбра
        self.t_max=0
        self.t_min=inf
        self.t_list=[]
        self.loops=0

    #метод для добавления вершины в граф, если она ещё не существует в графе
    def add_node(self, a):
        if a not in self.edge_map.keys():
            self.edge_map[a] = {}
            self.v += 1

    #метод для добавления ребра в граф
    def add_edge(self, a, b, t):
        if a==b:
            self.loops+=1
            return
        #добавляем вершины ребра в граф (если они уже были - они не добавятся)
        self.add_node(a)
        self.add_node(b)
        #если одна из вершин ребра уже присутствует в словаре от другой вершины - значит такое ребро уже было в графе
        if b in self.edge_map[a].keys():
            self.edge_map[a][b].append(t)
            self.edge_map[b][a].append(t)
        else:
            self.edge_map[a][b]=[t]
            self.edge_map[b][a]=[t]
            self.edge_map[a][b].sort()
            self.edge_map[b][a].sort()
            self.e += 1
        self.t_max=max(t,self.t_max)
        self.t_min=min(t,self.t_min)
        self.t_list.append(t)
        self.t_list.sort()
        self.me+=1
