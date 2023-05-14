class Solution:
    def gardenNoAdj(self, n: int, paths: List[List[int]]) -> List[int]:
        # множество соседей в графе
        # проверяем в какие цвета уже раскрашены соседи (где какой цветок посажен)
        # выбираем из оставшихся цветов
        # цветов - 4, макс степень вершины - 3
        g = defaultdict(set)
        flowers = set((1, 2, 3, 4))

        for i, j in paths:
            g[i].add(j)
            g[j].add(i)

        answer = [0] * n

        for i in range(1, n + 1):
            used_flower = set()
            for to in g[i]:
                if answer[to - 1] != 0:
                    used_flower.add(answer[to - 1])

            answer[i - 1] = min(flowers - used_flower)

        return answer