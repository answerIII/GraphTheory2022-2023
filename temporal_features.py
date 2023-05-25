import math
import pandas as pd
import numpy as np
import random

#Получение векторов в графе типа Events
def calc_dtf_events(file, q):
    def intersection_list(list1, list2):
        return set(list1).intersection(list2)
    def union_list(list1,list2):
        return set(list1+list2)
    #Считывание графа
    file_path = 'datasets/' + file + '.csv'
    data = pd.read_csv(file_path, sep="\t")
    dvudol = 0
    if file[-9] == '1':
        dvudol = 1
    AllEdges = {}
    AllTime = []
    AllVertex = {}
    #Сохранение ребер и списков их временных меток
    for index, row in data.iterrows():
        if row['in'] == row['out']:
            continue
        first_variant = AllEdges.get((str(row['in'])+'_'+str(row['out'])))
        second_variant = AllEdges.get((str(row['out'])+'_'+str(row['in'])))
        if first_variant:
            first_variant.append(int(row['time']))
            AllEdges[(str(row['in'])+'_'+str(row['out']))] = first_variant
        elif second_variant:
            second_variant.append(int(row['time']))
            AllEdges[(str(row['out']) + '_' + str(row['in']))] = second_variant
        else:
            AllEdges[(str(row['in'])+'_'+str(row['out']))] = [int(row['time'])]
        AllTime.append(int(row['time']))

    tmin = min(AllTime)
    tmax = max(AllTime)
    bound = np.percentile(AllTime, q)
    ExistingEdges = {}
    FutureEdges = {}
    #Создание списков смежности для графа до момента q
    for index,row in data.iterrows():
        if row['in'] == row['out'] or row['time'] >= bound:
            continue
        left = AllVertex.get(row['in'])
        if left:
            if (row['out']) in left:
                continue
            else:
                left.append(row['out'])
                AllVertex[row['in']] = left
        else:
            AllVertex[row['in']] = [row['out']]

        right = AllVertex.get(row['out'])
        if right:
            if row['in'] in right:
                continue
            else:
                right.append(row['in'])
                AllVertex[row['out']] = right
        else:
            AllVertex[row['out']] = [row['in']]
    #Разделение ребер на уже появившееся и те, что появятся в будущем
    for key in AllEdges:
        timesteps = AllEdges.get(key)
        exis = [edge for edge in timesteps if edge < bound]
        if len(exis)>0:
            ExistingEdges[key] = exis
        fut = [edge for edge in timesteps if edge >= bound]
        if len(fut)>0 and len(exis)==0:
            FutureEdges[key] = True
    #Перевод времени в веса
    for key in ExistingEdges:
        l = 0.2
        timesteps = ExistingEdges.get(key)
        w_linear = [(l + (1-l)*(i-tmin)/(tmax-tmin)) for i in timesteps]
        w_exponential = [(l + (1 - l) * (math.exp(3*(i - tmin) / (tmax - tmin))-1)/(math.e**3-1)) for i in timesteps]
        w_square = [(l + (1 - l) * math.sqrt((i - tmin) / (tmax - tmin))) for i in timesteps]
        ExistingEdges[key] = [w_linear, w_exponential, w_square]
    #Агрегация предыдущих событий
    for key in ExistingEdges:
        weights = ExistingEdges.get(key)
        new_weights = []
        for lists in weights:
            new_weights.append(np.percentile(lists, 0))
            new_weights.append(np.percentile(lists, 25))
            new_weights.append(np.percentile(lists, 50))
            new_weights.append(np.percentile(lists, 75))
            new_weights.append(np.percentile(lists, 100))
            new_weights.append(sum(lists))
            new_weights.append(np.average(lists))
            new_weights.append(np.average(np.var(lists)))
        ExistingEdges[key] = new_weights
    X = []
    Y = []
    keys = list(FutureEdges.keys())
    while len(Y) <= 20000:
        # Высчитывание вектора для ребра, которое появится
        key = random.choice(keys)
        u, v = map(int, key.split('_'))
        u_neigh = AllVertex.get(u)
        v_neigh = AllVertex.get(v)
        u_edges = []
        v_edges = []
        if not(u_neigh) or not(v_neigh):
            continue
        for neigh in u_neigh:
            edge = ExistingEdges.get(str(u) + '_' + str(neigh))
            if not(edge):
                edge = ExistingEdges.get(str(neigh) + '_' + str(u))
            u_edges.append(edge)
        for neigh in v_neigh:
            edge = ExistingEdges.get(str(v) + '_' + str(neigh))
            if not(edge):
                edge = ExistingEdges.get(str(neigh) + '_' + str(v))
            v_edges.append(edge)
        intersection_neigh = intersection_list(u_neigh, v_neigh)
        new_vec = []
        for i in range(24):
            AA = 0
            CN = 0
            JC = 0
            u_neigh_sum_i = sum([edges[i] for edges in u_edges])
            v_neigh_sum_i = sum([edges[i] for edges in v_edges])
            for z in intersection_neigh:
                z_neigh = AllVertex.get(z)
                u_z = ExistingEdges.get(str(u)+'_'+str(z))
                if not(u_z):
                    u_z = ExistingEdges.get(str(z)+'_'+str(u))
                v_z = ExistingEdges.get(str(v)+'_'+str(z))
                if not(v_z):
                    v_z = ExistingEdges.get(str(z)+'_'+str(v))
                wtf_uz = u_z[i]
                wtf_vz = v_z[i]
                z_x_sum = 0
                for x in z_neigh:
                    z_x = ExistingEdges.get(str(z)+'_'+str(x))
                    if not(z_x):
                        z_x = ExistingEdges.get(str(x)+'_'+str(z))
                    z_x_sum += z_x[i]
                zn = math.log2(1+z_x_sum)
                if zn < 1e-12:
                    zn = 1e-12
                AA += (wtf_uz+wtf_vz)/zn
                CN += wtf_uz+wtf_vz
            sum_neigh_i = (u_neigh_sum_i + v_neigh_sum_i)
            if sum_neigh_i < 1e-12:
                sum_neigh_i = 1e-12
            JC = CN / sum_neigh_i
            PA = u_neigh_sum_i * v_neigh_sum_i
            new_vec.append(AA)
            new_vec.append(CN)
            new_vec.append(JC)
            new_vec.append(PA)
        X.append(new_vec)
        Y.append(1)
        #Получение вектора для ребра, которое не появится
        was_found = False
        repeat = 0
        while was_found == False and repeat < 100:
            rand_u = random.choice(list(AllVertex.keys()))
            nbs_u = AllVertex.get(rand_u)
            nb_u = random.choice(nbs_u)
            rand_v = random.choice(AllVertex.get(nb_u))
            if int(rand_u) * int(rand_v) * dvudol <= 0 and not(FutureEdges.get(str(rand_u) +'_' + str(rand_v))) \
            and not(FutureEdges.get(str(rand_v) + '_' + str(rand_u))) \
            and rand_v not in nbs_u:
                u = rand_u
                v = rand_v
                u_neigh = AllVertex.get(u)
                v_neigh = AllVertex.get(v)
                u_edges = []
                v_edges = []
                if not (u_neigh) or not (v_neigh):
                    repeat += 1
                    continue
                was_found = True
                for neigh in u_neigh:
                    edge = ExistingEdges.get(str(u) + '_' + str(neigh))
                    if not (edge):
                        edge = ExistingEdges.get(str(neigh) + '_' + str(u))
                    u_edges.append(edge)
                for neigh in v_neigh:
                    edge = ExistingEdges.get(str(v) + '_' + str(neigh))
                    if not (edge):
                        edge = ExistingEdges.get(str(neigh) + '_' + str(v))
                    v_edges.append(edge)
                intersection_neigh = intersection_list(u_neigh, v_neigh)
                new_vec = []
                for i in range(24):
                    AA = 0
                    CN = 0
                    JC = 0
                    u_neigh_sum_i = sum([edges[i] for edges in u_edges])
                    v_neigh_sum_i = sum([edges[i] for edges in v_edges])
                    for z in intersection_neigh:
                        z_neigh = AllVertex.get(z)
                        u_z = ExistingEdges.get(str(u) + '_' + str(z))
                        if not (u_z):
                            u_z = ExistingEdges.get(str(z) + '_' + str(u))
                        v_z = ExistingEdges.get(str(v) + '_' + str(z))
                        if not (v_z):
                            v_z = ExistingEdges.get(str(z) + '_' + str(v))
                        wtf_uz = u_z[i]
                        wtf_vz = v_z[i]
                        z_x_sum = 0
                        for x in z_neigh:
                            z_x = ExistingEdges.get(str(z) + '_' + str(x))
                            if not (z_x):
                                z_x = ExistingEdges.get(str(x) + '_' + str(z))
                            z_x_sum += z_x[i]
                        zn = math.log2(1 + z_x_sum)
                        if zn < 1e-12:
                            zn = 1e-12
                        AA += (wtf_uz + wtf_vz) / zn
                        CN += wtf_uz + wtf_vz
                    sum_neigh_i = (u_neigh_sum_i + v_neigh_sum_i)
                    if sum_neigh_i < 1e-12:
                        sum_neigh_i = 1e-12
                    JC = CN / sum_neigh_i
                    PA = u_neigh_sum_i * v_neigh_sum_i
                    new_vec.append(AA)
                    new_vec.append(CN)
                    new_vec.append(JC)
                    new_vec.append(PA)
                X.append(new_vec)
                Y.append(0)
    #Возвращаем вектора признаков и ответы для них
    return (X,Y)

