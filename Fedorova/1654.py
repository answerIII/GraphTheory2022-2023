class Solution:
    def minimumJumps(self, forbidden: List[int], a: int, b: int, x: int) -> int:
        #BFS - Рассматриваем все возможные шаги вперед назад и запоминаем кол-во ходов
        #Во избежании повторов, также запоминаем посещенные позиции (+ шаг сделанный в позиции)
        limit = 2000 + a + b
        visited = set()
        queue = [(0,0,False)]
        while queue:
            new_position,res,step_b = queue.pop(0)
            if new_position in forbidden or (new_position,step_b) in visited:
                continue

            if new_position == x:
                return res

            if new_position + a < limit:
                queue.append((new_position + a,res + 1,False))

            if not step_b and new_position - b > 0:
                queue.append((new_position - b,res + 1,True))
            visited.add((new_position,step_b))
        return -1