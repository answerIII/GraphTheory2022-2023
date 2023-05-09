# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class FindElements:
    def recover(self, cursor: TreeNode, new_val: int):
        self.vals.append(new_val)
        if cursor.left:
            self.recover(cursor.left, 2 * new_val + 1)
        if cursor.right:
            self.recover(cursor.right, 2 * new_val + 2)

    def __init__(self, root: Optional[TreeNode]):
        self.vals = []
        self.recover(root, 0)

    def find(self, target: int) -> bool:
        return target in self.vals

# Your FindElements object will be instantiated and called as such:
# obj = FindElements(root)
# param_1 = obj.find(target)