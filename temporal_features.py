import numpy as np 
import math 
from collections import defaultdict
import networkx as nx

# A 
def calc_temporate_feauters(dataset, qs):

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
    b = False
    if tmp[-1] == 0:
      tmp[-1] = 1 #?????
      b = True
    for z in z_arr:
      JC = JC + (np.array(graph[u][z]['weight'][number]) + np.array(graph[v][z]['weight'][number])) / tmp
    if b:
      JC[-1] = 0
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

  def AA_temporal(u, v, z_arr, graph, number) -> (list):
    n =  len(graph[u][v]['weight'][number])
    AA = np.zeros(n)
    sum_x = np.zeros(n)

    for z in z_arr:
      x = graph[z]

      for x1 in x:
        sum_x += np.array(graph[z][x1]['weight'][number])

      b = False

      if sum_x[-1] == 0:
         sum_x[-1] = 0.0001
         tmp = AA[-1]
         b = True

      AA = AA + (np.array(graph[u][z]['weight'][number]) + np.array(graph[v][z]['weight'][number])) / np.log(1 + sum_x)
      # print("AA", AA)
      # print('log', np.log(1 + sum_x))
      sum_x = np.zeros(n)
      if b:
        AA[-1] = tmp

    return AA

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

    # print(AA)
    # print(CN)
    # print(JC)
    # print(PA)

    features = list(AA) + list(CN) + list(JC) + list(PA)

    return features

  ver = defaultdict(list)
  all_time = []
  ver_after = []

  for line in dataset:
      [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
      all_time.append(time)
      if time <= qs: 
        ver[(min(from_ind, to_ind), max(from_ind, to_ind))].append(time)
      else:
        ver_after.append([from_ind, to_ind])

  t_min = min(all_time)
  t_max = max(all_time)


  # for key, value in ver.items():
  #   print(key, ":" ,value)

  for key, value in ver.items():
    ver[key] = list(set(value))


  G = nx.Graph()

  weight_liner = defaultdict(list)

  for uv in ver:
    w = temporal_weight(ver[uv], t_min, t_max)
    weight_liner = past_event_aggregation(w['linear'])
    weight_exponetial = past_event_aggregation(w['exponential'])
    weight_square = past_event_aggregation(w['square root'])

    G.add_edge(uv[0], uv[1], weight = [list(weight_liner.values())])
    G[uv[0]][uv[1]]['weight'] += [list(weight_exponetial.values())]
    G[uv[0]][uv[1]]['weight'] += [list(weight_square.values())]

  ver.clear()
  for i in range(3):
    for j in G.edges:
      ver[(j[0], j[1])] += topological_features(j[0], j[1], G, i)

  y = [0] * len(ver)
  j = 0
  print("len(ver):", len(ver))
  print("len(ver_after):", len(ver_after))

  for i in ver:
    if ([i[0], i[1]] in ver_after) or ([i[1],i[0]] in ver_after):
      y[j] = 1
    j += 1

  print("y.count(1):", y.count(1))
  print("y.count(0):", y.count(0))

  return ver, y
