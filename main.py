from data_preporating import prep
from static_graph_features import calc_static_features
print('Введите название нужного файла из папки datasets (без расширения): ')
file = input()
file = prep(file)
print('Файл обработан')
while True:
    print('Для вычесления характеристик статического графа нажмите 1, для выхода - любой символ:' )
    choose = input()
    if choose == '1':
        calc_static_features(file)
        break
    else:
        break