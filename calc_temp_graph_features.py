import csv
import networkx as nx
import math
import pandas
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Загрузить граф из CSV файла
def calc_temp_features(file):

    def load_graph_from_csv(filename):
        G = nx.Graph()
        with open(filename, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter='\t')
            for row in csvreader:
                source, target, weight, time = int(row['in']), int(row['out']), int(row['weight']), int(row['time'])
                G.add_edge(source, target, weight=weight, time=time)
        return G

    # Рассчитать Common Neighbours (CN) для пар вершин
    def calculate_common_neighbours(graph):
        cn_dict = {}
        for u, v in graph.edges():
            common_neighbours = list(nx.common_neighbors(graph, u, v))
            cn_dict[(u, v)] = len(common_neighbours)
        return cn_dict

    # Рассчитать Adamic-Adar (AA) для пар вершин
    def calculate_adamic_adar(graph):
        aa_dict = {}
        for u, v in graph.edges():
            common_neighbours = list(nx.common_neighbors(graph, u, v))
            aa_score = sum(1 / (nx.degree(graph, node) + 1e-10) for node in common_neighbours)
            aa_dict[(u, v)] = aa_score
        return aa_dict

    # Рассчитать Jaccard Coefficient (JC) для пар вершин
    def calculate_jaccard_coefficient(graph):
        jc_dict = {}
        for u, v in graph.edges():
            common_neighbours = list(nx.common_neighbors(graph, u, v))
            jc_score = len(common_neighbours) / (nx.degree(graph, u) + nx.degree(graph, v) - len(common_neighbours))
            jc_dict[(u, v)] = jc_score
        return jc_dict

    # Рассчитать Preferential Attachment (PA) для пар вершин
    def calculate_preferential_attachment(graph):
        pa_dict = {}
        for u, v in graph.edges():
            pa_score = nx.degree(graph, u) * nx.degree(graph, v)
            pa_dict[(u, v)] = pa_score
        return pa_dict

    # Загрузить граф из CSV файла
    filename = 'datasets/'+file+'.csv'
      
    graph = load_graph_from_csv(filename)

    # Вычислить признаки для всех пар вершин в графе
    common_neighbours = calculate_common_neighbours(graph)
    adamic_adar = calculate_adamic_adar(graph)
    jaccard_coefficient = calculate_jaccard_coefficient(graph)
    preferential_attachment = calculate_preferential_attachment(graph)

    # Определите имя выходного файла
    output_filename = 'done/'+file+'_DONE.csv'

    # Сохранить значения признаков для каждой пары вершин в отдельный файл
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['Node1', 'Node2', 'CommonNeighbours', 'AdamicAdar', 'JaccardCoefficient', 'PreferentialAttachment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for (u, v) in graph.edges():
            writer.writerow({'Node1': u, 'Node2': v, 'CommonNeighbours': common_neighbours.get((u, v), 0),
                            'AdamicAdar': adamic_adar.get((u, v), 0), 'JaccardCoefficient': jaccard_coefficient.get((u, v), 0),
                            'PreferentialAttachment': preferential_attachment.get((u, v), 0)})

    print(f"Признаки сохранены в файл: {output_filename}")

def calc_temp_features1(file):
    filename = 'datasets/'+file+'.csv'

    def rgraph(filename): #вычисление tmin и tmax
        
        f = open(filename)
        f.readline()
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
    
    graph,count_node,count_edge,tmin,tmax=rgraph(filename)



    df = pandas.DataFrame({'def':[],'u':[],'v':[], 'cn': [],'aa': [],'jk': [],'pa':[]})


    l=0.2
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
    plt.plot(fpr,tpr,label= file +" AUC="+str(auc))
    plt.legend(loc=4)

    print(df.loc[1])

    plt.show()


def calc_temp_features2(file):
    filename = 'datasets/'+file+'.csv'

    def rgraph(filename): #вычисление tmin и tmax
        
        f = open(filename)
        f.readline()
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
    
    graph,count_node,count_edge,tmin,tmax=rgraph(filename)


    df = pandas.DataFrame({'def':[],'u':[],'v':[],
                        'cnwl': [], 'aawl': [], 'jcwl': [], 'pawl': [],
                        'cnws': [], 'aaws': [], 'jcws': [], 'paws': [],
                        'cnwe': [], 'aawe': [], 'jcwe': [], 'pawe': [],'time':[]})


    def wtfl(graph,a,b,tmin,tmax): #wt f linear
        t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
        return l+(1-l)*(t-tmin)/(tmax-tmin)
    def wtfe(graph,a,b,tmin,tmax): #wt f exponential
        t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
        return l+(1-l)*(math.exp(3*(t-tmin)/(tmax-tmin))-1)/(math.e**3-1)
    def wtfs(graph,a,b,tmin,tmax): #wt f square root
        t = int(graph[a]['time'][graph[a]['neigh'].index(b)])
        return l+(1-l)*(math.sqrt((t-tmin)/(tmax-tmin)))


    l=0.2
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


            for k in graph[i]['neigh']:
                #print (k)
                if k in graph[j]['neigh']:


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



    print(df.loc[1])

    plt.show()    