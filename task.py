import random
import matplotlib.pyplot as plt
import pandas
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

#filename='radoslaw_email_email.txt'
#filename='out.opsahl-ucsocial.txt'
#filename='out.soc-bitcoinalpha.txt'
#filename='out.sx-mathoverflow.txt'
#filename='out.munmun_digg_reply.txt'
#filename='test1.txt'
filename='test2.txt'

f = open(filename)
tmax=0
tmin=999999999999999

tmax=str(tmax)
tmin = str(tmin)
graph = {}
count_node = 0
count_edge = 0
edge = f.readline().split()
while edge:
    edge[0] = int(edge[0])
    edge[1] = int(edge[1])
    count_edge += 1
    if len(edge)!=2:
        if edge[3] > tmax:
            tmax = edge[3]
        if edge[3] < tmin:
            tmin = edge[3]
    if edge[0] in graph:
        if edge[0] == edge[1]:
            graph[edge[0]]['degree'] += 2
            #count_edge += 1
        elif edge[1] not in graph[edge[0]]['neigh']:
            graph[edge[0]]['neigh'].append(edge[1])
            if len(edge) != 2:
                graph[edge[0]]['time'].append(edge[3])

            graph[edge[0]]['degree'] += 1
            #count_edge += 1
    else:
        if edge[0] != edge[1]:
            if len(edge) != 2:
                graph[edge[0]] = {'neigh': [edge[1]],  'degree': 1, 'component': '', 'marker': False, 'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0,'time':[int(edge[3])]}
            else:
                graph[edge[0]] = {'neigh': [edge[1]],  'degree': 1, 'component': '', 'marker': False, 'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0}

            count_node += 1
            #count_edge += 1
        else:
            if len(edge) != 2:
                graph[edge[0]] = {'neigh': [],  'degree': 2, 'component': '', 'marker': False, 'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0,'time':[int(edge[3])]}
            else:
                graph[edge[0]] = {'neigh': [], 'degree': 2, 'component': '', 'marker': False, 'color': 'white',
                                  'dist': 0, 'Lv': 0, 'cl': 0}

            count_node += 1
           # count_edge += 1


    if edge[1] in graph:
        if edge[0] not in graph[edge[1]]['neigh'] and edge[0] != edge[1]:
            graph[edge[1]]['neigh'].append(edge[0])
            if len(edge)!=2:
                graph[edge[1]]['time'].append(edge[3])

            graph[edge[1]]['degree'] += 1
    else:
        if len(edge) != 2:
            graph[edge[1]] = {'neigh': [edge[0]],  'degree': 1, 'component': '', 'marker': False, 'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0,'time':[int(edge[3])]}
        else:
            graph[edge[1]] = {'neigh': [edge[0]],  'degree': 1, 'component': '', 'marker': False, 'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0}

        count_node += 1


    edge = f.readline().split()
f.close()

print('############################################')
print('task 1.1: ')
print('Count nodes: ', count_node)
print('Count edges: ', count_edge)
print('Density: ', (2*count_edge)/(count_node*(count_node-1)))

print('############################################')

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
print('task 1.2a')
print('Random sample')

comp=max_comp
node500 = random.sample(comp, max_node_comp[0])

d = []
d_all = []
for i in node500:
    graph[i]['color'] = 'grey'
    d_max = 0
    qq = [i]
    graph[i]['dist'] = 0
    while qq:
        a = qq[0]
        qq.pop(0)
        for i in graph[a]['neigh']:
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

####

print('############################################')
print('task 1.2a')
print('Snowball sample')
comp=max_comp
node500 = []
snow=0
for o in graph:
    if snow > 100:
        break
    for p in graph[o]['neigh']:
        node500.append(p)
        snow+=1
        if snow>100:
            break

d = []
d_all = []
for i in node500:
    graph[i]['color'] = 'grey'
    d_max = 0
    qq = [i]
    graph[i]['dist'] = 0
    while qq:
        a = qq[0]
        qq.pop(0)
        for i in graph[a]['neigh']:
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
####
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

print('############################################')
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



df = pandas.DataFrame({'def':[],'uv':[], 'cn': [],'aa': [],'jk': [],'pa':[]})
ds = pandas.DataFrame({'def':[],'uv':[], 'aawl': [],'aawe': [],'aaws': [],'cnwl': [],'cnwe': [],'cnws': [],'jkwe': [],'jkwl': [],'jkws': [],'pawe':[],'pawl':[],'paws':[]})
dt = pandas.DataFrame({'def':[],'uv':[], 'aawe': [],'cnwe': [],'jcwe': [],'pawe':[], 'aawl': [], 'cnwl': [], 'jcwl': [], 'pawl': [], 'aaws': [], 'cnws': [], 'jcws': [], 'paws': []})


l=0.2
#wl=l+(1-l)*(t-tmin)/(tmax-tmin)
#we=l+(1-l)*(math.exp(3*(t-tmin)/(tmax-tmin))-1)/(math.e**3-1)
#ws=l+(1-l)/(math.sqrt((t-tmin)/(tmax-tmin)))
tmax=int(tmax)
tmin=int(tmin)


def wtfe(graph,a,b,tmin,tmax):
    t = int(graph[a]['time'][b])
    return l+(1-l)*(t-tmin)/(tmax-tmin)
def wtfl(graph,a,b,tmin,tmax):
    t=int(graph[a]['time'][b])
    return l+(1-l)*(math.exp(3*(t-tmin)/(tmax-tmin))-1)/(math.e**3-1)
def wtfs(graph,a,b,tmin,tmax):
    t=int(graph[a]['time'][b])
    return l+(1-l)*(math.sqrt((t-tmin)/(tmax-tmin)))

sw=0
se=0
"""
for i in graph:
    for j in graph:
        cn = 0
        aa=3
        jc=0
        pa=0

        z = []
        aawe = 0
        pawe1=0
        pawe2=0
        jcwe=0
        cnwe=0

        aawl = 0
        pawl1=0
        pawl2=0
        jcwl=0
        cnwl=0

        aaws = 0
        paws1 = 0
        paws2 = 0
        jcws = 0
        cnws = 0

        for t in graph[i]['neigh']:
            for k in graph[j]['neigh']:
                if t == k:
                    z.append(t)

        for t2 in graph[j]['neigh']:
            pawl2 += wtfl(graph, j, graph[j]['neigh'].index(t2), tmin, tmax)
            pawe2 += wtfe(graph, j, graph[j]['neigh'].index(t2), tmin, tmax)
            paws2 += wtfs(graph, j, graph[j]['neigh'].index(t2), tmin, tmax)
        for t1 in graph[i]['neigh']:
            pawe1 += wtfe(graph,i, graph[i]['neigh'].index(t1),tmin,tmax)
            pawl1 += wtfl(graph, i, graph[i]['neigh'].index(t1), tmin, tmax)
            paws1 += wtfs(graph, i, graph[i]['neigh'].index(t1), tmin, tmax)

        for t in graph[i]['neigh']:
            for k in graph[j]['neigh']:
                if t==k:

                    cn+=1

                    zi = graph[i]['neigh'].index(t)
                    zj = graph[j]['neigh'].index(t)

                    aawet1 = wtfe(graph, i, zi, tmin, tmax) + wtfe(graph, j, zj, tmin, tmax)
                    aawlt1 = wtfl(graph, i, zi, tmin, tmax) + wtfe(graph, j, zj, tmin, tmax)
                    aawst1 = wtfs(graph, i, zi, tmin, tmax) + wtfe(graph, j, zj, tmin, tmax)

                    aawet2=0
                    aawlt2 = 0
                    aawst2 = 0


                    jcwe += aawet1 / (pawe1+pawe2)
                    jcwl += aawlt1 / (pawl1 + pawl2)
                    jcws += aawst1 / (paws1 + paws2)


                    for l in z:
                        if l in graph[t]['neigh']:
                            zj2 = graph[t]['neigh'].index(l)
                            aawet2+=wtfe(graph,t,zj2,tmin,tmax)
                            aawlt2 += wtfl(graph, t, zj2, tmin, tmax)
                            aawst2 += wtfs(graph, t, zj2, tmin, tmax)



                    cnwe += aawet1
                    cnwl += aawlt1
                    cnws += aawst1

                    if aawet2 != 0:
                        aawe += aawet1 / aawet2
                    if aawlt2 != 0:
                        aawl += aawlt1 / aawlt2
                    if aawst2 != 0:
                        aaws += aawst1 / aawst2

                    if aawet2!=0:
                        aawet2=math.log(1+aawet2)
                    if aawlt2!=0:
                        aawlt2=math.log(1+aawlt2)
                    if aawst2 != 0:
                        aawst2 = math.log(1 + aawst2)



                    if graph[t]['degree']!=1:
                        aa+=1/math.log(graph[t]['degree'])

        pawe = pawe1 * pawe2
        pawl = pawl1 * pawl2
        paws = paws1 * paws2


        jk=cn/(graph[i]['degree']+graph[j]['degree']-cn)
        pa=graph[i]['degree']*graph[j]['degree']
        if j in graph[i]['neigh']:
            newDict = {'def': 1, 'uv': {i,j}, 'cn': cn, 'aa': aa, 'jk': jk, 'pa': pa}
        else:
            newDict = {'def': 0, 'uv': {i,j}, 'cn': cn, 'aa': aa, 'jk': jk, 'pa': pa}
        df = pandas.concat([df, pandas.DataFrame([newDict])], ignore_index=True)

        if j in graph[i]['neigh']:
            newDict1 = {'def': 1, 'uv': {i, j}, 'cnwe': cnwe, 'aawe': aawe, 'jcwe': jcwe, 'pawe': pawe, 'cnwl': cnwe, 'aawl': aawe, 'jcwl': jcwe, 'pawl': pawe, 'cnws': cnwe, 'aaws': aawe, 'jcws': jcwe, 'paws': pawe}
        else:
            newDict1 = {'def': 0, 'uv': {i, j}, 'cnwe': cnwe, 'aawe': aawe, 'jcwe': jcwe, 'pawe': pawe, 'cnwl': cnwe, 'aawl': aawe, 'jcwl': jcwe, 'pawl': pawe, 'cnws': cnwe, 'aaws': aawe, 'jcws': jcwe, 'paws': pawe}
        dt = pandas.concat([dt, pandas.DataFrame([newDict1])], ignore_index=True)"""



for i in graph:
    for j in graph:
        cn = 0
        aa=3
        jc=0
        pa=0


        for t in graph[i]['neigh']:
            for k in graph[j]['neigh']:
                if t==k:

                    cn+=1

                    if graph[t]['degree']!=1:
                        aa+=1/math.log(graph[t]['degree'])


        jk=cn/(graph[i]['degree']+graph[j]['degree']-cn)
        pa=graph[i]['degree']*graph[j]['degree']
        if j in graph[i]['neigh']:
            newDict = {'def': 1, 'uv': {i,j}, 'cn': cn, 'aa': aa, 'jk': jk, 'pa': pa}
        else:
            newDict = {'def': 0, 'uv': {i,j}, 'cn': cn, 'aa': aa, 'jk': jk, 'pa': pa}
        df = pandas.concat([df, pandas.DataFrame([newDict])], ignore_index=True)



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

print(df.loc[1])

plt.show()

"""
X = dt[['cnwe', 'aawe','jcwe','pawe','cnwl','aawl','jcwl','pawl','cnwl','cnws','aaws','jcws','paws']]
y = dt['def']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=0)
log_regression = LogisticRegression()
log_regression.fit(X_train,y_train)
y_pred = log_regression.predict(X_test)



y_pred_proba = log_regression.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
plt.plot(fpr,tpr,label="AUC="+str(auc))
plt.legend(loc=4)

print('task 2.2')
print("AUC II-b:",str(auc))
plt.show()
"""