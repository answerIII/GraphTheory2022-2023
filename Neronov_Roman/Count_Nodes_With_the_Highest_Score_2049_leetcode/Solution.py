class Solution:
    
    def countHighestScoreNodes(self, parents: List[int]) -> int:

        def subtree_sizes_and_node_score(node, children_list_of_lists, sizes_list,scores_list,num_nodes):
            """
            Рекурсивная функция для вычисления размера всех 
            поддеревьев, исходящих их данного узла. 
            """
            for child in children_list_of_lists[node]:
                subtree_sizes_and_node_score(child, children_list_of_lists, sizes_list,scores_list,num_nodes)
                sizes_list[node] += sizes_list[child] # прибавляем размер поддерева
                scores_list[node] *= sizes_list[child]
            
            scores_list[node] *= num_nodes - sizes_list[node] #(*)
    
        num_nodes = len(parents)
        children_list_of_lists = [[] for _ in range(num_nodes)]
        
        # Создаем список детей для каждого узла
        for child, parent in enumerate(parents[1:]): # убираем проверку на корневую вершину
            children_list_of_lists[parent].append(child+1)
        # список сумм размеров поддеревьев для каждой вершины, включая корень поддерева
        sizes_list = [1] * num_nodes # учитываем саму вершину

        # список скоров для вершин дерева
        scores_list = [1] * num_nodes # далее произведение размеров

        # вычисляем суммарные размеры поддеревьев
        subtree_sizes_and_node_score(0, children_list_of_lists, sizes_list,scores_list,num_nodes) 
        
        # чтобы избежать проверки на корень при умножении на размер дерева, к которому крепится вершина (*)
        scores_list[0]=1
        for child in children_list_of_lists[0]:
            scores_list[0] *= sizes_list[child]


        max_score = 0
        count = 0
        for i in range(num_nodes):
            if scores_list[i] > max_score:
                max_score=scores_list[i]
                count=0
            if scores_list[i] == max_score:
                count += 1

        return count
        
