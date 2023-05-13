from bisect import bisect

class Solution:
    def closestNodes(self, root: Optional[TreeNode], queries: List[int]) -> List[List[int]]:
        array = []
        inorder_trav(root, array)
        answer = []
        for num in queries:
            answer.append(b_find(array, num))
        return answer

def inorder_trav(root, array):
    if root.left != None:
        inorder_trav(root.left, array)
    array.append(root.val)
    if root.right != None:
        inorder_trav(root.right, array)

def b_find(array, num):
    out = [0, 0]

    if num > array[-1]:
        out[0] = array[-1]
    if num < array[0]:
        out[0] = -1

    if num < array[0]:
        out[1] = array[0]
    if num > array[-1]:
        out[1] = -1
    
    if out[0] != 0 and out[1] != 0:
        return out
    
    if out[0] != 0 and out[1] == 0:
        out[1] = array[bisect_right(array, num)]
        return out
    if out[0] == 0 and out[1] != 0:
        out[0] = array[bisect_left(array, num)]
        return out
    
    i = bisect(array, num)
    if array[i - 1] == num:
        return [array[i - 1], array[i - 1]]
    else:
        return [array[i - 1], array[i]] 