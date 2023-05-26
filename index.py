#!/usr/bin/env python3

import json
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import roc_auc_score

SKIP_PLOT = True

for name in os.listdir("data"):
    # S --- Static
    # T --- Topological
    S, T, y = [], [], []

    with open(f"data/{name}") as file:
        for row in json.load(file)["features"]:
            y.append(row[0])
            S.append(row[1])
            T.append(row[2])

    clf_s = LogisticRegression(max_iter=450).fit(S, y)
    print(f"auc({name}, s): {roc_auc_score(y, clf_s.decision_function(S))}")

    if not SKIP_PLOT:
        RocCurveDisplay.from_predictions(y, clf_s.predict_proba(S)[:,1])
        plt.axis("square")
        plt.xlabel("false positive rate")
        plt.ylabel("true positive rate")
        plt.title("dataset {name}, s")
        plt.legend()
        plt.show()

    clf_t = LogisticRegression(max_iter=450).fit(T, y)
    print(f"auc({name}, t): {roc_auc_score(y, clf_t.decision_function(T))}")

    if not SKIP_PLOT:
        RocCurveDisplay.from_predictions(y, clf_s.predict_proba(S)[:,1])
        plt.axis("square")
        plt.xlabel("false positive rate")
        plt.ylabel("true positive rate")
        plt.title("dataset {name}, t")
        plt.legend()
        plt.show()
