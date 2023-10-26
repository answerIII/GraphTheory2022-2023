
import numpy as np
from first_task_functions.data_preporating import prep
from first_task_functions.calc_graph_features import calc_static_features
from second_task_functions.calc_temp_graph_features import calc_static_feature, calc_temp_feature
from second_task_functions.bin_clasification import bin_clasification
from test import testtt

if __name__ == '__main__':
    from components.graph import Graph
    from components.edge import Edge


print('Выберите датасет (введите название): ')
file = input()
print('Вычисление...')


#1 Вычисление статических признаков
#file = prep(file)
#calc_static_features(file)

#2 Вычисление предсказания появления ребер в графе
  # В папке done находятся статические признаки для всех ребер датасетов (заархивировано чтобы можно было загрузить на гитхаб)


  # Задание 2.1.1 # Вычисление статических признаков
#calc_static_feature(file)
  # Задание 2.1.2 # Вычисление темпоральных признаков
#calc_temp_feature(file)
  # Задание 2.2 Построение ROC AUC кривой
#bin_clasification(file)





testtt(file)






