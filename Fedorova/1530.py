# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countPairs(self, root: TreeNode, distance: int) -> int:
        #DFS для обхода. Для потомков рекурсивно вызываем функцию в левом и правом поддеревьях
        #перебираем левый и правый списки и вычисляем количество пар,расстояния которых меньше distance.
        #возвращаем список, содержащий все расстояния от текущего узла до его потомков.
        self.ans = 0

        def dfs(root):
            if not root: return []
            if not root.left and not root.right: return [1]
            left = dfs(root.left)
            right = dfs(root.right)
            for i in left:
                for j in right:
                    if i+j <= distance:
                        self.ans += 1
            return [i+1 for i in left + right]
        dfs(root)
        return self.ans