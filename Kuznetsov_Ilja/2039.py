from typing import List

class Solution:
    # @staticmethod
    def networkBecomesIdle(self, edges: List[List[int]], patience: List[int]) -> int:
        # building graph
        vertices_num = len(patience)
        neighbors: List[List[int]] = [[] for _ in range(vertices_num)]
        for from_idx, to_idx in edges:
            neighbors[from_idx].append(to_idx)
            neighbors[to_idx].append(from_idx)
        
        # BFS
        current_step_indices = [0]
        next_step_indices: List[int] = []
        visited = [False] * vertices_num
        visited[0] = True
        
        cur_time = 1
        max_idle_moment = -1
        
        while current_step_indices:
            cur_vertex_idx = current_step_indices.pop()
            for neighbor_idx in neighbors[cur_vertex_idx]:
                if not visited[neighbor_idx]:
                    next_step_indices.append(neighbor_idx)
                    visited[neighbor_idx] = True
                    
                    pat = patience[neighbor_idx]
                    max_idle_moment = max(
                        max_idle_moment,
                        4 * cur_time - (2 * cur_time - 1) % pat
                    )
            
            if not current_step_indices:
                current_step_indices = next_step_indices
                next_step_indices = []
                cur_time += 1
        
        return max_idle_moment