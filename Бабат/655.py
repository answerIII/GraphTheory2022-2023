class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def printTree(self, root: Optional[TreeNode]) -> List[List[str]]:
        height = self.getHeight(root)
        rows = height
        cols = (2 ** height) - 1
        res = [["" for _ in range(cols)] for _ in range(rows)]
        mid_col = (cols - 1) // 2
        res[0][mid_col] = str(root.val)
        
        self.placeNodes(root.left, res, 1, 0, mid_col - 1, cols)
        self.placeNodes(root.right, res, 1, mid_col + 1, cols, cols)
        
        return res

    def getHeight(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.getHeight(root.left), self.getHeight(root.right))
    
    def placeNodes(self, node: Optional[TreeNode], res: List[List[str]], row: int, left: int, right: int, cols: int) -> None:
        if not node:
            return
        mid_col = (left + right) // 2
        res[row][mid_col] = str(node.val)
        self.placeNodes(node.left, res, row + 1, left, mid_col - 1, cols)
        self.placeNodes(node.right, res, row + 1, mid_col + 1, right, cols)
