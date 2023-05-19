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

random_v = random.choices(list(max_WCC), k=n) # мн-во вершин для 2a 
 

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
  return max(k) 



def find_eccentrisity(g, v) -> list: # поиск массива экцентрисететов g - граф, v - мн-во вершин, по которым идёт поиск 
  e = []
  for i in v: 
      m = dijkstra_algo(g, i) 
      e.append(m) 
  return e


eccentricity = find_eccentrisity(ver, random_v) 

print("Диаметр:", max(eccentricity), "Совпадает со встроенной ф-цией?") 
print("Радиус:", min(eccentricity), "Совпадает со встроенной ф-цией?") 
# Возможно неправильно 
print("90 процентиля расстояния (геодезического) между вершинами графа:", np.percentile(eccentricity_r, 90)) 
