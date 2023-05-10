from sys import setrecursionlimit
from typing import List

setrecursionlimit(10**5)

class Solution:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        # construct tree
        children: List[List[int]] = [[] for _ in range(n)]
        for employee_idx, manager_idx in enumerate(manager):
            if manager_idx != -1:
                children[manager_idx].append(employee_idx)
        
        # DFS
        return Solution.DFS(children, informTime, headID)

    @staticmethod
    def DFS(children: List[List[int]], informTime: List[int], current_node_idx: int):
        if children[current_node_idx]:
            max_child_time = max(Solution.DFS(children, informTime, child_idx)
                                for child_idx in children[current_node_idx])
            return informTime[current_node_idx] + max_child_time
        return 0

print(Solution().numOfMinutes(n = 6, headID = 2, manager = [2,2,-1,2,2,2], informTime = [0,0,1,0,0,0]))