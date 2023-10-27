
import numpy as np
from second_task_functions.calc_temp_graph_features import calc_static_feature, calc_temp_feature
from second_task_functions.bin_clasification import bin_clasification
from components.graph import Graph
from components.calc_static_features import Static_calculator
from components.calc_properties import Properties_calculator





print('Выберите датасет (введите название): ')
#file = input()
file = 'RA_Rado_0prep'
print('Вычисление...')

graph = Graph()
graph.prep(file)
graph.read_from_file(file)

#1 Вычислений свойств графа
#graph_properties = Properties_calculator()
#graph_properties.calc(file)

#2.1 Вычисление статических признаков
#В папке done находятся статические признаки для всех ребер датасетов (заархивировано чтобы можно было загрузить на гитхаб)
static_features = Static_calculator()
static_features.calc(graph)
graph.write_static_results_to_csv()

#2.2 Вычисление темпоральных признаков















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















