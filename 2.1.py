import pandas as pd
import math
import random
import numpy as np
from collections import deque
import collections

# dataset_path = 'datasets/' + 'test' + '.txt'
dataset_path = 'datasets/' + 'out.radoslaw_email_email' + '.txt'
# dataset_path = 'datasets/' + 'out.prosper-loans' + '.txt'
data = pd.read_csv(dataset_path, sep='\s+', names=['id_from', 'id_to', 'weight', 'time'], header=None)

def get_adjacency_list(data):
    adjacency_list = dict({})
    edges = set()
    time = []
    for row in data.itertuples():
        # if row[4] >= t0 and row[4] <= t1:
        if(row[1] in adjacency_list):
            if(row[2] not in adjacency_list[row[1]]):
                adjacency_list[row[1]].append(row[2])
        else:
            adjacency_list[row[1]] = [row[2]]
        if(row[2] in adjacency_list):
            if(row[1] not in adjacency_list[row[2]]):
                adjacency_list[row[2]].append(row[1])
        else:
            adjacency_list[row[2]] = [row[1]]
        if (row[1], row[2]) not in edges and (row[2], row[1]) not in edges:
            edges.add((row[1], row[2]))
        time.append(row[4])
    return [adjacency_list, min(time), max(time), edges]

def floyd_warshall(adjacency_list):
    d = [[[] for _ in range(len(adjacency_list))] for __ in range(len(adjacency_list))]
    for node_1 in adjacency_list:
        for node_2 in adjacency_list:
            d[list(adjacency_list).index(node_1)][list(adjacency_list).index(node_2)] = [math.inf, node_1, node_2]

    for node in adjacency_list:
        for neighbour in adjacency_list[node]:
            d[list(adjacency_list).index(node)][list(adjacency_list).index(neighbour)] = [1, node, neighbour]

    for i in range(len(d)):
        d_i = [d[j][:] for j in range(len(d))]
        for u in range(len(d)):
            for v in range(len(d)):
                d[u][v][0] = min(d_i[u][v][0], d_i[u][i][0] + d_i[i][v][0])

    for i in range(len(d)):
        d[i][i][0] = 0
    return d

def common_neighbours(u, v, adjacency_list):
    return len(set(adjacency_list[u]) & set(adjacency_list[v]))

def adamic_adar(u, v, adjacency_list):
    Z = set(adjacency_list[u]) & set(adjacency_list[v])
    AA = 0
    for z in Z:
        AA += 1 / math.log(len(adjacency_list[z]))
    return AA

def jaccard_coefficient(u, v, adjacency_list):
    return len(set(adjacency_list[u]) & set(adjacency_list[v])) / len(set(adjacency_list[u]) | set(adjacency_list[v]))

def preferential_attachment(u, v, adjacency_list):
    return len(adjacency_list[u]) * len(adjacency_list[v])

adjacency_list, tmin, tmax, edges = get_adjacency_list(data)
d = [[[math.inf, node, neighbour] for neighbour in adjacency_list[node]] for node in adjacency_list]
pairs_v_dist_2 = set()
d = floyd_warshall(adjacency_list)

for i in range(len(d)):
    for j in range(len(d)):
        if d[i][j][0] == 2 and ((d[i][j][1], d[i][j][2]) not in pairs_v_dist_2) and ((d[i][j][2], d[i][j][1]) not in pairs_v_dist_2):
            pairs_v_dist_2.add((d[i][j][1], d[i][j][2]))

all_pairs_edges = set()
for i in range(1, len(adjacency_list)):
    for j in range(i+1, len(adjacency_list)):
        all_pairs_edges.add((i, j))

remaining_pairs = all_pairs_edges - pairs_v_dist_2

positives = set()
negatives = set()
for pair in remaining_pairs:
    if (pair[1] in adjacency_list[pair[0]]) and len(positives) < 10000:
        positives.add(pair)
    elif len(negatives) < 10000:
        negatives.add(pair)

X = []
Y = []
for pair in pairs_v_dist_2:
    CN = common_neighbours(pair[0], pair[1], adjacency_list)
    AA = adamic_adar(pair[0], pair[1], adjacency_list)
    JC = jaccard_coefficient(pair[0], pair[1], adjacency_list)
    PA = preferential_attachment(pair[0], pair[1], adjacency_list)
    X.append([CN, AA, JC, PA])
    Y.append(0)

for pair in positives:
    CN = common_neighbours(pair[0], pair[1], adjacency_list)
    AA = adamic_adar(pair[0], pair[1], adjacency_list)
    JC = jaccard_coefficient(pair[0], pair[1], adjacency_list)
    PA = preferential_attachment(pair[0], pair[1], adjacency_list)
    X.append([CN, AA, JC, PA])
    Y.append(1)

for pair in negatives:
    CN = common_neighbours(pair[0], pair[1], adjacency_list)
    AA = adamic_adar(pair[0], pair[1], adjacency_list)
    JC = jaccard_coefficient(pair[0], pair[1], adjacency_list)
    PA = preferential_attachment(pair[0], pair[1], adjacency_list)
    X.append([CN, AA, JC, PA])
    Y.append(0)

    
    
# Получения списка ребер
edges_r = dict({})
for row in data.itertuples():
    if (row[1]<row[2]):
        fir=row[1]
        sec=row[2]
    else:
        fir = row[2]
        sec = row[1]
    if (fir, sec) in edges_r:
        edges_r[(fir, sec)].append(row[4])
    else:
        edges_r[(fir, sec)] = [row[4]]

ver_count=len(adjacency_list)
print(ver_count)

s=(tmax-tmin)/2
print(tmin,tmax,s)

# Все ребра которых небыло до s
edges_p=[]
edges_n=[]
for i in range(1, ver_count):
    for j in range(i+1, ver_count):
        if (j in adjacency_list[i]):
            if (min(edges_r[(i,j)])>=s):
                edges_p.append((i, j))
        else:
            edges_n.append((i,j))
# Ограничить расстоянием

# Заменить ребра на
for i in range(len(edges_p)):
    CN = common_neighbours(edges_p[i][0], edges_p[i][1], adjacency_list)
    AA = adamic_adar(edges_p[i][0], edges_p[i][1], adjacency_list)
    JC = jaccard_coefficient(edges_p[i][0], edges_p[i][1], adjacency_list)
    PA = preferential_attachment(edges_p[i][0], edges_p[i][1], adjacency_list)
    edges_p[i]=[CN, AA, JC, PA]

for i in range(len(edges_n)):
    CN = common_neighbours(edges_n[i][0], edges_n[i][1], adjacency_list)
    AA = adamic_adar(edges_n[i][0], edges_n[i][1], adjacency_list)
    JC = jaccard_coefficient(edges_n[i][0], edges_n[i][1], adjacency_list)
    PA = preferential_attachment(edges_n[i][0], edges_n[i][1], adjacency_list)
    edges_n[i]=[CN, AA, JC, PA]

X_new=edges_n + edges_p;
Y_new=[0]*len(edges_n)+[1]*len(edges_p);
# Делим 25% тестовых
model = LogisticRegression()
X_train, X_test, Y_train, Y_test = train_test_split(X_new, Y_new, test_size=0.25, random_state=0)
# Обучение
model.fit(X_train, Y_train)
accuracy = accuracy_score(Y_test, model.predict(X_test))
auc_roc = roc_auc_score(Y_test, model.predict_proba(X_test)[:, 1])
print(classification_report(Y_test, model.predict(X_test)))
svc_disp = RocCurveDisplay.from_estimator(model, X_test, Y_test)
plt.show()
    
