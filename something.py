
### мусор, который может быть пригодится

#  adjList = [[] for _ in range(V)]
#     for line in dataset:
#         [from_ind, to_ind, weight, time] = [int(x) for x in line.split()]
#         adjList[from_ind].append([to_ind, time])
#         adjList[to_ind].append([from_ind, time])

#     print("adjList:")
#     for i in range(V):
#         print(i, ":", end=" ")
#         print(adjList[i])


#     def get_static_graph(adjList, t):
#         for u in range(V):
#             nodesToRemove = []
#             for v in adjList[u]:
#                 if v[1] > t:
#                     nodesToRemove.append(v) 
#             for node in nodesToRemove:
#                 adjList[u].remove(node)
                
#     get_static_graph(adjList, t)

#     print("adjList_modified:")
#     for i in range(V):
#         print(i, ":", end=" ")
#         print(adjList[i])


# #     # # G = nx.from_numpy_array(a)
# #     # # nx.draw_networkx(G)


# all_possible_edges = set(all_possible_edges)
#     pairs_of_vertexes = set(pairs_of_vertexes)

#     remaining_edges = all_possible_edges - pairs_of_vertexes

#     print("remaining_edges:", remaining_edges)
#     print("size of remaining_edges:", len(remaining_edges))

#     print("V:", V - 1)

#     edge_list = []
#     for i in range(1, V):
#         for j in range(i, V):
#             if a[i][j] == 1:
#                 edge_list.append((i,j))
#     print(a)
#     print("edge_list:", edge_list)
#     print("size of edge_list:", len(edge_list))

#     positives = []; negatives = []
#     for edge in remaining_edges:
#         if edge in edge_list and len(positives) < 10000:
#             positives.append(edge)
#         elif len(negatives) < 10000:
#             negatives.append(edge)
#         else:
#             break

#     print("positives:", positives)
#     print("size of positives:", len(positives))
            
#     print("positives:", negatives)
#     print("size of negatives:", len(negatives))