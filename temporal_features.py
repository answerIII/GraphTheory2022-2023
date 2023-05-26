import math
from collections import defaultdict
from typing import List, Callable
from operator import add, truediv, mul
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, RocCurveDisplay
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json
from numpy import quantile


def read_graph(path = "out.sx-mathoverflow"):
    tmin = math.inf
    tmax = 0
    time_list = []
    with open(path, 'r') as fin:
        for line in fin:
            line = line.strip().split()
            _,_,_,t = map(int, line)
            time_list.append(t)
            tmin = min(tmin, t)
            tmax = max(tmax, t)

    q_time = quantile(time_list, 0.66)

    with open(path, 'r') as fin:
        for line in fin:
            line = line.strip().split()
            a,b,_,t = map(int, line)
            if t <= q_time:
                adj_dict_qtime[a].append((b,t))
                adj_dict_qtime[b].append((a,t))
                adj_dict_qtime_nbs[a].add(b)
                adj_dict_qtime_nbs[b].add(a)
            else:
                adj_dict_qto1[a].add(b)
                adj_dict_qto1[b].add(a)

    return tmin, tmax

# adj_dict_qtime = defaultdict(list)
# adj_dict_qto1 = defaultdict(set)
# adj_dict_qtime_nbs = defaultdict(set)
l = 0.2
# tmin, tmax = read_graph(adj_dict_qtime, adj_dict_qto1)


def balanced_selecetion_pos(selection_volume, positive : set) -> None:
    for node in adj_dict_qto1.keys():
        for neighbour in adj_dict_qto1[node]:
            if len(common_neighbours(node, neighbour)) != 0 and node != neighbour and (neighbour, node) not in positive and node not in adj_dict_qtime_nbs[neighbour]:
                positive.add((node,neighbour))
                if len(positive) == selection_volume:
                    return
                
def balanced_selecetion_neg(selection_volume, negative : set) -> None:
    for node in adj_dict_qtime.keys():
        for neighbour in adj_dict_qtime_nbs[node]:
            if neighbour == node:
                continue
            for nb_dist_2 in adj_dict_qtime_nbs[neighbour]:
                if node != nb_dist_2 and (nb_dist_2, node) not in negative and node not in adj_dict_qto1[nb_dist_2] and node not in adj_dict_qtime_nbs[nb_dist_2]:
                    negative.add((node,nb_dist_2))
                if len(negative) == selection_volume:
                    return
                
def check_simple_graph(adj_dict_qtime : dict, adj_dict_qtime_nbs : dict) -> bool:
    for key in adj_dict_qtime.keys():
        if len(adj_dict_qtime[key]) != len(adj_dict_qtime_nbs):
            return False
    return True


#checked
def w_linear(t):
    ans = l + (1-l) * (t - tmin) / (tmax - tmin)
    return ans

#checked
def w_exponential(t):
    ans = l + (1-l) * (math.exp( (3*(t-tmin)) / (tmax-tmin) ) - 1) / (math.exp(3) - 1)
    return ans

#checked
def w_square_root(t):
    ans = l + (1-l) * math.sqrt((t-tmin)/(tmax-tmin))
    return ans

#checked
def past_event_aggregation(weights : list) -> list:
    accumulated_weights = []
    weights.sort()
    n = len(weights)
    w_sum = sum(weights)
    mean = w_sum / n
    variance = sum([(i-mean)**2 for i in weights]) / n
    weights.append(weights[-1])
    for alpha in [0, 0.25, 0.5, 0.75, 1]:
        k = int((n-1) * alpha)
        if k+1 < alpha * n:
            accumulated_weights.append(weights[k+1])
        elif k+1 == alpha * n:
            accumulated_weights.append((weights[k+1]+weights[k])/2)
        else:
            accumulated_weights.append(weights[k])

    weights.pop()
    accumulated_weights.extend([w_sum, mean, variance])
    return accumulated_weights

