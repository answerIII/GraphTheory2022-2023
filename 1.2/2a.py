from traitlets.traitlets import default
from collections import defaultdict 
import numpy as np 
import math 
import random


f = open('small-graph.txt', 'r') 

dataset = f.readlines()

ver = defaultdict(set) # подграф с наибольшей КСС 

for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    if from_ind in max_WCC:
      ver[from_ind].add(to_ind)
      ver[to_ind].add(from_ind) 
      
print("подграф с наибольшей КСС: ", ver) 

n = 5 # кол-во вершин дя 2a 

random_v = random.sample(list(max_WCC), k=n) # мн-во вершин для 2a 
 

def dijkstra_algo(graph, start) -> int:
  d = defaultdict(bool) # расстояние от вершины старт до всех остальных 
  use = defaultdict(bool)
  d[start] = 0 
  min_d = 0 
  curr_v = start
  while min_d < math.inf:
    i = curr_v 
    use[i] = True 
    min_d = math.inf 
    path = d[i] + 1
    for j in graph[i]: 
      if (not d[j] and j != start) or path < d[j]:
        d[j] = path  

    for i in graph:
      if not use[i] and (d[i] and d[i] < min_d): 
        curr_v = i
        min_d = d[i]

  print("Расстояния ", d, "Вершина", start) 
  k = list(d.values())
  return max(k), k 



def find_eccentrisity(g, v) -> list: # поиск массива экцентрисететов g - граф, v - мн-во вершин, по которым идёт поиск 
  e = []
  e_1 = []
  for i in v: 
      m = dijkstra_algo(g, i) 
      e.append(m)
      e_1.append(m[1])
  return e, e_1


eccentricity = find_eccentrisity(ver, random_v) 
print('-------') 
matrix_of_shortest_paths = find_eccentrisity(ver, max_WCC)

print("Диаметр:", max(eccentricity[0]), "Совпадает со встроенной ф-цией?") 
print("Радиус:", min(eccentricity[0]), "Совпадает со встроенной ф-цией?") 
# Возможно неправильно 
print("90 процентиля расстояния (геодезического) между вершинами графа:", np.percentile(matrix_of_shortest_paths[1], 90)) 


#2b
def bfs_snowball(adjList, unvisited, lenght):
    WCC = set()  # weakly connected component
    queue = list()  # queue<int>
    
    src_node = unvisited.pop()
    queue.append(src_node)
    
    # loop until the queue is empty
    while queue and len(WCC) < lenght:
        # pop the front node of the queue and add it to WCC
        current_node = queue.pop(0)
        WCC.add(current_node)
        
        # check all the neighbour nodes of the current node
        for neighbour_node in adjList[current_node]:
            to = neighbour_node[0] # neighbour_node - это tuple(to, weight, time)
            if to in unvisited:
                unvisited.remove(to)
                queue.append(to)

    return WCC

n = 5 #любое число 

if len(max_WCC) > n:
    new_WCC = bfs_snowball(adjList, max_WCC, n)#третий параметр - это количество вершин, которые мы включим в множество

new_ver = defaultdict(set)

for line in dataset:
    [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
    if from_ind in new_WCC and to_ind in new_WCC:
      new_ver[from_ind].add(to_ind)
      new_ver[to_ind].add(from_ind) 

        
for i in new_WCC: 
      m = dijkstra_algo(new_ver, i)
