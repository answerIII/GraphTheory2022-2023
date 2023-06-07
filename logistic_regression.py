from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay, RocCurveDisplay
from matplotlib import pyplot as plt

from prepare_data import prepare_data_at_dist_2
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

    [V, qs, adjList, nonexistent_edges, y] = prepare_data_at_dist_2(dataset, s, display_interm_results=False)

    X = []
    for edge in nonexistent_edges:
        features = calc_four_static_properties(adjList, edge, display_interm_results=False)
        X.append(features)
        

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)


    logistic_model = LogisticRegression()
    logistic_model.fit(X_train, y_train)


    predictions = logistic_model.predict(X_test)

    print(classification_report(y_test, predictions))

    cm = confusion_matrix(y_test, predictions, labels=logistic_model.classes_)
    disp_t = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=logistic_model.classes_)
    disp_t.plot()
    disp_t.ax_.set_title('Confusion Matrix (static)')
    plt.show()
    
    AUC(X_test, y_test, logistic_model)


    
def link_prediction_temporal(dataset, s):
    
    [V, qs, adjList, nonexistent_edges, y] = prepare_data_at_dist_2(dataset, s, display_interm_results=False)


    X = calc_temporate_feauters(dataset, nonexistent_edges, qs)
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    logistic_model = LogisticRegression(max_iter=10000)
    logistic_model.fit(X_train, y_train)
    
    predictions = logistic_model.predict(X_test)
    
    print(classification_report(y_test, predictions))

    cm = confusion_matrix(y_test, predictions, labels=logistic_model.classes_)
    disp_t = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=logistic_model.classes_)
    disp_t.plot()
    disp_t.ax_.set_title('Confusion Matrix (static)')
    plt.show()

    AUC(X_test, y_test, logistic_model)
