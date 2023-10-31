import numpy as np
from components.graph import Graph
from components.calc_static_features import Static_calculator
from components.calc_temp_features import Temporal_calculator
from components.calc_properties import Properties_calculator
from components.bin_classificator import Bin_classificator

#1 Вычислений свойств графа
def task1(file):
  graph_properties = Properties_calculator()
  graph_properties.calc(file)

print('Выберите датасет (введите название): ')
file = input()          #edges     #nodes
#file = 'BA_bitA_0prep'  #24 186    #3 783
#file = 'BO_bitOt_0prep' #35 592    #5 881
#file = 'RA_Rado_0prep'  #82 927    #167
#file = 'UC_UC_0prep'    #59 835    #1 899

#file = 'testgraph_1_0prep'

filepath = 'test/' + file
max = 40400

print('Чтение датасета...')
graph = Graph()
graph.prep(filepath)
#graph.read_test_from_csv(file)
print ('Датасет прочитан')

#graph.print_edges()
#graph.find_neighbors_at_distance_2()
#graph.print_neigbours_2()

task1(filepath) #Вычисление свойств графа для тестовых графов без weigh,time
