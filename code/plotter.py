import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_curve, roc_auc_score
from .features.feature_extraction import compute_features, save, load

def read(path:str):
    return pd.read_pickle(path)
    #Here, supposedly, you can implement
    # a function that runs everything before that
    # if the file is from the dataset,
    # or simply downloads the pickle if the file is .pickle
    
def get_best_params(data: dict):
    edges_labels = data['edges_labels']
    static_array = data['static']
    answers = edges_labels[:, 2]
    
    static_normalized = StandardScaler().fit_transform(static_array)
    
    param_grid = {'penalty': ['l1', 'l2'],
              'C': [0.001, 0.01, 0.1, 1, 10, 100],
              'solver': ['liblinear', 'saga'],
             'max_iter': [1000]}
    
    logistic_regression = LogisticRegression()
    grid_search = GridSearchCV(logistic_regression, param_grid, cv=5)
    grid_search.fit(static_normalized, answers)
    best_params = grid_search.best_params_
    print("Best Parameters:", best_params)
    return best_params

def pipeline(path:str):
    data = read(path)
    fit_and_plot_roc(data)

def fit_and_plot_roc(data: dict):
    edges_labels = data['edges_labels']
    static_array = data['static']
    second_a_array = data['second_a']
    answers = edges_labels[:, 2]
    
    static_normalized = StandardScaler().fit_transform(static_array)
    
    model_static = LogisticRegression(C=10, max_iter=1000, penalty='l1', solver='saga')
    model_static.fit(static_normalized, answers)
    
    second_a_normalized = StandardScaler().fit_transform(second_a_array)
    
    model_second_a = LogisticRegression(max_iter=1000, penalty='l1', solver='liblinear')
    model_second_a.fit(second_a_normalized, answers)
    
    plt.figure(figsize=(10, 6))

    plt.subplot(1, 2, 1)
    predictions_static = model_static.predict_proba(static_normalized)[:, 1]
    fpr, tpr, thresholds = roc_curve(answers, predictions_static)
    auc_score = roc_auc_score(answers, predictions_static)
    plt.plot(fpr, tpr, label='ROC curve (AUC = {:.3f})'.format(auc_score))
    plt.plot([0, 1], [0, 1], 'k--') 
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic(static)')
    plt.legend(loc='lower right')
    
    plt.subplot(1, 2, 2)
    predictions_second_a = model_second_a.predict_proba(second_a_normalized)[:, 1]
    fpr, tpr, thresholds = roc_curve(answers, predictions_second_a)
    auc_score = roc_auc_score(answers, predictions_second_a)
    plt.plot(fpr, tpr, label='ROC curve (AUC = {:.3f})'.format(auc_score))
    plt.plot([0, 1], [0, 1], 'k--') 
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic(second_a)')
    plt.legend(loc='lower right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    pipeline('features_compiled/radoslaw_email.pickle')
