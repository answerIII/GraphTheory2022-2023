from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class FindElements:

    def __init__(self, root: Optional[TreeNode]):
        # DFS
        self.nodes_values = set()
        self.add_nodes_values(root, 0)
    
    def add_nodes_values(self, root: Optional[TreeNode], idx: int) -> None:
        if root is not None:
            self.nodes_values.add(idx)
            self.add_nodes_values(root.left, idx * 2 + 1)
            self.add_nodes_values(root.right, idx * 2 + 2)

    def find(self, target: int) -> bool:
        return target in self.nodes_values
