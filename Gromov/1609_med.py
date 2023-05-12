#Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque

class Solution:
    def isEvenOddTree(self, root: Optional[TreeNode]) -> bool:
        # Если дерево пусто, то оно автоматически является Even Odd Tree
        if root == None:
          return True
        q = deque()
        q.append(root) # Изначально в рассмотрении корневой узел
        k = 0 # Текущий уровень - 0-ой

        while(q):
          prev = None # Предыдущий узел нужен для сравнения
          
          # Рассматриваем k-ый уровень 
          for i in range(len(q)): # Итератор нужен для обновления значение уровня (k) после рассмотрения всех узлов на текущем уровне
            node = q.popleft() # Рассматриваем текущий узел

            # Если четный уровень
            if (k%2 == 0):
              # Проверяем, нечетное ли значение узла
              if (node.val % 2 == 0): 
                # Если четно, то условия Even Odd Tree нарушены - возвращаем False
                return False
              # Проверяем, в строго возрастающем ли порядке расположены узлы
              if (prev and prev.val >= node.val):
                # Если значение предыдущего узла >= значения текущего узла,
                # то условия EvenOdd Tree нарушены - возвращаем False
                return False

            # Если нечетный уровень
            else:
              # Проверяем, четное ли значение узла
              if (node.val % 2 != 0): 
                # Если нечетно, то условия Even Odd Tree нарушены - возвращаем False
                return False
              # Проверяем, в строго убывающем ли порядке расположены узлы
              if (prev and prev.val <= node.val):
                # Если значение предыдущего узла >= значения текущего узла,
                # то условия Even Odd Tree нарушены - возвращаем False
                return False
          
            # Добавляем всех потомков узлов (если они есть), рассматриваемых на уровне
            # Теперь в q лежат все узлы со следующего уровня
            if (node.left):
              q.append(node.left)
            if (node.right):
              q.append(node.right)
            
            # Предыдущий узле для следующего узла - только что рассмотренный узел
            prev = node

          # Переходим к следующему уровню дерева
          k+=1

          # Если никаких нарушения условий не было,
          # то рассматриваемое дерево - Even Odd Tree 
        return True