from static_features import calc_four_static_properties
from basic_features import print_basic_properties

datasets = {
    1:'testgraph_1', 2:'testgraph_2', 3:'testgraph_3', 4: 'testgraph_4', 5: 'testgraph_5',
    6:'testgraph_6', 7:'testgraph_7', 
    8:'socfb-Middlebury45', 
    9:'socfb-Reed98', 
    10:'team_3'
}

def number_of_vertexes(dataset):
    uniqueVertexes = set()
    for line in dataset:
        [from_ind, to_ind] = [int(x) for x in line.split()]
        uniqueVertexes.add(from_ind)
        uniqueVertexes.add(to_ind)
    return len(uniqueVertexes) + 1

f = open('test_graphs\\' + datasets[6] + '.txt', 'r')
dataset = f.readlines()

print_basic_properties(dataset)


# for i in range(1, 11):
#     f = open('test_graphs\\' + datasets[i] + '.txt', 'r')
#     dataset = f.readlines()

#     print("*********************************")
#     print(datasets[i])

#     V = number_of_vertexes(dataset)
#     adjList = [[] for _ in range(V)]
#     for line in dataset:
#         [from_ind, to_ind] = [int(x) for x in line.split()]
#         adjList[from_ind].append(to_ind)
#         adjList[to_ind].append(from_ind)

#     # delete duplicate edges
#     for i in range(V):
#         _set = set(adjList[i])
#         adjList[i] = list(_set)

#     edge = (1, 2)

#     [CN, AA, JC, PA] = calc_four_static_properties(adjList, edge)

#     print("for edge:", edge)
#     print("CN:" , CN)
#     print("AA:" , AA)
#     print("JC:" , JC)
#     print("PA:" , PA)


#     print("*********************************")

    