# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def printTree(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[str]]
        """
        h = self.height_tree(root)
        w = 2 ** h - 1
        mass = []
        for i in range(h):
            mass.append([""] * w)

        def dfs(root, left, right, i, mass):
            if root is None:
                return
            temp = (right + left) // 2
            mass[i][temp] = str(root.val)
            i += 1
            dfs(root.left, left, temp - 1, i, mass)
            dfs(root.right, temp + 1, right, i, mass)
            return

        dfs(root, 0, w - 1, 0, mass)

        return mass

    def height_tree(self, root):
        if root is not None:
            right_height = self.height_tree(root.right)
            left_height = self.height_tree(root.left)
            return max(right_height, left_height) + 1
        return 0
