# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import defaultdict
class Solution:
    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
          
          def traverse(root, roots_dict, min_left=float('-inf'), max_right=float('inf')):
              
              if root.val <= min_left or root.val >= max_right: # Нарушение принципов бинарного дерева поиска
                  return False
              if root.left==None and root.right==None: # Если узел - лист
                  node = roots_dict.get(root.val, None)
                  if node is not None and root != node: # Присоединяем корень другого дерева
                      root.left = node.left
                      root.right = node.right
                      roots_dict.pop(root.val) # Теперь корень, который присоединили, - не корень общего дерева
              if root.left!=None: # Продолжение обхода налево
                traverse_left = traverse(root.left, roots_dict, min_left, root.val)
              else:
                traverse_left = True

              if root.right!=None: # Продолжение обхода направо
                traverse_right = traverse(root.right, roots_dict, root.val, max_right)
              else:
                traverse_right = True
                      
              return traverse_left and traverse_right
          
          roots_dict = {}
          node_dict = defaultdict(int)
          
          # Проходимся по всем деревьям с составляем словарь корней и
          # словарь узлов c количеством повторений их значений
          for t in trees:
              roots_dict[t.val] = t
              node_dict[t.val] += 1
              if t.left:
                node_dict[t.left.val] += 1
              if t.right:
                node_dict[t.right.val] += 1
          
          # Проходимся по корням деревьев и находим корень с повторением значения 1, 
          # чтобы возможно было построить единое дерево
          for root in trees:
              if node_dict[root.val] == 1:
                # 1-ое условие - получилось соединить в единое дерево
                # 2-ое условие - остался один корень (другие присоединились к общему дереву)
                if traverse(root, roots_dict) and len(roots_dict) == 1: 
                  return root 
                else:
                  return None
          return None
