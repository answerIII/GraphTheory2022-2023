import random
import matplotlib.pyplot as plt
import pandas
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy



def rgraph(filename):
    f = open(filename)
    graph = {}
    count_node = 0
    count_edge = 0
    edge = f.readline().split()
    tmax=1000000000000
    tmin=0
    while edge:
        if len(edge) != 1:
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            edge[3] = int(edge[3])
            count_edge += 1
            if tmin > edge[3]:
                tmin = edge[3]
            elif tmax < edge[3]:
                tmax = edge[3]
            if edge[0] in graph:
                if edge[0] == edge[1]:
                    graph[edge[0]]['neigh'].append(edge[1])
                    graph[edge[0]]['time'].append(edge[3])
                    graph[edge[0]]['degree'] += 2

                elif edge[1] not in graph[edge[0]]['neigh']:
                    graph[edge[0]]['neigh'].append(edge[1])
                    graph[edge[0]]['time'].append(edge[3])
                    graph[edge[0]]['degree'] += 1
            else:
                if edge[0] != edge[1]:
                    graph[edge[0]] = {'neigh': [edge[1]], 'degree': 1, 'component': '', 'marker': False,
                                      'color': 'white', 'dist': 0, 'Lv': 0, 'cl': 0,'time':[edge[3]]}
                    count_node += 1
                else:
                    graph[edge[0]] = {'neigh': [edge[0]], 'degree': 2, 'component': '', 'marker': False, 'color': 'white',
                                      'dist': 0, 'Lv': 0, 'cl': 0,'time':[edge[3]]}
                    count_node += 1
                    #print(edge[0])
            if edge[1] in graph:
                if edge[0] not in graph[edge[1]]['neigh'] and edge[0] != edge[1]:
                    graph[edge[1]]['neigh'].append(edge[0])
                    graph[edge[1]]['time'].append(edge[3])
                    graph[edge[1]]['degree'] += 1
            else:
                graph[edge[1]] = {'neigh': [edge[0]], 'degree': 1, 'component': '', 'marker': False, 'color': 'white',
                                  'dist': 0, 'Lv': 0, 'cl': 0, 'time':[edge[3]]}
                count_node += 1
        edge = f.readline().split()
    f.close()
    return graph,count_node,count_edge,tmin,tmax

def bfs(graph,l,d_all):
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
    return d_max

def clm(graph):
    C = 0
    for i in graph:
        n = len(graph[i]['neigh'])
        C += (n * (n - 1)) / 2

    Cl_medium = 0

    cc = 0
    for i in graph:
        cc = 0
        for k in graph[i]['neigh']:
            for l in graph[i]['neigh']:
                if k in graph[l]['neigh']:
                    cc += 1
        graph[i]['Lv'] = cc * 3

    for i in graph:
        t = int(graph[i]['Lv'] / 6)
        graph[i]['Lv'] = t
        n = len(graph[i]['neigh'])
        if n >= 2:
            graph[i]['cl'] = (2 * t) / (n * (n - 1))
        c = graph[i]['cl']
        Cl_medium += c
    return Cl_medium
def af(graph):
    r1 = 0
    r2 = 0
    r3 = 0
    re = 0
    m = 0
    for i in graph:
        m += graph[i]['degree']
    for i in graph:
        r1 += graph[i]['degree']
        r2 += graph[i]['degree'] * graph[i]['degree']
        r3 += graph[i]['degree'] * graph[i]['degree'] * graph[i]['degree']
        for j in graph[i]['neigh']:
            re += graph[i]['degree'] * graph[j]['degree']
    return  (re * r1 - r2 * r2) / (r3 * r1 - r2 * r2)


#filename='radoslaw_email_email.txt'
#filename='out.opsahl-ucsocial.txt'
#filename='out.soc-bitcoinalpha.txt'
#filename='out.sx-mathoverflow.txt'
#filename='out.munmun_digg_reply.txt'
#filename='test1.txt'
#filename='test2.txt'
#filename='testgraph_3.txt'
#filename='testgraph_4.txt'
#filename='testgraph_5.txt'
#filename='testgraph_6.txt'
#filename='testgraph_7.txt'
#filename='team_16.txt'
graph,count_node,count_edge,tmin,tmax=rgraph(filename)
print('############################################')
print('task 1.1: ')
print('Count nodes: ', count_node)
print('Count edges: ', count_edge)
print('Density: ', (2*count_edge)/(count_node*(count_node-1)))
######################################################################################

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
node500 = random.sample(comp, 500)

d = []
d_all = []
for l in node500:
    d_max=bfs(graph,l,d_all)
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

Cl_medium = clm(graph)/count_node


print('task 1.3')
print('Average cluster network  coefficient: ', Cl_medium)

print('############################################')


r=af(graph)
print('task 1.4')
print('Assortative factor: ',r)

print('############################################')


df = pandas.DataFrame({'def':[],'u':[],'v':[],
                       'cnwl': [], 'aawl': [], 'jcwl': [], 'pawl': [],
                       'cnws': [], 'aaws': [], 'jcws': [], 'paws': [],
                       'cnwe': [], 'aawe': [], 'jcwe': [], 'pawe': [],'time':[]})
                      # 'cnwe': [], 'aawe': [], 'jcwe': [], 'pawe': [],
                     #  )

