
import numpy as np
from components.graph import Graph
from components.calc_static_features import Static_calculator
from components.calc_temp_features import Temporal_calculator
from components.calc_properties import Properties_calculator
from components.bin_classificator import Bin_classificator
import random

#1 Вычислений свойств графа
def task1(file):
  graph_properties = Properties_calculator()
  graph_properties.calc(file)


#2.1 Вычисление статических признаков и построение ROC AUC кривой для статич. признаков
def task2_prep(graph, max):
  
  #В папке done находятся статические признаки для всех ребер датасетов (заархивировано чтобы можно было загрузить на гитхаб)
  print('запускаем калькулятор')
  static_features = Static_calculator()
  static_features.calc(graph, max)  #случайный перебор
  random.shuffle(graph.static_features) #перемешиваем случайным образом полученные признаки
  graph.write_static_results_to_csv()
  clasificator = Bin_classificator()

  #75% данных используется для обучения и 25% данных используется для тестирования
  clasificator.static(graph.static_features, graph.name) # Построение ROC кривой для статических признаков  Common Neighbours (CN); Adamic-Adar (AA); Jaccard Coefficient (JC); Preferential Attachment (PA)


def task2_prep_with_distance(graph, max):
  
  #В папке done находятся статические признаки для всех ребер датасетов (заархивировано чтобы можно было загрузить на гитхаб)
  print('находим соседей на расстоянии 2')
  graph.find_neighbors_at_distance_2()
  print('запускаем калькулятор')
  static_features = Static_calculator()
  static_features.calc2(graph, max) #на расстоянии 2
  random.shuffle(graph.static_features) #перемешиваем случайным образом полученные признаки
  graph.write_static_results_to_csv()
  clasificator = Bin_classificator()

  #75% данных используется для обучения и 25% данных используется для тестирования
  clasificator.static(graph.static_features, graph.name) # Построение ROC кривой для статических признаков  Common Neighbours (CN); Adamic-Adar (AA); Jaccard Coefficient (JC); Preferential Attachment (PA)

def task2(graph):
  graph.read_static_results_from_csv()
  clasificator = Bin_classificator()
  clasificator.static(graph.static_features, graph.name)

def task2(graph):
  graph.read_static_results_from_csv()
  clasificator = Bin_classificator()
  clasificator.static(graph.static_features, graph.name)

def task3_slow(graph):
  graph.get_time()
  l = 0.2
  temporal_features = Temporal_calculator(l, graph.tmin, graph.tmax)
  temporal_features.calc(graph)
  clasificator = Bin_classificator()
  clasificator.temporal(graph.temporal_features, graph.name)


def task3(graph, file, max):
  temporal_features = Temporal_calculator()
  temporal_features.calc(graph, file, max)
  clasificator = Bin_classificator()
  clasificator.temporal(graph.temporal_features, graph.name)



print('Выберите датасет (введите название): ')
file = input()          #edges     #nodes
#file = 'BA_bitA_0prep'  #24 186    #3 783
#file = 'BO_bitOt_0prep' #35 592    #5 881
#file = 'RA_Rado_0prep'  #82 927    #167
#file = 'UC_UC_0prep'    #59 835    #1 899


max = 10000

print('Чтение датасета...')

graph = Graph()                       #Cоздаем обьект граф
graph.prep(file)                      #Проверяем в нужном ли формате датасет и при необходимости подготавливаем csv
graph.read_from_csv(file)             #Читаем данные из файла
print ('Датасет прочитан')


#task1(file)                          # Задание 1, вычисление свойств графа
#task2_prep(graph,max)                # Задание 2, вычисление статических признаков 
#task2_prep_with_distance(graph,max)  # Задание 2, вычисление статических признаков на расстоянии 2
#task2(graph)                         # Задание 2, чтение готовых статических признаков из done
task3(graph, file, max)              # Задание 3, вычисление темпоральных признаков
print(file)

























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















