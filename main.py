from data_preporating import prep
import numpy as np
from static_graph_features import calc_static_features
from static_topological_features import calc_stf
from linear import regression_model
from temporal_features import calc_dtf
print('Введите название нужного файла из папки datasets (без расширения): ')
file = input()
file = prep(file)
print('Файл обработан')
while True:
    print('Для вычесления характеристик статического графа нажмите 1, для вычисления статических параметров - 2, для динамических - 3, для выхода - любой символ:' )
    choose = input()
    if choose == '1':
        calc_static_features(file)
        break
    elif choose =="2":
        X, Y = calc_stf(file)
        regression_model((np.array(X), np.array(Y)))
        break
    elif choose=='3':
        print(calc_dtf(file))
        break
    else:
        break


