from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc
from matplotlib import pyplot as plt

from prepare_data import prepare_data_all, prepare_data_at_dist_2_static, prepare_data_at_dist_2_temp
from static_features import calc_four_static_properties
from temporal_features import calc_temporate_feauters
import pylab


def AUC(X_test, Y_test, logistic_model):
    if sum(Y_test) != 0 and sum(Y_test) != len(Y_test):
        lr_predictions = logistic_model.predict_proba(X_test)
        lr_probs = lr_predictions[:, 1]
        # рассчитываем ROC AUC
        lr_auc = roc_auc_score(Y_test, lr_probs)
        print('LogisticRegression: ROC AUC=%.3f' % (lr_auc))
        # рассчитываем roc-кривую
        fpr, tpr, treshold = roc_curve(Y_test, lr_probs)
        roc_auc = auc(fpr, tpr)
        # строим график
        plt.plot(fpr, tpr, color='darkorange',
                 label='ROC кривая (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC-кривая')
        plt.legend(loc="lower right")
        plt.show()
        pylab.show()
    else:
        print('y_test содержит либо все 1, либо все 0')


def link_prediction(dataset, s):

    [V, qs, adjList, nonexistent_edges, y] = prepare_data_at_dist_2_static(dataset, s, display_interm_results=False)

    # for i in range(V):
    #     print(i, ":", end=" ")
    #     print(adjList[i])

    X = []
    for edge in nonexistent_edges:
        features = calc_four_static_properties(adjList, edge, display_interm_results=False)
        X.append(features)
        

    # for i in range(len(nonexistent_edges)):
    #     print(nonexistent_edges[i], ":", X[i])



    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)



    logistic_model = LogisticRegression()
    logistic_model.fit(X_train, y_train)


    predictions = logistic_model.predict(X_test)

    print(classification_report(y_test, predictions))
    
    AUC(X_test, y_test, logistic_model)


    
def link_prediction_temporal(dataset, s):
    
    [V, qs, adjList, nonexistent_edges, y] = prepare_data_at_dist_2_temp(dataset, s, display_interm_results=False)



    features, y = calc_temporate_feauters(dataset, nonexistent_edges, qs)
    #print(features)

    # for _list in features:
    #     print(_list)


    X = []
    X = list(features.values())
    # # print(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    logistic_model = LogisticRegression(max_iter=100000)
    logistic_model.fit(X_train, y_train)
    
    predictions = logistic_model.predict(X_test)
    
    print(classification_report(y_test, predictions))


    AUC(X_test, y_test, logistic_model)
