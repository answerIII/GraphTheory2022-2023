from collections import defaultdict
from typing import List


class Solution:
    def pyramidTransition(self, bottom: str, allowed: List[str]) -> bool:
        blocks = defaultdict(list)

        for a in allowed:
            blocks[a[:2]].append(a[2])

        def dfs(row: str, _next_row: str, k: int) -> bool:
            if len(row) == 1:
                return True
            if len(_next_row) + 1 == len(row):
                return dfs(_next_row, '', 0)

            for i in blocks[row[k:k + 2]]:
                if dfs(row, _next_row + i, k + 1):
                    return True

            return False

        return dfs(bottom, '', 0)
