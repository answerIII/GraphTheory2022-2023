
import numpy as np


from functions.data_preporating import prep
from functions.calc_graph_features import calc_static_features
from calc_temp_graph_features import calc_temp_features
from calc_temp_graph_features import calc_temp_features2
from calc_temp_graph_features import calc_temp_features1

print('Выберите датасет (введите название): ')
file = input()

print('Вычисление...')



#1 Вычисление статических признаков
file = prep(file)
calc_static_features(file)

#2 Вычисление предсказания появления ребер в графе
  # В папке done хранятся статические признаки для всех ребер датасетов
#calc_temp_features(file)

  # Задание 2.1
#calc_temp_features1(file)
  # Задание 2.2
#calc_temp_features2(file)










