from typing import Optional, Dict, List
from pydantic import BaseModel, Field
import numpy as np
import pydantic_numpy.dtype as pnd
from pydantic_numpy import NDArray


class Node(BaseModel):
    number: int
    node_degree: Optional[int]

    def __lt__(self, other):
        return self.number < other.number

    def __eq__(self, other):
        return self.number == other.number


class Edge(BaseModel):
    start_node: Node
    end_node: Node
    weight: int

    def __lt__(self, other):
        return max(self.end_node, self.start_node) < max(other.end_node, other.start_node)
    
    def __eq__(self, other):
        return self.start_node == other.start_node and self.end_node == other.end_node and self.weight == other.weight

    def __str__(self):
        return f'Начальная нода: {self.start_node}; Конечная нода: {self.end_node}; Вес: {self.weight}'
    
    def get_max_node(self):
        return max(self.end_node, self.start_node)


with open('/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/radoslaw_email/out.radoslaw_email_email') as raw_data:
    raw_data.readline()
    raw_data.readline()
    list_of_items = raw_data.read().split('\n')
    list_of_items.pop(-1)
    for item in list_of_items:
        item = item.split(' ')
        item.pop(2)
        if item[0] == item[1]:
            print(item)
        if item[2] != '1':
            print(item)
        # print(item)
        
        # print(item)
        e = Edge(start_node=Node(number=int(item[0])-1),
                 end_node=Node(number=int(item[1])-1),
                 weight=int(item[2]))
        if e.end_node == e.start_node:
            print("Loop DETECTED!!!!")
            print(e)
        # self.edge_list.append(
        #                     (int(item[-1]), 
        #                     Edge(
        #                         start_node=Node(number=int(item[0])-1),
        #                         end_node=Node(number=int(item[1])-1),
        #                         weight=int(item[2]),
        #                         )
        #                     ))
    # ---

    # raw_data.readline()
    # raw_data.readline()
    # a = raw_data.read().split('\n')

    # a.pop(-1)
    # print(a)
    # b = a[0].split(' ')
    # print(b.pop(2))
    # # print(b.pop(2))
    # print(b)


# TEST --------------
# TG = TemporalGraph(path='/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/soc-sign-bitcoinotc/out.soc-sign-bitcoinotc')
# paths = ['/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/email-Eu-core-temporal/email-Eu-core-temporal.txt',
#          '/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/munmun_digg_reply/out.munmun_digg_reply',
#          '/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/opsahl-ucsocial/out.opsahl-ucsocial',
#          '/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/radoslaw_email/out.radoslaw_email_email',
#          '/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/soc-sign-bitcoinalpha/out.soc-sign-bitcoinalpha',
#          '/home/jim/Prjoects/Study/GraphTheory/graph-project-2023/datasets/sx-mathoverflow/out.sx-mathoverflow']
# for i in paths:
#     print('Обрабатывается ', i)
#     start = time.time()
#     TemporalGraph(path=i)
#     end = time.time()
#     print('Done ', i)
#     print('Время обоработки: ', end-start)
# TEST --------------