#Получение векторов в обыном графе
def calc_dtf(file,q):
    def intersection_list(list1, list2):
        return set(list1).intersection(list2)
    def union_list(list1,list2):
        return set(list1+list2)
    #Считывание графа
    file_path = 'datasets/' + file + '.csv'
    data = pd.read_csv(file_path, sep="\t")
    dvudol = 0
    if file[-9] == '1':
        dvudol = 1
    AllEdges = {}
    AllTime = []
    AllVertex = {}
    #Сохранение ребер и временных меток
    for index, row in data.iterrows():
        if row['in'] == row['out']:
            continue
        AllEdges[(str(row['in'])+'_'+str(row['out']))] = int(row['time'])
        AllTime.append(int(row['time']))

    tmin = min(AllTime)
    tmax = max(AllTime)
    bound = np.percentile(AllTime, q)
    ExistingEdges = {}
    FutureEdges = {}
    #Создание списков смежности для графа до момента q
    for index,row in data.iterrows():
        if row['in'] == row['out'] or row['time'] >= bound:
            continue
        left = AllVertex.get(row['in'])
        if left:
            if (row['out']) in left:
                continue
            else:
                left.append(row['out'])
                AllVertex[row['in']] = left
        else:
            AllVertex[row['in']] = [row['out']]

        right = AllVertex.get(row['out'])
        if right:
            if row['in'] in right:
                continue
            else:
                right.append(row['in'])
                AllVertex[row['out']] = right
        else:
            AllVertex[row['out']] = [row['in']]
    #Разделение ребер на уже появившееся и те, что появятся в будущем
    for key in AllEdges:
        time = AllEdges.get(key)
        if time<bound:
            ExistingEdges[key] = time
        else:
            FutureEdges[key] = True
    #Перевод времени в веса
    for key in ExistingEdges:
        l = 0.2
        time = ExistingEdges.get(key)
        w_linear = (l + (1-l)*(time-tmin)/(tmax-tmin))
        w_exponential = (l + (1 - l) * (math.exp(3*(time - tmin) / (tmax - tmin))-1)/(math.e**3-1))
        w_square = (l + (1 - l) * math.sqrt((time - tmin) / (tmax - tmin)))
        ExistingEdges[key] = [w_linear, w_exponential, w_square]
    X = []
    Y = []
    keys = list(FutureEdges.keys())
    while len(Y) <= 20000:
        # Высчитывание вектора для ребра, которое появится
        key = random.choice(keys)
        u, v = map(int, key.split('_'))
        u_neigh = AllVertex.get(u)
        v_neigh = AllVertex.get(v)
        u_edges = []
        v_edges = []
        if not (u_neigh) or not (v_neigh):
            continue
        for neigh in u_neigh:
            edge = ExistingEdges.get(str(u) + '_' + str(neigh))
            if not (edge):
                edge = ExistingEdges.get(str(neigh) + '_' + str(u))
            u_edges.append(edge)
        for neigh in v_neigh:
            edge = ExistingEdges.get(str(v) + '_' + str(neigh))
            if not (edge):
                edge = ExistingEdges.get(str(neigh) + '_' + str(v))
            v_edges.append(edge)
        intersection_neigh = intersection_list(u_neigh, v_neigh)
        new_vec = []
        for i in range(3):
            AA = 0
            CN = 0
            JC = 0
            u_neigh_sum_i = sum([edges[i] for edges in u_edges])
            v_neigh_sum_i = sum([edges[i] for edges in v_edges])
            for z in intersection_neigh:
                z_neigh = AllVertex.get(z)
                u_z = ExistingEdges.get(str(u) + '_' + str(z))
                if not (u_z):
                    u_z = ExistingEdges.get(str(z) + '_' + str(u))
                v_z = ExistingEdges.get(str(v) + '_' + str(z))
                if not (v_z):
                    v_z = ExistingEdges.get(str(z) + '_' + str(v))
                wtf_uz = u_z[i]
                wtf_vz = v_z[i]
                z_x_sum = 0
                for x in z_neigh:
                    z_x = ExistingEdges.get(str(z) + '_' + str(x))
                    if not (z_x):
                        z_x = ExistingEdges.get(str(x) + '_' + str(z))
                    z_x_sum += z_x[i]
                zn = math.log2(1 + z_x_sum)
                if zn < 1e-12:
                    zn = 1e-12
                AA += (wtf_uz + wtf_vz) / zn
                CN += wtf_uz + wtf_vz
            sum_neigh_i = (u_neigh_sum_i + v_neigh_sum_i)
            if sum_neigh_i < 1e-12:
                sum_neigh_i = 1e-12
            JC = CN / sum_neigh_i
            PA = u_neigh_sum_i * v_neigh_sum_i
            new_vec.append(AA)
            new_vec.append(CN)
            new_vec.append(JC)
            new_vec.append(PA)
        X.append(new_vec)
        Y.append(1)
        # Получение вектора для ребра, которое не появится
        was_found = False
        repeat = 0
        while was_found == False and repeat < 100:
            rand_u = random.choice(list(AllVertex.keys()))
            nbs_u = AllVertex.get(rand_u)
            nb_u = random.choice(nbs_u)
            rand_v = random.choice(AllVertex.get(nb_u))
            if int(rand_u) * int(rand_v) * dvudol <= 0 and not (FutureEdges.get(str(rand_u) + '_' + str(rand_v))) \
                    and not (FutureEdges.get(str(rand_v) + '_' + str(rand_u))) \
                    and rand_v not in nbs_u:
                u = rand_u
                v = rand_v
                u_neigh = AllVertex.get(u)
                v_neigh = AllVertex.get(v)
                u_edges = []
                v_edges = []
                if not (u_neigh) or not (v_neigh):
                    repeat += 1
                    continue
                was_found = True
                for neigh in u_neigh:
                    edge = ExistingEdges.get(str(u) + '_' + str(neigh))
                    if not (edge):
                        edge = ExistingEdges.get(str(neigh) + '_' + str(u))
                    u_edges.append(edge)
                for neigh in v_neigh:
                    edge = ExistingEdges.get(str(v) + '_' + str(neigh))
                    if not (edge):
                        edge = ExistingEdges.get(str(neigh) + '_' + str(v))
                    v_edges.append(edge)
                intersection_neigh = intersection_list(u_neigh, v_neigh)
                new_vec = []
                for i in range(3):
                    AA = 0
                    CN = 0
                    JC = 0
                    u_neigh_sum_i = sum([edges[i] for edges in u_edges])
                    v_neigh_sum_i = sum([edges[i] for edges in v_edges])
                    for z in intersection_neigh:
                        z_neigh = AllVertex.get(z)
                        u_z = ExistingEdges.get(str(u) + '_' + str(z))
                        if not (u_z):
                            u_z = ExistingEdges.get(str(z) + '_' + str(u))
                        v_z = ExistingEdges.get(str(v) + '_' + str(z))
                        if not (v_z):
                            v_z = ExistingEdges.get(str(z) + '_' + str(v))
                        wtf_uz = u_z[i]
                        wtf_vz = v_z[i]
                        z_x_sum = 0
                        for x in z_neigh:
                            z_x = ExistingEdges.get(str(z) + '_' + str(x))
                            if not (z_x):
                                z_x = ExistingEdges.get(str(x) + '_' + str(z))
                            z_x_sum += z_x[i]
                        zn = math.log2(1 + z_x_sum)
                        if zn < 1e-12:
                            zn = 1e-12
                        AA += (wtf_uz + wtf_vz) / zn
                        CN += wtf_uz + wtf_vz
                    sum_neigh_i = (u_neigh_sum_i + v_neigh_sum_i)
                    if sum_neigh_i < 1e-12:
                        sum_neigh_i = 1e-12
                    JC = CN / sum_neigh_i
                    PA = u_neigh_sum_i * v_neigh_sum_i
                    new_vec.append(AA)
                    new_vec.append(CN)
                    new_vec.append(JC)
                    new_vec.append(PA)
                X.append(new_vec)
                Y.append(0)
    # Возвращаем вектора признаков и ответы для них
    return (X, Y)







