class Solution:
    def isSubPath(self, head: Optional[ListNode], root: Optional[TreeNode]) -> bool:
        out = [0]
        main_dfs(root, head, out)
        return out[0]

def main_dfs(root, head, out):
    if out[0] == 1:
        return

    sub_dfs(root, head, out)

    if root.left != None:
        main_dfs(root.left, head, out)
    if root.right != None:
        main_dfs(root.right, head, out)

def sub_dfs(root, head, out):
    if head.next == None and (head.val == root.val):
        out[0] = 1
        return
    
    if root.val == head.val:
        if root.left != None:
            sub_dfs(root.left, head.next, out)
        if root.right != None:
            sub_dfs(root.right, head.next, out)
    return