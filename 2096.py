# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
 
        def is_finded(node: TreeNode, value: int, path: List[str]) -> bool:
            if node.val == value:
                return True
            if node.right and is_finded(node.right, value, path):
                path += "R"
            elif node.left and is_finded(node.left, value, path):
                path += "L"
            return path

        s, d = [], []
        is_finded(root, startValue, s)
        is_finded(root, destValue, d)

        while len(s) and len(d) and s[-1] == d[-1]:
            s.pop()
            d.pop()
        return "".join("U" * len(s)) + "".join(reversed(d))
