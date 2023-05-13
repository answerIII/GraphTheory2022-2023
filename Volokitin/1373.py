class Solution:
    def maxSumBST(self, root: Optional[TreeNode]) -> int:
        max_val = [0]
        dfs_main(root, max_val) 
        return max_val[0]
    

def dfs_main(root, max_val):
    if root.left == None and root.right == None:
        return [1, root.val, root.val, root.val]

    left_val, right_val = None, None

    if root.left != None:
        left_val = dfs_main(root.left, max_val)
        if max_val[0] < left_val[1]:
            max_val[0] = left_val[1]
    if root.right != None:
        right_val = dfs_main(root.right, max_val)
        if max_val[0] < right_val[1]:
            max_val[0] = right_val[1]

    if left_val != None and right_val != None:
        if left_val[0] and right_val[0] and left_val[3] < root.val and right_val[2] > root.val:
            ans = root.val + left_val[1] + right_val[1]
            if max_val[0] < ans:
                max_val[0] = ans
            return [1, ans, left_val[2], right_val[3]]
    elif left_val != None:
        if left_val[0] and left_val[3] < root.val :
            ans = root.val + left_val[1]
            if max_val[0] < ans:
                max_val[0] = ans
            return [1, ans, min(root.val, left_val[2]), max(root.val, left_val[3])]
    elif right_val != None:
        if right_val[0] and right_val[2] > root.val :
            ans = root.val + right_val[1]
            if max_val[0] < ans:
                max_val[0] = ans
                print(max_val)
            return [1, ans, min(root.val, right_val[2]), max(root.val, right_val[3])]
            
    return [0, 0, 0, 0]
    