#checked
def weighted_neighbours_sum(node : int, w_function : Callable) -> list:
    weighted_neighbors_link = defaultdict(list)
    aggregated_weights  = [0] * 8
    for neigbour, time in adj_dict_qtime[node]:
        weighted_neighbors_link[neigbour].append(w_function(time))

    for value in weighted_neighbors_link.values():
        aggregated_weights = list(map(add, aggregated_weights, past_event_aggregation(value)))

    return aggregated_weights

#checked
def wtf(u,v, w_function: Callable) -> list:
    weighted_link = []
    for neigbour, time in adj_dict_qtime[u]:
        if neigbour == v:
            weighted_link.append(w_function(time))

    return past_event_aggregation(weighted_link)

#checked but use wisely
def common_neighbours(u,v) -> set:
    u_neighbours = set([i[0] for i in adj_dict_qtime[u]])
    v_neighbours = set([i[0] for i in adj_dict_qtime[v]])
    return u_neighbours.intersection(v_neighbours)

#checked
def aa_temp(u,v,func):
    ans = [0] * 8
    for i in common_neighbours(u,v):
        numerator = list(map(add, wtf(u,i,func), wtf(v,i,func)))
        denominator = [math.log(1+i) for i in weighted_neighbours_sum(i, func)]
        if denominator[-1] == 0:
            temp = list(map(truediv, numerator[:-1], denominator[:-1]))
            temp.append(0)
        else:
            temp = list(map(truediv, numerator, denominator))
        ans = list(map(add, temp, ans))
    return ans

#checked
def cn_temp(u, v, func):
    ans = [0] * 8
    for i in common_neighbours(u,v):
        temp = list(map(add, wtf(u,i,func), wtf(v,i,func)))
        ans = list(map(add, temp, ans))
    return ans

#checked
def jc_temp(u, v, func):
    ans = [0] * 8
    for i in common_neighbours(u,v):
        numerator = list(map(add, wtf(u,i,func), wtf(v,i,func)))
        ans = list(map(add, numerator, ans))

    denominator = list(map(add, weighted_neighbours_sum(u, func), weighted_neighbours_sum(v, func)))
    if denominator[-1] == 0:
        ans = list(map(truediv, ans[:-1], denominator[:-1]))
        ans.append(0)
    else:
        ans = list(map(truediv, ans, denominator))
    return ans

#checked
def pa_temp(u,v,func):
    ans = list(map(mul, weighted_neighbours_sum(u, func), weighted_neighbours_sum(v, func)))
    return ans


def temporal_feature_vector(u,v):
    ans = []
    weight_functions = [w_linear, w_exponential, w_square_root]
    feature_functions = [aa_temp, cn_temp, jc_temp, pa_temp]
    for w_function in weight_functions:
        for f_function in feature_functions:
            ans.extend(f_function(u,v,w_function))

    return ans


def wtf_simple(u,v, w_function: Callable) -> float:
    for neigbour, time in adj_dict_qtime[u]:
        if neigbour == v:
            return w_function(time)
        
def weighted_neighbours_sum_simple(node : int, w_function : Callable) -> float:
    weighted_sum = 0
    for neigbour, time in adj_dict_qtime[node]:
        weighted_sum += w_function(time)
    return weighted_sum


def aa_temp_simple(u,v,func):
    ans = 0
    for i in common_neighbours(u,v):
        numerator = wtf_simple(u,i,func) + wtf_simple(v,i,func)
        denominator = math.log1p(weighted_neighbours_sum_simple(i, func))
        ans += numerator / denominator
    return ans


def cn_temp_simple(u, v, func):
    ans = 0
    for i in common_neighbours(u,v):
        ans += wtf_simple(u,i,func) + wtf_simple(v,i,func)
    return ans


def jc_temp_simple(u, v, func):
    ans = 0
    for i in common_neighbours(u,v):
        ans += wtf_simple(u,i,func), wtf_simple(v,i,func)
    denominator = weighted_neighbours_sum_simple(u, func) + weighted_neighbours_sum_simple(v, func)
    ans = ans / denominator
    return ans


