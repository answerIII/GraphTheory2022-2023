# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def isSubPath(self, head, root):
        """
        :type head: ListNode
        :type root: TreeNode
        :rtype: bool
        """
        def dfs(root, temp, arr):
            if root is None:
                return

            temp.append(root.val)
            
            if root.left is None and root.right is None:
                arr.append(list(temp))

            dfs(root.left, temp, arr)
            dfs(root.right, temp, arr)
            temp.pop()

            return arr

        arr = dfs(root, [], [])
       
        n = len(arr)
        mass = []
        for i in range(n):
            s = ''
            for j in arr[i]:
                s += str(j)
            mass.append(s)

        temp = ''
        while head:
            temp += str(head.val)
            head = head.next

        for i in mass:
            if temp in i:
                return True

        return False
