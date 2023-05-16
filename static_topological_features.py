import math
import pandas as pd
import numpy as np

def calc_stf(file):
    def intersection_list(list1, list2):
        return set(list1).intersection(list2)
    def union_list(list1,list2):
        return set(list1+list2)

    file_path = 'datasets/' + file + '.csv'
    data = pd.read_csv(file_path, sep="\t")
    dvudol = 0
    if file[-9] == '1':
        dvudol = 1
    AllEdges = []
    AllTime = []
    AllVertex = {}
    for index, row in data.iterrows():
        if row['in'] == row['out']:
            continue
        left = AllVertex.get(row['in'])
        if left:
            if (row['out']) in left or row['in']==row['out']:
                continue
            else:
                left.append(row['out'])
                AllVertex[row['in']] = left
        else:
            AllVertex[row['in']] = [row['out']]

        right = AllVertex.get(row['out'])
        if right:
            if row['in'] in right or row['in']==row['out']:
                continue
            else:
                right.append(row['in'])
                AllVertex[row['out']] = right
        else:
            AllVertex[row['out']] = [row['in']]

        AllEdges.append([int(row['in']), int(row['out']), int(row['time'])])
        AllTime.append(row['time'])

    tmin = min(AllTime)
    tmax = max(AllTime)
    q = np.percentile(AllTime, 50)

    X = []
    Y = []
    inData = set([])
    for edge in AllEdges:
        #if edge[2] > q:
            list1 = AllVertex.get(edge[0])
            list2 = AllVertex.get(edge[1])
            CN = intersection_list(list1,list2)
            AA = 0
            for vertex in CN:
                AA += 1/math.log(len(AllVertex.get(vertex)))
            JC = len(CN)/len(union_list(list1, list2))
            PA = len(list1)*len(list2)

            X.append([len(CN), AA, JC, PA])
            Y.append(1)
            inData.add(str(edge[0])+str(edge[1]))
            inData.add(str(edge[1])+str(edge[0]))
        #else:
            right = AllVertex.get(edge[1])
            left = AllVertex.get(edge[0])
            was_found = False
            for neigh in right:
                if neigh not in left and (str(edge[0])+str(neigh)) not in inData and (str(neigh)+str(edge[0])) not in inData \
                        and int(edge[0])*int(neigh)*dvudol <= 0:
                    list1 = AllVertex.get(edge[0])
                    list2 = AllVertex.get(neigh)
                    CN = intersection_list(list1, list2)
                    AA = 0
                    for vertex in CN:
                        if neigh == edge[0]:
                            continue
                        AA += 1 / math.log(len(AllVertex.get(vertex)))
                    JC = len(CN) / len(union_list(list1, list2))
                    PA = len(list1) * len(list2)
                    X.append([len(CN), AA, JC, PA])
                    Y.append(0)
                    inData.add(str(edge[0]) + str(neigh))
                    inData.add(str(neigh) + str(edge[0]))
                    was_found = True
                    break
            for neigh in left:
                if was_found:
                    break
                if neigh not in right and (str(edge[1])+str(neigh)) not in inData and (str(neigh)+str(edge[1])) not in inData \
                        and int(edge[1])*int(neigh)*dvudol <= 0:
                    list1 = AllVertex.get(edge[1])
                    list2 = AllVertex.get(neigh)
                    CN = intersection_list(list1, list2)
                    AA = 0
                    for vertex in CN:
                        if neigh == edge[1]:
                            continue
                        AA += 1 / math.log(len(AllVertex.get(vertex)))
                    JC = len(CN) / len(union_list(list1, list2))
                    PA = len(list1) * len(list2)
                    X.append([len(CN), AA, JC, PA])
                    Y.append(0)
                    inData.add(str(edge[1]) + str(neigh))
                    inData.add(str(neigh) + str(edge[1]))
                    was_found = True
                    break

    return (X,Y)


