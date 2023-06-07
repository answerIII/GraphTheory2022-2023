from logistic_regression import link_prediction, link_prediction_temporal
from basic_features import print_basic_properties

datasets = {
    1:'Rado', 2:'UC', 3:'EU', 4:'Dem', 5:'bitA', 6: 'bitOT',
    7:'SX-MO', 8:'D-rep', 10:'loans', 
    21:'small-graph', 22:'assortativity-example'
}

print("Введите номер датасета: ", end="")
n = int(input())
print("Выбранный датасет:", datasets[n])

f = open('datasets\\' + datasets[n] + '.txt', 'r')
dataset = f.readlines()
s = 66

while True:
    print("****************** \n1 - посчитать статические свойства \n2 - запустить логистическую регрессию со статическими признаками \n" +
          "3 - запустить логистическую регрессию с темпоральными признаками \n4 - выбрать другой датасет\n******************")
    option = input()
    match option:
        case "1":
            print("Проводим рассчеты...")
            print_basic_properties(dataset)
        case "2":
            print("Проводим рассчеты...")
            link_prediction(dataset, s)
        case "3":
            print("Проводим рассчеты...")
            link_prediction_temporal(dataset, s)
        case "4":
            print("Введите номер датасета: ", end="")
            n = int(input())
            print("Выбранный датасет:", datasets[n])

            f = open('datasets\\' + datasets[n] + '.txt', 'r')
            dataset = f.readlines()
        case _:
            print("Code not found")
            break


f.close()