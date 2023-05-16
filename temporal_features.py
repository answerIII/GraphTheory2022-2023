import math
import pandas as pd
import numpy as np

def calc_dtf(file):
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

    tmin = min(AllTime)
    tmax = max(AllTime)
    for key in AllEdges:
        l = 0.2
        timesteps = AllEdges.get(key)
        w_linear = [(l + (1-l)*(i-tmin)/(tmax-tmin)) for i in timesteps]
        w_exponential = [(l + (1 - l) * (math.exp(3*(i - tmin) / (tmax - tmin))-1)/(math.e**3-1)) for i in timesteps]
        w_square = [(l + (1 - l) * math.sqrt((i - tmin) / (tmax - tmin))) for i in timesteps]
        AllEdges[key] =[w_linear, w_exponential, w_square]
    for key in AllEdges:
        weights = AllEdges.get(key)
        new_weights = []
        for list in weights:
            new_weights.append(np.percentile(list, 0))
            new_weights.append(np.percentile(list, 25))
            new_weights.append(np.percentile(list, 50))
            new_weights.append(np.percentile(list, 75))
            new_weights.append(np.percentile(list, 100))
            new_weights.append(sum(list))
            new_weights.append(np.average(list))
            new_weights.append(np.average(np.var(list)))
        AllEdges[key] = new_weights
    Data = []
    for key in AllEdges:
        u, v = map(int, key.split('_'))
        u_neigh = AllVertex.get(u)
        v_neigh = AllVertex.get(v)
        u_edges = []
        v_edges = []
        for neigh in u_neigh:
            edge = AllEdges.get(str(u) + '_' + str(neigh))
            if not(edge):
                edge = AllEdges.get(str(neigh) + '_' + str(u))
            u_edges.append(edge)
        for neigh in v_neigh:
            edge = AllEdges.get(str(v) + '_' + str(neigh))
            if not(edge):
                edge = AllEdges.get(str(neigh) + '_' + str(v))
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
                u_z = AllEdges.get(str(u)+'_'+str(z))
                if not(u_z):
                    u_z = AllEdges.get(str(z)+'_'+str(u))
                v_z = AllEdges.get(str(v)+'_'+str(z))
                if not(v_z):
                    v_z = AllEdges.get(str(z)+'_'+str(v))
                wtf_uz = u_z[i]
                wtf_vz = v_z[i]
                z_x_sum = 0
                for x in z_neigh:
                    z_x = AllEdges.get(str(z)+'_'+str(x))
                    if not(z_x):
                        z_x = AllEdges.get(str(x)+'_'+str(z))
                    z_x_sum += z_x[i]
                AA += (wtf_uz+wtf_vz)/math.log2(1+z_x_sum)
                CN += wtf_uz+wtf_vz
            JC = CN/(u_neigh_sum_i+v_neigh_sum_i)
            PA = u_neigh_sum_i * v_neigh_sum_i
            new_vec.append(AA)
            new_vec.append(CN)
            new_vec.append(JC)
            new_vec.append(PA)
        Data.append(new_vec)
        print(new_vec, len(new_vec))
    return Data