def wtfl(graph,a,b,tmin,tmax):
   # print (a,' ',b)
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    return l+(1-l)*(t-tmin)/(tmax-tmin)
def wtfe(graph,a,b,tmin,tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    return l+(1-l)*(math.exp(3*(t-tmin)/(tmax-tmin))-1)/(math.e**3-1)
def wtfs(graph,a,b,tmin,tmax):
    t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
    return l+(1-l)*(math.sqrt((t-tmin)/(tmax-tmin)))


l=0.2
file = open("1.txt", "w")

for i in graph:
    jcl1=0
    jce1=0
    jcs1=0
    for l1 in graph[i]['neigh']:
        jcl1+=wtfl(graph,i,l1,tmin,tmax)
        jce1+=wtfe(graph,i,l1,tmin,tmax)
        jcs1+=wtfs(graph,i,l1,tmin,tmax)
    for j in graph:
        jcl2=0
        jce2=0
        jcs2=0

        for l2 in graph[j]['neigh']:
            jcl2 += wtfl(graph, j, l2, tmin, tmax)
            jce2 += wtfe(graph, j, l2, tmin, tmax)
            jcs2 += wtfs(graph, j, l2, tmin, tmax)
        cnl=0
        aal=0
        jcl=0
        pal=0

        cne=0
        aae=0
        jce=0
        pae=0

        cns=0
        aas=0
        jcs=0
        pas=0
        #print(i,'  ',j)

        for k in graph[i]['neigh']:
            if k in graph[j]['neigh']:
                #print(k)
                aal1=0
                aas1=0
                aae1=0
                cnl=cnl+wtfl(graph, i, k, tmin, tmax)+wtfl(graph, j, k, tmin, tmax)
                cns=cns+wtfs(graph, i, k, tmin, tmax)+wtfl(graph, j, k, tmin, tmax)
                cne=cne+wtfe(graph, i, k, tmin, tmax)+wtfl(graph, j, k, tmin, tmax)
                for l in graph[i]['neigh']:
                    if l in graph[j]['neigh'] and l in graph[k]['neigh']:
                        aal1 += wtfl(graph, k, l, tmin, tmax)
                        aas1 += wtfs(graph, k, l, tmin, tmax)
                        aae1 += wtfe(graph, k, l, tmin, tmax)

                #print(aal1)
                if (aal1==0):
                    aal1=math.e-1
                if (aas1==0):
                    aas1=math.e-1
                if (aae1==0):
                    aae1=math.e-1
                aal = (wtfl(graph, i, k, tmin, tmax) + wtfl(graph, j, k, tmin, tmax)) / math.log(1 + aal1)
                aas = (wtfs(graph, i, k, tmin, tmax) + wtfs(graph, j, k, tmin, tmax)) / math.log(1 + aas1)
                aae = (wtfe(graph, i, k, tmin, tmax) + wtfe(graph, j, k, tmin, tmax)) / math.log(1 + aae1)

                jcl=(wtfl(graph, i, k, tmin, tmax)+wtfl(graph, j, k, tmin, tmax))/(jcl1+jcl2)
                jcs=(wtfs(graph, i, k, tmin, tmax)+wtfs(graph, j, k, tmin, tmax))/(jcs1+jcs2)
                jce=(wtfe(graph, i, k, tmin, tmax)+wtfe(graph, j, k, tmin, tmax))/(jce1+jce2)

                pal=jcl1*jcl2
                pas = jcs1 * jcs2
                pae = jce1 * jce2

        if j in graph[i]['neigh']:
            newDict = pandas.DataFrame({'def': [1], 'u': [i], 'v': [j],
                            'cnwl': [cnl], 'aawl': [aal], 'jcwl': [jcl], 'pawl': [pal],
                            'cnws': [cns], 'aaws': [aas], 'jcws': [jcs], 'paws': [pas],
                            'cnwe': [cne], 'aawe': [aae], 'jcwe': [jce], 'pawe': [pae],'time':[graph[j]['time'][graph[j]['neigh'].index(i)]]})
            df = pandas.concat([df, newDict], ignore_index=True)
            if (i==1 and j==2) or (i==2 and j==1):
                print(newDict)
        else:
            newDict = pandas.DataFrame({'def': [0], 'u': [i], 'v': [j],
                                        'cnwl': [cnl], 'aawl': [aal], 'jcwl': [jcl], 'pawl': [pal],
                                        'cnws': [cns], 'aaws': [aas], 'jcws': [jcs], 'paws': [pas],
                                        'cnwe': [cne], 'aawe': [aae], 'jcwe': [jce], 'pawe': [pae],'time':[0]})
            if (i==1 and j==2) or (i==2 and j==1):
               print(newDict)
            df = pandas.concat([df, newDict], ignore_index=True)

print('start log')
df.sort_values(by='time')
X = df[['cnwl', 'aawl','jcwl','pawl','cnws','aaws','jcws','paws','cnwe','aawe','jcwe','pawe']]
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
