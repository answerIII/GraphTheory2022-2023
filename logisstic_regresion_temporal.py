import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from temporal_features import calc_temporate_feauters
from prepare_data import get_edgeList
from logistic_regression import AUC

def link_prediction_temporal(dataset, s):

    edgeList = get_edgeList(dataset)
    time_list = [edge[2] for edge in edgeList]
    qs = np.percentile(time_list, s)  # qs - s-й процентиль списка timestamp'ов

    features, y = calc_temporate_feauters(dataset, qs)
    # print(features)


    X = []
    X = list(features.values())
    # print(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    logistic_model = LogisticRegression(max_iter=100000)
    logistic_model.fit(X_train, y_train)
    #
    predictions = logistic_model.predict(X_test)
    #
    print(classification_report(y_test, predictions))


    AUC(X_test, y_test, logistic_model)
