from typing import List
from itertools import islice
from collections import deque

WHITE, GRAY, BLACK = 0, 1, 2

class Solution:
    def maximumInvitations(self, favorite: List[int]) -> int:
        size = len(favorite)
        max_employees_cycles_of_2 = 0
        max_cycle = 0
        
        # transpose graph
        transposed = [[] for _ in range(size)]
        for node_idx, parent_idx in enumerate(favorite):
            transposed[parent_idx].append(node_idx)
        
        visited = [WHITE] * size
        
        for start_idx in range(len(favorite)):
            if visited[start_idx] != WHITE:
                continue
            
            vertex_idx = start_idx
            
            while visited[vertex_idx] == WHITE:
                visited[vertex_idx] = GRAY
                vertex_idx = favorite[vertex_idx]
            
            cycle_length = 0
            while visited[vertex_idx] == GRAY:
                visited[vertex_idx] = BLACK
                vertex_idx = favorite[vertex_idx]
                cycle_length += 1
            
            depths_sum = 0
            for _ in range(cycle_length):
                depth = Solution.findMaxDepth(transposed, vertex_idx, visited)
                vertex_idx = favorite[vertex_idx]
                depths_sum += depth
            
            if cycle_length == 2:
                max_employees_cycles_of_2 += 2 + depths_sum
            max_cycle = max(max_cycle, cycle_length)
        return max(max_cycle, max_employees_cycles_of_2)
    
    @staticmethod
    def findMaxDepth(children: List[List[int]], from_idx: int, visited: List[bool]):
        cur_depth_indices, new_depth_indices = [], [from_idx]
        depth = 0    
        
        while new_depth_indices:
            cur_depth_indices, new_depth_indices = new_depth_indices, []
            depth += 1
            
            for index in cur_depth_indices:
                for child in children[index]:
                    if visited[child] != BLACK:
                        visited[child] = BLACK
                        new_depth_indices.append(child)
                        
        return depth - 1
