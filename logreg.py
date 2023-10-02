from sklearn.linear_model import LogisticRegression
from sklearn import metrics, model_selection
from matplotlib import pyplot as plt
import pandas as pd


def concat_dfs(df1, df2):
    for col in df2.columns:
        df1[col] = df2[col]
    return df1

def fit_logreg(X: pd.DataFrame, y: pd.Series) -> LogisticRegression:
    logreg = LogisticRegression(C=0.01, penalty='l2')
    logreg.fit(X, y)
    return logreg


def test_logreg(logreg: LogisticRegression, X: pd.DataFrame, y: pd.Series):
    y_pred = logreg.predict(X)
    return metrics.classification_report(y, y_pred, zero_division=1)


def roc_auc_curve(logreg: LogisticRegression, X: pd.DataFrame, y: pd.Series, name: str):
    predict_proba = logreg.predict_proba(X)[::, 1]
    fpr, tpr, thresholds = metrics.roc_curve(y, predict_proba)
    auc = metrics.roc_auc_score(y, predict_proba)
    fig = plt.figure()
    plt.rc("font", size=14)
    plt.plot(fpr, tpr, label=f'auc={str(round(auc, 5))}')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(name)
    plt.legend(loc="lower right")
    return fig


def train(df: pd.DataFrame, name: str):
    train_df, test_df = model_selection.train_test_split(df, test_size=0.25, random_state=0)

    logreg = fit_logreg(train_df.drop(columns=['flag']), train_df['flag'])
    fig = roc_auc_curve(logreg, test_df.drop(columns=['flag']), test_df['flag'], name)
    return fig


def save_figure(name, static_flag=True):
    if not static_flag:
        plt.savefig('III_results/' + name)
    else:
        plt.savefig('static_results/' + name)
    plt.close()
