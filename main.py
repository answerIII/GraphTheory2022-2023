import pandas as pd
import math
import random
import numpy as np
from collections import deque
import collections
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import RocCurveDisplay

from all_info_dataset import get_info_dataset
from graph_properties import get_graph_properties
from static_topological_features import get_static_topological_features
from temporal_topological_features import get_temporal_topological_features
from all_info_dataset import get_adjacency_list_test
from static_topological_features import common_neighbours, adamic_adar, jaccard_coefficient, preferential_attachment

# dataset_path = 'datasets/' + 'test' + '.txt'
# dataset_path = 'datasets/' + 'RA_radoslaw_email_email' + '.txt'
# dataset_path = 'datasets/' + 'UC_opsahl-ucsocial' + '.txt'
# dataset_path = 'datasets/' + 'BA_soc-sign-bitcoinalpha' + '.txt'
# dataset_path = 'datasets/' + 'BO_soc-sign-bitcoinotc' + '.txt'

# dataset_path = 'datasets/' + 'ma_sx-mathoverflow' + '.txt'
# dataset_path = 'datasets/' + 'as_sx-askubuntu' + '.txt'

# dataset_path = 'datasets/' + 'DG_munmun_digg_reply' + '.txt'
# dataset_path = 'datasets/' + 'DF_digg-friends' + '.txt'
# dataset_path = 'datasets/' + 'su_sx-superuser' + '.txt'
# dataset_path = 'datasets/' + 'PL_prosper-loans' + '.txt'

# dataset_path = 'datasets/' + 'testgraph_1' + '.txt'
# dataset_path = 'datasets/' + 'testgraph_2' + '.txt'
# dataset_path = 'datasets/' + 'testgraph_3' + '.txt'
dataset_path = 'datasets/' + 'team_12' + '.txt'


print('Введите 1, если датасет из тестовых (без весов ребер и времени)')
print('Введите 2, если иначе')
is_test = input()
if is_test == '1':
    data = pd.read_csv(dataset_path, sep='\s+', names=['id_from', 'id_to'], header=None)
    adjacency_list, count_edges, is_loop = get_adjacency_list_test(data)
    get_graph_properties(adjacency_list, count_edges, is_loop)

    CN = common_neighbours(1, 2, adjacency_list)
    AA = adamic_adar(1, 2, adjacency_list)
    JC = jaccard_coefficient(1, 2, adjacency_list)
    PA = preferential_attachment(1, 2, adjacency_list)

    print('CN = ' + str(CN))
    print('AA = ' + str(AA))
    print('JC = ' + str(JC))
    print('PA = ' + str(PA))

elif is_test == '2':
    data = pd.read_csv(dataset_path, sep='\s+', names=['id_from', 'id_to', 'weight', 'time'], header=None)
    q = 0.5
    adjacency_list, adjacency_list_until_s, adjacency_list_until_s_multi, edges_r, edges_r_until_s, \
    edges_r_until_s_multi, edges_p, edges_n, edges_p_multi, edges_n_multi, tmin, tmax, count_edges, is_loop = get_info_dataset(data, q)

    for edge in edges_r:
        if len(edges_r[edge]) > 1:
            print('Типа графа: Мультиграф')
            break

    print('Введите 1 для характеристик статического графа')
    print('Введите 2 для static topological features')
    print('Введите 3 для temporal topological features')
    part = input()
    if part == '1': #Характеристики статического графа
        get_graph_properties(adjacency_list, count_edges, is_loop)
    elif part == '2': #Static topological features 4.1.1
        edges_p_copy_1 = edges_p.copy()
        edges_n_copy_1 = edges_n.copy()
        X_1, Y_1 = get_static_topological_features(adjacency_list_until_s, edges_p_copy_1, edges_n_copy_1)

        # Делим 25% тестовых
        model = LogisticRegression()
        X_train, X_test, Y_train, Y_test = train_test_split(X_1, Y_1, test_size=0.25, random_state=0)
        # Обучение
        model.fit(X_train, Y_train)
        accuracy = accuracy_score(Y_test, model.predict(X_test))
        auc_roc = roc_auc_score(Y_test, model.predict_proba(X_test)[:, 1])
        print(classification_report(Y_test, model.predict(X_test)))
        svc_disp = RocCurveDisplay.from_estimator(model, X_test, Y_test)
        plt.show()
    elif part == '3': #Temporal topological features
        edges_p_copy_2 = edges_p_multi.copy()
        edges_n_copy_2 = edges_n_multi.copy()
        X_2, Y_2 = get_temporal_topological_features(adjacency_list_until_s_multi, tmin, tmax, edges_r_until_s_multi,
                                                     edges_p_copy_2, edges_n_copy_2)

        # Делим 25% тестовых
        model = LogisticRegression()
        X_train, X_test, Y_train, Y_test = train_test_split(X_2, Y_2, test_size=0.25, random_state=0)
        # Обучение
        model.fit(X_train, Y_train)
        accuracy = accuracy_score(Y_test, model.predict(X_test))
        auc_roc = roc_auc_score(Y_test, model.predict_proba(X_test)[:, 1])
        print(classification_report(Y_test, model.predict(X_test)))
        svc_disp = RocCurveDisplay.from_estimator(model, X_test, Y_test)
        plt.show()

