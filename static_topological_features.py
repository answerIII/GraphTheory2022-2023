import math
import pandas as pd
import numpy as np
import random

def calc_stf(file, q):
    def intersection_list(list1, list2):
        return set(list1).intersection(list2)
    def union_list(list1,list2):
        return set(list1+list2)

    file_path = 'datasets/' + file + '.csv'
    data = pd.read_csv(file_path, sep="\t")
    dvudol = 0
    if file[-9] == '1':
        dvudol = 1
    AllEdges = {}
    AllTime = []
    AllVertex = {}

    #Сохранение ребер и времени первого их появления
    for index, row in data.iterrows():
        if row['in'] == row['out']:
            continue
        first_variant = AllEdges.get((str(row['in']) + '_' + str(row['out'])))
        second_variant = AllEdges.get((str(row['out']) + '_' + str(row['in'])))
        if first_variant:
            first_variant = min(first_variant, int(row['time']))
            AllEdges[(str(row['in']) + '_' + str(row['out']))] = first_variant
        elif second_variant:
            second_variant = min(second_variant, int(row['time']))
            AllEdges[(str(row['out']) + '_' + str(row['in']))] = second_variant
        else:
            AllEdges[(str(row['in']) + '_' + str(row['out']))] = int(row['time'])
        AllTime.append(int(row['time']))

    bound = np.percentile(AllTime, q)

    #Создание списков смежности для данного отрезка времени
    for edge in AllEdges.keys():
        u, v = map(str, edge.split('_'))
        time = AllEdges[edge]
        if u == v or time >= bound:
            continue
        left = AllVertex.get(u)
        if left:
            if v in left:
                continue
            else:
                left.append(v)
                AllVertex[u] = left
        else:
            AllVertex[u] = [v]

        right = AllVertex.get(v)
        if right:
            if u in right:
                continue
            else:
                right.append(u)
                AllVertex[v] = right
        else:
            AllVertex[v] = [u]

    X = []
    Y = []
    keys = list(AllEdges.keys())
    for _ in range(10000):
            # Вычисляем признаки для ребра, которое появится
            edge = random.choice(keys)
            time = AllEdges[edge]
            if time < bound:
                continue
            list1 = AllVertex.get(edge.split('_')[0])
            list2 = AllVertex.get(edge.split('_')[1])
            if not(list2) or not(list1):
                continue
            CN = intersection_list(list1,list2)
            AA = 0
            for vertex in CN:
                AA += 1/math.log(len(AllVertex.get(vertex)))
            JC = len(CN)/len(union_list(list1, list2))
            PA = len(list1)*len(list2)

            X.append([len(CN), AA, JC, PA])
            Y.append(1)

            # Вычисляем признаки для ребра, которое не появится
            was_found = False
            repeat = 0
            while was_found == False and repeat < 100:
                rand_u = random.choice(list(AllVertex.keys()))
                nbs_u = AllVertex.get(rand_u)
                nb_u = random.choice(nbs_u)
                rand_v = random.choice(AllVertex.get(nb_u))
                first_variant = str(rand_u) + '_' + str(rand_v)
                second_variant = str(rand_v) + '_' + str(rand_u)
                repeat += 1
                if (first_variant) and (second_variant) and \
                        int(rand_u) * int(rand_v) * dvudol <= 0 and not (AllEdges.get(second_variant)) \
                        and not(AllEdges.get(first_variant)) and rand_v not in nbs_u and rand_v!=rand_u:

                    list1 = AllVertex.get(rand_u)
                    list2 = AllVertex.get(rand_v)
                    CN = intersection_list(list1, list2)
                    AA = 0
                    for vertex in CN:
                        AA += 1 / math.log(len(AllVertex.get(vertex)))
                    JC = len(CN) / len(union_list(list1, list2))
                    PA = len(list1) * len(list2)
                    X.append([len(CN), AA, JC, PA])
                    Y.append(0)
                    was_found = True
                    break
    return (X,Y)


