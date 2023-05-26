#!/usr/bin/env python3

import json
import os
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


for name in os.listdir('data'):
    # S --- Static
    # T --- Topological
    S, T, y = [], [], []

    with open(f"data/{name}") as file:
        for row in json.load(file)["features"]:
            y.append(row[0])
            S.append(row[1])
            T.append(row[2])

    clf_s = LogisticRegression(max_iter=250).fit(S, y)
    print(f"auc({name}, s): {roc_auc_score(y, clf_s.decision_function(S))}")
    clf_t = LogisticRegression(max_iter=250).fit(T, y)
    print(f"auc({name}, t): {roc_auc_score(y, clf_t.decision_function(T))}")
