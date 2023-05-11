class Solution:
    def countPairs(self, root, distance):
        self.result = 0  
        #поиск в глубину
        def dfs(node):
            if not node: return [] # если null
            if not node.left and not node.right: return [1] # если лист <=> нет наследников
            # рекурсивно вызываем поиск для потомков
            left_list = dfs(node.left)
            right_list = dfs(node.right)
            # в результате будет сумма всех значений из левого и правого списков
            self.result += sum(l+r <= distance for l in left_list for r in right_list) 
            # возвращается список элементов которые мы рассматриваем, и запоминаем именно дистанцию
            # +1 для учета спуска
            return [1+item for item in left_list+right_list]
        
        dfs(root)
        return self.result 
