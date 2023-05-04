class Solution:
    def closestNodes(self, root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
    
        def DFS(root,node_values_list):
            if not root: # если root == null
                return
            node_values_list.append(root.val) 
            DFS(root.left,node_values_list)
            DFS(root.right,node_values_list)
        
        node_values_list = []
        ans = []

        DFS(root,node_values_list) # добавляем все значения узлов дерева в список

        size = len(node_values_list) # кол-вл узлов

        node_values_list.sort() # сортировка списка

        for querie in queries:
            
            # бинарный поиск querie в node_values_list
            l_b = 0
            h_b = size-1
            while h_b - l_b > 1:
                mid = l_b + (h_b - l_b) // 2
                if node_values_list[mid] < querie:
                    l_b = mid
                elif node_values_list[mid] > querie:
                    h_b = mid
                else:
                    ans.append([querie, querie])
                    break;
            else:
                # добавляем в список ответов(ans) min и max для querie
                if node_values_list[l_b] == querie:
                    ans.append([node_values_list[l_b], node_values_list[l_b]])

                elif node_values_list[h_b] == querie:
                    ans.append([node_values_list[h_b], node_values_list[h_b]])
                
                elif node_values_list[0] > querie:
                    ans.append([-1, node_values_list[0]])

                elif node_values_list[size-1] < querie:
                    ans.append([node_values_list[size-1], -1])

                else:
                    ans.append([node_values_list[l_b], node_values_list[h_b]])

        return ans
