# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def printTree(self, root: Optional[TreeNode]) -> List[List[str]]:
        from collections import deque

        q = deque()
        q.append(root)
        h = -1
        # Проходимся по всем вершинам и находим высоту дерева
        while(q):
            h+=1
            for i in range(len(q)):
                node = q.popleft()
                if (node.left):
                    q.append(node.left)
                if (node.right):
                    q.append(node.right)

        m = h+1
        n = 2**(h+1) - 1
        # Делаем матрицу m*n, заполненную пустыми строками
        res = [['' for _ in range(n)] for _ in range(m)]
        # Изначально вставляем элементы как TreeNode, потом заменим на значения узлов
        res[0][int((n-1)/2)] = root

        for i in range(m):
            for j in range(n):
                # Если пустая ячейка, то пропускаем
                if (res[i][j] == ''):
                    continue
                # Вычисляем координаты потомков
                lri = i+1 # Уровень потомков
                lj = j-2**(h-i-1) # Номер столбца для левого потомка
                rj = j+2**(h-i-1) # Номер столбца для правого потомка

                if (res[i][j].left):
                    res[lri][lj] = res[i][j].left
                if (res[i][j].right):
                    res[lri][rj] = res[i][j].right
                if (res[i][j]):
                    res[i][j] = str(res[i][j].val)

        return res