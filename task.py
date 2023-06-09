import random
import matplotlib.pyplot as plt
import pandas
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics




def rgraph(filename):
    f = open(filename)
    graph = {}
    count_node = 0
    count_edge = 0
    edge = f.readline().split()
    while edge:
        if len(edge) != 1:
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            count_edge += 1
            if edge[0] in graph:
                if edge[0] == edge[1]:
                    graph[edge[0]]['neigh'].append(edge[1])
                    graph[edge[0]]['degree'] += 2
                    print(edge[0])
                elif edge[1] not in graph[edge[0]]['neigh']:
                    graph[edge[0]]['neigh'].append(edge[1])
                    graph[edge[0]]['degree'] += 1
            else:
                if edge[0] != edge[1]:
                    graph[edge[0]] = {'neigh': [edge[1]], 'degree': 1, 'component': '', 'marker': False,
                                      'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0}
                    count_node += 1
                else:
                    graph[edge[0]] = {'neigh': [edge[0]], 'degree': 2, 'component': '', 'marker': False, 'color': 'white',
                                      'dist': 0, 'Lv': 0, 'cl': 0}
                    count_node += 1
                    print(edge[0])
            if edge[1] in graph:
                if edge[0] not in graph[edge[1]]['neigh'] and edge[0] != edge[1]:
                    graph[edge[1]]['neigh'].append(edge[0])
                    graph[edge[1]]['degree'] += 1
            else:
                graph[edge[1]] = {'neigh': [edge[0]], 'degree': 1, 'component': '', 'marker': False, 'color': 'white',
                                  'dist': 0, 'Lv': 0, 'cl': 0}
                count_node += 1
        edge = f.readline().split()
    f.close()
    return graph,count_node,count_edge








#filename='radoslaw_email_email.txt'
#filename='out.opsahl-ucsocial.txt'
#filename='out.soc-bitcoinalpha.txt'
#filename='out.sx-mathoverflow.txt'
#filename='out.munmun_digg_reply.txt'
#filename='test1.txt'
#filename='test2.txt'
#filename='testgraph_3.txt'
#filename='testgraph_4.txt'
filename='testgraph_5.txt'
#filename='testgraph_6.txt'
#filename='testgraph_7.txt'
#filename='team_16.txt'
graph,count_node,count_edge=rgraph(filename)
print('############################################')
print('task 1.1: ')
print('Count nodes: ', count_node)
print('Count edges: ', count_edge)
print('Density: ', (2*count_edge)/(count_node*(count_node-1)))
######################################################################################
"""
stack = []
number_comp = 1
max_node_comp = [0,0]
compt = []
for b in graph:
    node = 0
    if not graph[b]['marker']:
        stack.insert(0, b)
        node += 1
        compt = [b]
        graph[b]['marker'] = True
        graph[b]['component'] = number_comp
        while stack:
            c = False
            for i in graph[stack[0]]['neigh']:
                if not graph[i]['marker']:
                    graph[i]['marker'] = True
                    graph[i]['component'] = number_comp
                    stack.insert(0, i)
                    compt.append(i)
                    node += 1
                    c = True
                    break

            if not c:
                stack.pop(0)
        number_comp += 1
        if max_node_comp[0] < node:
            max_node_comp[0] = node
            max_node_comp[1] = number_comp - 1
            max_comp = compt
number_comp=number_comp-1

print('Count components: ', number_comp)
print('Number nodes: ', max_node_comp[0])
print('Fraction of nodes: ', max_node_comp[0]/count_node)
print('############################################')
print('task 1.2')
print('Random sample')

comp=max_comp
node500 = comp#random.sample(comp, 500)

d = []
d_all = []
for l in node500:
    graph[l]['color'] = 'grey'
    d_max = 0
    qq = [l]
    graph[l]['dist'] = 0
    while qq:
        a = qq[0]
        qq.pop(0)
        for i in graph[a]['neigh']:
            #if i in node500:
                if graph[i]['color'] == 'white':
                    graph[i]['color'] = 'grey'
                    graph[i]['dist'] = graph[a]['dist'] + 1
                    d1 = graph[i]['dist']
                    d_all.append(d1)
                    qq.append(i)
                    if d_max < d1:
                        d_max = d1
                else:
                    graph[a]['color'] = 'black'

    for j in comp:
        graph[j]['color'] = 'white'
    d.append(d_max)
d.sort()
d_all.sort()

print('Diameter: ', max(d))
print('Radius: ', min(d))
print('90 percentile: ', d_all[round(0.9*len(d_all))])


print('############################################')
""""""
C = 0
for i in graph:
    n = len(graph[i]['neigh'])
    C += (n*(n-1))/2

Cl_medium = 0

cc = 0
for i in graph:
    cc = 0
    for k in graph[i]['neigh']:
        for l in graph[i]['neigh']:
            if k in graph[l]['neigh']:
                cc+=1
    graph[i]['Lv']=cc*3

for i in graph:
    t = int(graph[i]['Lv']/6)
    graph[i]['Lv'] = t
    n = len(graph[i]['neigh'])
    if n >= 2:
        graph[i]['cl'] = (2*t)/(n*(n-1))
    c = graph[i]['cl']
    Cl_medium += c

Cl_medium = Cl_medium/count_node


print('task 1.3')
print('Average cluster network  coefficient: ', Cl_medium)

print('############################################')

r1=0
r2=0
r3=0
re=0
m=0
for i in graph:
    m+=graph[i]['degree']
for i in graph:
    r1 += graph[i]['degree']
    r2 += graph[i]['degree'] * graph[i]['degree']
    r3 += graph[i]['degree'] * graph[i]['degree'] * graph[i]['degree']
    for j in graph[i]['neigh']:
        re+=graph[i]['degree']*graph[j]['degree']
r=(re*r1-r2*r2)/(r3*r1-r2*r2)

print('task 1.4')
print('Assortative factor: ',r)

print('############################################')
"""

df = pandas.DataFrame({'def':[],'u':[],'v':[], 'cn': [],'aa': [],'jk': [],'pa':[]})


l=0.2
#wl=l+(1-l)*(t-tmin)/(tmax-tmin)
#we=l+(1-l)*(math.exp(3*(t-tmin)/(tmax-tmin))-1)/(math.e**3-1)
#ws=l+(1-l)/(math.sqrt((t-tmin)/(tmax-tmin)))

for i in graph:
    for j in graph:
        cn=0
        aa=0
        jc=0
        pa=0

        jk=len(graph[j]['neigh'])
        for k in graph[i]['neigh']:
            if k in graph[j]['neigh']:
                cn+=1
                if graph[k]['degree']!=1:
                    aa+=1/math.log(graph[k]['degree'])

        for k in graph[i]['neigh']:
            if k not in graph[j]['neigh']:
                jk+=1

        jk = cn / jk
        pa=graph[i]['degree']*graph[j]['degree']
        if j in graph[i]['neigh']:
            newDict = {'def': 1, 'u': i, 'v': j, 'cn': cn, 'aa': aa, 'jk': jk, 'pa': pa}
            if (i==1 and j==2) or (i==2 and j==1):
                print(newDict)
        else:
            newDict = {'def': 0, 'u': i, 'v': j, 'cn': cn, 'aa': aa, 'jk': jk, 'pa': pa}
            if (i==1 and j==2) or (i==2 and j==1):
                print(newDict)
        df = pandas.concat([df, pandas.DataFrame([newDict])], ignore_index=True)
        print(newDict)

print('start log')
X = df[['cn', 'aa','jk','pa']]
y = df['def']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
log_regression = LogisticRegression()
log_regression.fit(X_train,y_train)
y_pred = log_regression.predict(X_test)
y_pred_proba = log_regression.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.legend(loc=4)
print('task 2.1')
print("AUC I:",str(auc))
#print(df.loc[(df['u'] == 1)&(df.loc[df['v'] == 2])])

print(df.loc[1])

plt.show()
