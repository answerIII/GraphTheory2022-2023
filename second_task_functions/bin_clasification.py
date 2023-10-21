import pandas as pd
import numpy as np
import math
from second_task_functions.data_preporating import read_edge_for_bin
from second_task_functions.functions_for_bin_classification import weighted_topological_features_linear, weighted_topological_features_exp, weighted_topological_features_square
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt

def bin_clasification(file):

    print('----2.2----')
    filename = 'datasets/' + file + '.csv'
    graph, count_node, count_edge, tmin, tmax = read_edge_for_bin(filename)

    df = pd.DataFrame({'def': [], 'u': [], 'v': [],
                       'cnwl': [], 'aawl': [], 'jcwl': [], 'pawl': [],
                       'cnws': [], 'aaws': [], 'jcws': [], 'paws': [],
                       'cnwe': [], 'aawe': [], 'jcwe': [], 'pawe': [], 'time': []})



    for i in graph:
        jaccard_linear1 = 0
        jaccard_exp1 = 0
        jaccard_square1 = 0
        for l1 in graph[i]['neigh']:
            jaccard_linear1 += weighted_topological_features_linear(graph, i, l1, tmin, tmax)
            jaccard_exp1 += weighted_topological_features_exp(graph, i, l1, tmin, tmax)
            jaccard_square1 += weighted_topological_features_square(graph, i, l1, tmin, tmax)
        for j in graph:
            jaccard_linear2 = 0
            jaccard_exp2 = 0
            jaccard_square2 = 0

            for l2 in graph[j]['neigh']:
                jaccard_linear2 += weighted_topological_features_linear(graph, j, l2, tmin, tmax)
                jaccard_exp2 += weighted_topological_features_exp(graph, j, l2, tmin, tmax)
                jaccard_square2 += weighted_topological_features_square(graph, j, l2, tmin, tmax)

            common_neigh_linear = 0
            adamic_linear = 0
            jaccard_linear = 0
            preferential_linear = 0
            common_neigh_exp = 0
            adamic_exp = 0
            jaccard_exp = 0
            preferential_exp = 0
            common_neigh_square = 0
            adamic_square = 0
            jaccard_square = 0
            preferential_square = 0

            for k in graph[i]['neigh']:
                if k in graph[j]['neigh']:
                    adamic_linear1 = 0
                    adamic_square1 = 0
                    adamic_exp1 = 0
                    common_neigh_linear = common_neigh_linear + weighted_topological_features_linear(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)
                    common_neigh_square = common_neigh_square + weighted_topological_features_square(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)
                    common_neigh_exp = common_neigh_exp + weighted_topological_features_exp(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)
                    for l in graph[i]['neigh']:
                        if l in graph[j]['neigh'] and l in graph[k]['neigh']:
                            adamic_linear1 += weighted_topological_features_linear(graph, k, l, tmin, tmax)
                            adamic_square1 += weighted_topological_features_square(graph, k, l, tmin, tmax)
                            adamic_exp1 += weighted_topological_features_exp(graph, k, l, tmin, tmax)

                    if (adamic_linear1 == 0):
                        adamic_linear1 = math.e - 1
                    if (adamic_square1 == 0):
                        adamic_square1 = math.e - 1
                    if (adamic_exp1 == 0):
                        adamic_exp1 = math.e - 1

                    adamic_linear = (weighted_topological_features_linear(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)) / math.log(1 + adamic_linear1)
                    adamic_square = (weighted_topological_features_square(graph, i, k, tmin, tmax) + weighted_topological_features_square(graph, j, k, tmin, tmax)) / math.log(1 + adamic_square1)
                    adamic_exp = (weighted_topological_features_exp(graph, i, k, tmin, tmax) + weighted_topological_features_exp(graph, j, k, tmin, tmax)) / math.log(1 + adamic_exp1)

                    jaccard_linear = (weighted_topological_features_linear(graph, i, k, tmin, tmax) + weighted_topological_features_linear(graph, j, k, tmin, tmax)) / (jaccard_linear1 + jaccard_linear2)
                    jaccard_square = (weighted_topological_features_square(graph, i, k, tmin, tmax) + weighted_topological_features_square(graph, j, k, tmin, tmax)) / (jaccard_square1 + jaccard_square2)
                    jaccard_exp = (weighted_topological_features_exp(graph, i, k, tmin, tmax) + weighted_topological_features_exp(graph, j, k, tmin, tmax)) / (jaccard_exp1 + jaccard_exp2)

                    preferential_linear = jaccard_linear1 * jaccard_linear2
                    preferential_square = jaccard_square1 * jaccard_square2
                    preferential_exp = jaccard_exp1 * jaccard_exp2

            if j in graph[i]['neigh']:
                new_row = pd.DataFrame({'def': [1], 'u': [i], 'v': [j],
                                'cnwl': [common_neigh_linear], 'aawl': [adamic_linear], 'jcwl': [jaccard_linear], 'pawl': [preferential_linear],
                                'cnws': [common_neigh_square], 'aaws': [adamic_square], 'jcws': [jaccard_square], 'paws': [preferential_square],
                                'cnwe': [common_neigh_exp], 'aawe': [adamic_exp], 'jcwe': [jaccard_exp], 'pawe': [preferential_exp], 'time': [graph[j]['time'][graph[j]['neigh'].index(i)]]})
                df = pd.concat([df, new_row], ignore_index=True)
                if (i == 1 and j == 2) or (i == 2 and j == 1):
                    print(new_row)
            else:
                new_row = pd.DataFrame({'def': [0], 'u': [i], 'v': [j],
                                        'cnwl': [common_neigh_linear], 'aawl': [adamic_linear], 'jcwl': [jaccard_linear], 'pawl': [preferential_linear],
                                        'cnws': [common_neigh_square], 'aaws': [adamic_square], 'jcws': [jaccard_square], 'paws': [preferential_square],
                                        'cnwe': [common_neigh_exp], 'aawe': [adamic_exp], 'jcwe': [jaccard_exp], 'pawe': [preferential_exp], 'time': [0]})
                if (i == 1 and j == 2) or (i == 2 and j == 1):
                    print(new_row)
                df = pd.concat([df, new_row], ignore_index=True)

    print('start log')
    df = df.sort_values(by='time')
    X = df[['cnwl', 'aawl', 'jcwl', 'pawl', 'cnws', 'aaws', 'jcws', 'paws', 'cnwe', 'aawe', 'jcwe', 'pawe']]
    y = df['def']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    log_regression = LogisticRegression()
    log_regression.fit(X_train, y_train)
    y_pred = log_regression.predict(X_test)
    y_pred_proba = log_regression.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = metrics.roc_curve(y_test, y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    plt.plot(fpr, tpr, label="AUC=" + str(auc))
    plt.legend(loc=4)

    print(df.iloc[1])
    plt.show()

