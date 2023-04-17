# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def countV(self, root: TreeNode) -> int:
        # implementation simple DFS
        if root is None:
            return 0
        else:
            return self.countV(root.left) + self.countV(root.right) + 1 
    
    def search(self, node: TreeNode, x: int) -> TreeNode:
        if node is None:
            return None

        if node.val == x:
            return node
        left = self.search(node.left, x)
        right = self.search(node.right, x)
        return left if left is not None else right


    def btreeGameWinningMove(self, root: Optional[TreeNode], n: int, x: int) -> bool:

        redNode = self.search(root, x)

        leftTree = self.countV(redNode.left)
        rightTree = self.countV(redNode.right)
        parentTree = n - (leftTree + rightTree + 1)
        mx = max(leftTree, rightTree, parentTree)
        if mx is leftTree:
            return mx > rightTree + 1 + parentTree
        elif mx is rightTree:
            return mx > leftTree + 1 + parentTree
        else:
            return mx > leftTree + 1 + rightTree