def pa_temp_simple(u,v,func):
    ans = weighted_neighbours_sum(u, func) * weighted_neighbours_sum(v, func)
    return ans


def temporal_feature_vector_simple(u,v):
    ans = []
    weight_functions = [w_linear, w_exponential, w_square_root]
    feature_functions = [aa_temp_simple, cn_temp_simple, jc_temp_simple, pa_temp_simple]
    for w_function in weight_functions:
        for f_function in feature_functions:
            ans.append(f_function(u,v,w_function))

    return ans


def apply_regression(positive_pairs : list, negative_pairs : list, data_amount, path : str = '', simple=False):
    X = []
    if simple:
        for pair in positive_pairs:
            X.append(temporal_feature_vector_simple(pair[0], pair[1]))
        if path:
            write_json(f"{path}_pos_features.json", X)
        temp = []
        for pair in negative_pairs:
            temp.append(temporal_feature_vector_simple(pair[0], pair[1]))
        if path:
            write_json(f"{path}_neg_features.json", temp)
        X.extend(temp)
        del temp
    else:
        for pair in positive_pairs:
            X.append(temporal_feature_vector(pair[0], pair[1]))
        if path:
            write_json(f"{path}_pos_features.json", X)
        temp = []
        for pair in negative_pairs:
            temp.append(temporal_feature_vector(pair[0], pair[1]))
        if path:
            write_json(f"{path}_neg_features.json", temp)
        X.extend(temp)
        del temp

    if not path:
        y = [1 for _ in range(data_amount)]
        y.extend([0 for _ in range(data_amount)])

        X_train, X_test, y_train, y_test = train_test_split(X,y, train_size = 0.75, test_size=0.25)

        lin_reg = LogisticRegression()
        y_score = lin_reg.fit(X_train, y_train).predict_proba(X_test)
        print(roc_auc_score(y_test,y_score[:,1]))
        RocCurveDisplay.from_predictions(y_test, y_score[:,1])
        plt.show()


def read_selection_json(path):
    with open(path, 'r') as fin:
        data = json.load(fin)
    return data


def read_selection_txt(path):
    data = []
    with open(path, 'r') as fin:
        for line in fin:
            data.append([float(i) for i in line.strip().split()])
    return data


def write_fetures_txt(path, X):
        with open(path, 'w') as fout:
            for i in X:
                temp = [float(k) for k in i]
                temp.append('\n')
                fout.write(' '.join(map(str, temp)))

def write_json(path, X):
    with open(path, 'w') as fout:
        json.dump(list(X), fout)


def main(path = None):
    global adj_dict_qtime, adj_dict_qto1, adj_dict_qtime_nbs
    adj_dict_qtime = defaultdict(list)
    adj_dict_qto1 = defaultdict(set)
    adj_dict_qtime_nbs = defaultdict(set)
    global tmin, tmax
    tmin, tmax = read_graph()
    pos = set()
    neg = set()
    data_amount = 100
    simple = check_simple_graph(adj_dict_qtime, adj_dict_qtime_nbs)
    balanced_selecetion_pos(data_amount,pos)
    data_amount = len(pos)
    balanced_selecetion_neg(data_amount, neg)
    if path:
        write_json(f"{path}_pos_pairs.json", pos)
        write_json(f"{path}_neg_pairs.json", neg)
    apply_regression(pos, neg, data_amount, path, simple)

def features_to_file():
    source_files = ["out_digg_reply.munmun_digg_reply", "out.opsahl-ucsocial", "out.sx-askubuntu", "out.sx-mathoverflow", "out.sx-superuser", "out.true_digg_friends"] #"out.soc-sign-bitcoinotc" - floats
    for fname in source_files:
        main(fname)

if __name__ == "__main__":
    main()

# features_to_file()