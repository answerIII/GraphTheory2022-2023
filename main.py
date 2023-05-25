from logistic_regression import link_prediction
from basic_features import print_basic_properties
from logisstic_regresion_temporal import link_prediction_temporal 

datasets = {
    1:'Rado', 2:'UC', 5:'bitA',
    8:'D-rep', 7:'SX-MO', 10:'loans', 
    21:'small-graph', 22:'assortativity-example'
}

print("Введите номер датасета: ", end="")
n = int(input())
print(datasets[n])

f = open('datasets\\' + datasets[n] + '.txt', 'r')
dataset = f.readlines()

while True:
    print("****************** \n1 - посчитать статические свойства \n2 - запустить логистическую регрессию со статическими признаками \n3 - запустить логистическую регрессию с темпоральными признаками\n******************")
    option = input()
    match option:
        case "1":
            print("Проводим рассчеты...")
            print_basic_properties(dataset)
        case "2":
            print("Проводим рассчеты...")
            link_prediction(dataset, 50)
        case "3":
            print("Проводим рассчеты...")
            link_prediction_temporal(dataset, 50)
        case _:
            print("Code not found")
            break


f.close()
