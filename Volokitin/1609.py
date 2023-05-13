class Solution:
    def isEvenOddTree(self, root: Optional[TreeNode]) -> bool:
        out = [1]
        traverse(root, out)
        return out[0]

def traverse(root, out):
    if root.val % 2 == 0:
        out[0] = 0
        return
    
    level_old_node = []
    level_old_val = []
    
    if root.left != None:
        level_old_node.append(root.left)
        level_old_val.append(root.left.val)
    if root.right != None:
        level_old_node.append(root.right)
        level_old_val.append(root.right.val)

    if len(level_old_val) == 0:
        return

    if check(level_old_val, 0) == 0:
        out[0] = 0
        return

    curr = 1    

    while True:
        level_new_node = []
        level_new_val = []
        for i in range(len(level_old_node)):
            if level_old_node[i].left != None:
                level_new_node.append(level_old_node[i].left)
                level_new_val.append(level_old_node[i].left.val)
            if level_old_node[i].right != None:
                level_new_node.append(level_old_node[i].right)
                level_new_val.append(level_old_node[i].right.val)
        level_old_node = level_new_node
        level_old_val = level_new_val

        if len(level_new_node) == 0:
            return

        if check(level_new_val, curr) == 0:
            out[0] = 0
            return

        curr += 1
        
def check(arr, num_type):
    if num_type % 2 == 1:
        for i in range(len(arr) - 1):
            if arr[i] >= arr[i + 1]:
                return 0
            if arr[i] % 2 == 0:
                return 0
        if arr[-1] % 2 == 0:
            return 0
    if num_type % 2 == 0:
        for i in range(len(arr) - 1):
            if arr[i] <= arr[i + 1]:
                return 0
            if arr[i] % 2 == 1:
                return 0
        if arr[-1] % 2 == 1:
            return 0
    return 1