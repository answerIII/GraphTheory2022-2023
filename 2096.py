# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def find_paths(self, root, startValue: int, destValue, curr_path: str,
                   direction: str):
        if not root:
            return
        curr_path.append(direction)
        if root.val == startValue:
            self.paths[0] = curr_path.copy()
        if root.val == destValue:
            self.paths[1] = curr_path.copy()

        self.find_paths(root.left, startValue, destValue, curr_path, 'L')
        self.find_paths(root.right, startValue, destValue, curr_path, 'R')
        curr_path.pop(-1)

    def getDirections(self, root: Optional[TreeNode], startValue: int,
                      destValue: int) -> str:
        self.paths = [[], []]
        self.find_paths(root, startValue, destValue, [], '')
        start_path, dest_path = self.paths[0], self.paths[1]
        while len(start_path) > 0 and len(dest_path) > 0:
            if start_path[0] != dest_path[0]:
                break
            start_path.pop(0)
            dest_path.pop(0)
        start_path = 'U' * len(start_path)
        return start_path + ''.join(dest_path)
