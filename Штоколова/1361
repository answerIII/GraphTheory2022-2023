class Solution:
   
    def dfs(self, i: int, leftChild: list[int], rightChild: list[int], inp: list[int], out: list[int]) -> bool:
        out[i] = 1
        if (leftChild[i] == -1 and rightChild[i] == -1) or inp[i] == 0 and ((rightChild[i] == -1 and inp[leftChild[i]] == 0 and out[leftChild[i]] == 1) or (leftChild[i] == -1 and inp[rightChild[i]] == 0 and out[rightChild[i]] == 1)): 
            return True 
           
        elif leftChild[i] == -1 and inp[rightChild[i]] != 1:
            inp[rightChild[i]] = 1 
            return self.dfs(rightChild[i], leftChild, rightChild, inp, out)

        elif rightChild[i] == -1 and inp[leftChild[i]] != 1: 
            inp[leftChild[i]] = 1
            return self.dfs(leftChild[i], leftChild, rightChild, inp, out)
        
        elif (leftChild[i] * rightChild[i] >= 0) and inp[leftChild[i]] + inp[rightChild[i]] == 0: 
            inp[leftChild[i]] = 1
            inp[rightChild[i]] = 1
            a, b = True, True
            if out[leftChild[i]] == 0:
               a = self.dfs(leftChild[i], leftChild, rightChild, inp, out)
            elif out[rightChild[i]] == 0: 
                b = self.dfs(rightChild[i], leftChild, rightChild, inp, out)
            return a and b
        else:
            return False  


    def validateBinaryTreeNodes(self, n: int, leftChild: list[int], rightChild: list[int]) -> bool: 
        inp = [0] * n
        out = [0] * n
        i = 0 
        a = self.dfs(i, leftChild, rightChild, inp, out)
        while a and i < n: 
            i += 1
            if i == n:
                break;
            if out[i]*inp[i] == 1:
                continue
            if out[i] + inp[i] == 0 and not(leftChild[i] == rightChild[i] == -1) and sum(inp) != 0:
                if (leftChild[i] != -1  and out[leftChild[i]] == 0) or (rightChild[i] != -1 and out[rightChild[i]] == 0):
                    return False
            a = self.dfs(i, leftChild, rightChild, inp, out)
        return a 
