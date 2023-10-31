import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, RocCurveDisplay



class Bin_classificator():
    #  X_train набор обучающих признаков, который будет использоваться для обучения модели
    #  X_test  набор тестовых признаков, который будет использоваться для оценки производительности модели
    #  y_train набор обучающих меток (целевой переменной), соответствующих обучающим признакам
    #  y_test  набор тестовых меток (целевой переменной), соответствующих тестовым признакам

    def static(self,features, dataset_name):
        features_df = pd.DataFrame(features)
        X = features_df[['Common Neighbours', 'Adamic-Adar', 'Jaccard Coefficient', 'Preferential Attachment']]
        y = features_df['Def']
        self.plot(X,y, dataset_name)

    def temporal(self,features, dataset_name):
        features = features.sort_values(by='time')
        X = features[['cnwl', 'aawl', 'jcwl', 'pawl', 'cnws', 'aaws', 'jcws', 'paws', 'cnwe', 'aawe', 'jcwe', 'pawe']]
        y = features['def']

        #X = features[['cnwl', 'aawl', 'jcwl', 'pawl', 'cnws', 'aaws', 'jcws', 'paws', 'cnwe', 'aawe', 'jcwe', 'pawe']]
        #y = features['def']
        self.plot(X,y, dataset_name)


    def plot(self, X, y, dataset_name):
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.75, test_size = 0.25)

        lin_reg = LogisticRegression()
        y_score = lin_reg.fit(X_train, y_train).predict_proba(X_test)
        print('Датасет: ' + dataset_name + ' ROC_AUC: '  +  str(roc_auc_score(y_test,y_score[:,1])))
        RocCurveDisplay.from_predictions(y_test, y_score[:,1])
        plt.show()

