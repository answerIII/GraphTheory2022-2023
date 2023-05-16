from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score


def regression_model(data):
    X, Y = data
    #scaler = Normalizer().fit(X)
    #normalized_X = scaler.transform(X)
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, random_state=0)
    lr = LogisticRegression()
    lr.fit(x_train,y_train)
    lr_probs = lr.predict_proba(x_test)
    lr_probs = lr_probs[:, 1]
    lr_auc = roc_auc_score(y_test, lr_probs)
    print('LogisticRegression: ROC AUC=%.3f' % (lr_auc))
    fpr, tpr, treshold = roc_curve(y_test, lr_probs)
    roc_auc = auc(fpr, tpr)
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
    import pickle
    with open('model.pkl', 'wb') as f:
        pickle.dump(lr, f)