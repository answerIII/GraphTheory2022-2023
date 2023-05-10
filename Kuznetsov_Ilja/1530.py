from typing import List, Tuple, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def countPairs(self, root: TreeNode, distance: int) -> int:
        ans, _ = Solution.traverse(root, distance)
        return ans
    
    @staticmethod
    def traverse(root: Optional[TreeNode], distance: int) -> Tuple[int, List[int]]:
        default_depths_distr = [0] * (distance + 1)
        if root is None:
            return 0, default_depths_distr
        
        if root.left is None and root.right is None:
            default_depths_distr[1] += 1
            return 0, default_depths_distr
        
        left_pairs, left_depths = Solution.traverse(root.left, distance)
        right_pairs, right_depths  = Solution.traverse(root.right, distance)
        
        good_pairs = left_pairs + right_pairs
        left_partial_sum = 0
        
        for left, right in zip(left_depths, reversed(right_depths)):
            left_partial_sum += left
            good_pairs += right * left_partial_sum
        
        result_distr = [0] + list(map(sum, zip(left_depths, right_depths)))
        result_distr.pop()
        
        return good_pairs, result_distr

# tests
# from math import log2, ceil

# def list_to_root(lst, idx=0):
#     if not idx:
#         lst = lst + [None] * (2 * 2 ** ceil(log2(len(lst))) - len(lst))
    
#     if lst[idx] is None:
#         return None
#     return TreeNode(idx, list_to_root(lst, 2 * idx + 1), list_to_root(lst, 2 * idx + 2))

