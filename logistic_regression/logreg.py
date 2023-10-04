from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from matplotlib import pyplot as plt
import pandas as pd
import pickle

def fit_logreg(X: pd.DataFrame, y: pd.Series) -> LogisticRegression:
    logreg = LogisticRegression(C = 0.01, penalty = 'l2')
    logreg.fit(X, y)    
    return logreg
    
    
def test_logreg(logreg: LogisticRegression, X: pd.DataFrame, y: pd.Series):
    y_pred = logreg.predict(X)
    return metrics.classification_report(y, y_pred, zero_division=1)


def roc_auc_curve(logreg: LogisticRegression, X: pd.DataFrame, y: pd.Series):
    pred_proba = logreg.predict_proba(X)[::,1]
    fpr, tpr, thresholds = metrics.roc_curve(y, pred_proba)
    auc = metrics.roc_auc_score(y, pred_proba)
    fig = plt.figure()
    plt.rc("font", size=14)
    plt.plot(fpr, tpr, label=f'auc={str(round(auc, 5))}')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    return fig


def save_file(data, save_path: str):
    if (type(data) == plt.Figure):
        plt.savefig(save_path)
    else:
        with open(save_path, 'wb') as file:
            pickle.dump(data, file)


if __name__ == '__main__':
    import preproc_data
    
    train, test = preproc_data.load_data('features/digg-friends.txt')
    X_train, y_train = preproc_data.split_data(train)
    X_test, y_test = preproc_data.split_data(train)
    
    logreg = fit_logreg(X_train, y_train)
    fig = roc_auc_curve(logreg, X_test, y_test)
    
    plt.savefig("FIG")