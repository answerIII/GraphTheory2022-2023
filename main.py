from logistic_regression import link_prediction
from basic_features import print_basic_properties

datasets = {
    1:'Rado', 2:'UC', 5:'bitA',
    8:'D-rep', 7:'SX-MO', 10:'loans', 
    21:'small-graph', 22:'assortativity-example'
}

print("Введите номер датасета: ")
n = int(input())
f = open('datasets\\' + datasets[n] + '.txt', 'r')
dataset = f.readlines()

# while True:
#     option = input()
#     match option:
#         case "1":
#             print("OK")
#         case "2":
#             print("Not Found")
#         case "3":
#             print("I'm a teapot")
#         case _:
#             print("Code not found")
#             break

#print_basic_properties(dataset)
link_prediction(dataset)

f.close()