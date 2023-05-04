from collections import defaultdict
class Solution:
    def magnificentSets(self, n: int, edges: List[List[int]]) -> int:
      
      def BFS(start_node,edges_dict):
            node_deque = [start_node]
            prev_layer_node = set()
            visited = set([start_node])
            num_of_layer = 0
            
            while node_deque:
                next_layer = set()
                for node in node_deque:
                    for adj_node in edges_dict[node]:
                        if adj_node not in visited:
                            next_layer.add(adj_node)  
                        elif adj_node in prev_layer_node:
                            continue
                        else: # ребро с более ранними группами - противоречие условию
                            return -1, None
                for node in next_layer:
                    visited.add(node)
                prev_layer_node = set(node_deque)
                node_deque = list(next_layer)
                num_of_layer+=1
            return num_of_layer, visited
      
      edges_dict = defaultdict(set)
      for u, v in edges:
        edges_dict[u].add(v)
        edges_dict[v].add(u)

      result = defaultdict(int)
      # Из каждой вершины запустим BFS
      for i in range(1,n+1):
            num_of_groups, visit = BFS(i,edges_dict)
            if visit==None:
                return -1
            min_node_num = min(visit) # узел минимального номера определяет набор групп (на случай более одной КС)
            # Каждый набор групп начинается с минимального узла, 
            # а ширина набора групп определяется максимальной длиной цепочки узлов, 
            # связанных между собой и соединенных с минимальным узлом.
            result[min_node_num] = max(result[min_node_num], num_of_groups) # на случай, если граф не связен
      return sum(result.values())    


            
