# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def dfs(self, head: Optional[ListNode], root: Optional[TreeNode]):
        left_path, right_path = False, False
        if not head:
            return True
        if head.val == root.val:
            if not head.next:
                return True
            if root.left:
                left_path = self.dfs(head.next, root.left)
            if root.right:
                right_path = self.dfs(head.next, root.right)

        return left_path or right_path

    def isSubPath(self, head: Optional[ListNode],
                  root: Optional[TreeNode]) -> bool:
        head_path = False
        if not root:
            return False
        if not head:
            return True
        if root.val == head.val:
            head_path = self.dfs(head, root)

        left_path = self.isSubPath(head, root.left)
        right_path = self.isSubPath(head, root.right)

        return left_path or right_path or head_path



