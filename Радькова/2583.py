# Definition for a binary tree node.
# class TreeNode:
#    def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        Q = list([root])
        lvlsum = []

        while Q:
            qlen = len(Q)
            tmpsum = 0

            for i in range(qlen):
                node = Q.pop(0)
                tmpsum += node.val

                if node.left:
                    Q.append(node.left)
                if node.right:
                    Q.append(node.right)

            lvlsum.append(tmpsum)

        if len(lvlsum) < k:
            return -1
        else:
            lvlsum.sort(reverse=True)

            return lvlsum[k-1]