from collections import deque
from typing import List


class Solution:
    def highestPeak(self, isWater: List[List[int]]) -> List[List[int]]:
        array = deque([])
        visited = set()
        kor_1, kor_2 = len(isWater), len(isWater[0])
        for i in range(kor_1):
            for j in range(kor_2):
                if isWater[i][j] == 1:
                    array.append((i, j, 0))
                    visited.add((i, j))
        result = [[0 for c in range(kor_2)] for c in range(kor_1)]
        while array:
            size = len(array)
            for c in range(size):
                i, j, height = array.popleft() # удаляет и возвращает первый элемент очереди
                for a, b in [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]:
                    if 0 <= a < kor_1 and 0 <= b < kor_2 and (a, b) not in visited:
                        visited.add((a, b))
                        array.append((a, b, height + 1))
                        result[a][b] = height + 1
        return result
