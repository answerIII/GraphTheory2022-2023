# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sufficientSubset(self, root: Optional[TreeNode], limit: int) -> Optional[TreeNode]:
      
      # Для листовой вершины
      if root.left==None and root.right==None:
        if root.val < limit:
          return None 
        else:
          return root
     
      # спуск по левому поддереву с изменением остаточного лимита
      if root.left: 
        root.left = self.sufficientSubset(root.left, limit - root.val)
      
      # спуск по правому поддереву с изменением остаточного лимита
      if root.right: 
        root.right = self.sufficientSubset(root.right, limit - root.val)
      
      # Если не удалены правое и левое поддерево, значит не все пути имеют суммарную стоимость
      # меньше лимита
      if root.left or root.right:
        return root
      else:
        return None
      
