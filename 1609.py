class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution(object):
    def isEvenOddTree(self, root):
        if not root:
            return True

        queue = [root]
        level = 0

        while queue:
            level_vals = []
            size = len(queue)

            for _ in range(size):
                node = queue.pop(0)
                val = node.val

                if level % 2 == 0:
                    if val % 2 == 0 or (level_vals and val <= level_vals[-1]):
                        return False
                else:
                    if val % 2 == 1 or (level_vals and val >= level_vals[-1]):
                        return False

                level_vals.append(val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            level += 1

        return True