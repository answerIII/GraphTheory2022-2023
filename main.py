from data_preporating import prep
import numpy as np
from static_graph_features import calc_static_features
from static_topological_features import calc_stf
from LogReg import regression_model
from temporal_features import calc_dtf_events
from temporal_features import calc_dtf
#from legacy_static_features import leg_calc_stf
#from legacy_topological_features import leg_calc_dtf, leg_calc_dtf_events
print('Введите название нужного файла из папки datasets (без расширения): ')
file = input()
file = prep(file)
print('Файл обработан')
while True:
    print('Для вычесления: \n -характеристик статического графа - нажмите 1 \n Для построения регрессии на: \n  -статических параметрах - нажмите 2 \n - временных в обычном графе - 3 \n -временных в мультиграфе - 4 \n  Для выхода - любой другой символ:' )
    choose = input()
    if choose == '1':
        calc_static_features(file)
        break
    elif choose =="2":
        X, Y = calc_stf(file, 66)
        # X, Y = leg_calc_stf(file, 66)
        regression_model((np.array(X), np.array(Y)))
        break
    elif choose=='3':
        X, Y = calc_dtf(file, 66)
        # X, Y = leg_calc_dtf(file, 66)
        regression_model((np.array(X), np.array(Y)))
        break
    elif choose=='4':
        X, Y = calc_dtf_events(file, 66)
        # X, Y = leg_calc_dtf_events(file, 66)
        regression_model((np.array(X), np.array(Y)))
        break
    else:
        break


