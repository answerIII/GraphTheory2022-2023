import numpy as np 
import math 
from collections import defaultdict

# A 

def temporal_weight(t_arr, t_min, t_max) -> (dict):

  t_weight = defaultdict(list)

  l = 0.2 
  t_minmax = t_max - t_min
  for t in t_arr: 

    tt = (t-t_min)/(t_minmax) 

    t_weight['linear'].append(l + (1-l)*(tt))
    t_weight['exponential'].append(l + (1-l)*((math.exp(3*tt) - 1) / (math.exp(3) - 1)))
    t_weight['square root'].append(l + (1-l)*(tt**0.5))


  return t_weight 

# B 

def past_event_aggregation(weight) -> (dict): 

  a = {}

  a['zeroth'], a['first'], a['second'], a['third'], a['fourth quantile'] = np.quantile(weight, [0, 0.25, 0.5, 0.75, 1])
   
  a['sum'] = sum(weight) 
  a['mean'] = np.mean(weight)
  a['variance'] = np.var(weight) 
  
  return a 
  
# C 


def CN_temporal(u, v, z_arr, graph, number) -> (list): 
  CN = np.zeros(len(graph[u][v]['weight'][number]))

  for z in z_arr: 
    CN = CN + np.array(graph[u][z]['weight'][number]) + np.array(graph[v][z]['weight'][number])  

  return CN 
  
def JC_temporal(u, v, z_arr, graph, number) -> list: 
  n =  len(graph[u][v]['weight'][number])
  x = np.zeros(n)
  y = np.zeros(n)
  JC = np.zeros(n) 

  for i in graph[u]: 
    x += np.array(graph[u][i]['weight'][number]) 

  for i in graph[v]: 
    y += np.array(graph[v][i]['weight'][number])

  tmp = x + y 
  for z in z_arr: 
    JC = JC + (np.array(graph[u][z]['weight'][number]) + np.array(graph[v][z]['weight'][number])) / tmp 
  return JC 

# sum([1,2,3], [4,5,6])


def PA_temporal(u, v, graph, number) -> (list):
  n = len(graph[u][v]['weight'][number])
  PA = np.zeros(n) 
  x = np.zeros(n)
  y = np.zeros(n)

  for i in graph[u]: 
    x += np.array(graph[u][i]['weight'][number]) 

  for i in graph[v]: 
    y += np.array(graph[v][i]['weight'][number])
  
  PA = x * y 

  return PA 

def topological_features(u, v, graph, number) -> list: 
  u_neigh = set(graph[u]) 
  v_neigh = set(graph[v]) 
  z_arr = list(u_neigh & v_neigh) 
  if len(z_arr) > 0:
    AA = AA_temporal(u, v, z_arr, graph, number) 
    CN = CN_temporal(u, v, z_arr, graph, number) 
    JC = JC_temporal(u, v, z_arr, graph, number)
  else: 
    n = len(graph[u][v]['weight'][number])
    AA, CN, JC = [0]*n, [0]*n, [0]*n

  PA = PA_temporal(u, v, graph, number)

  print(AA)
  print(CN)
  print(JC)
  print(PA) 

  features = list(AA) + list(CN) + list(JC) + list(PA)

  return features 
  
