from typing import List, Optional, Tuple, Union

class Solution:
    def mostProfitablePath(self, edges: List[List[int]], bob: int, amount: List[int]) -> int:
        # construct tree
        children: List[List[int]] = [[] for _ in range(len(edges) + 1)]
        for start, end in edges:
            children[start].append(end)
            children[end].append(start)
        
        # DFS
        return Solution.DFS(children, amount, 0, bob)[1]

    @staticmethod
    def DFS(children: List[List[int]], amount: List[int],
            current_node_idx: int, bob: int,
            depth: int = 0, visited: Optional[List[bool]] = None) -> Tuple[Union[int, float], int]:
        
        if visited is None:
            visited = [False] * len(children)
        visited[current_node_idx] = True
        
        dist_from_bob = float('inf')
        max_income = float('-inf')

        for child_idx in children[current_node_idx]:
            if not visited[child_idx]:
                dist_from_bob_in_subtree, income = Solution.DFS(
                    children, amount, child_idx, bob, depth + 1, visited
                )

                dist_from_bob = min(dist_from_bob, dist_from_bob_in_subtree)
                max_income = max(max_income, income)

        if current_node_idx == bob:
            dist_from_bob = 0
        else:
            dist_from_bob += 1

        # calculating price, considering Bob's moves
        to_add = amount[current_node_idx]
        if dist_from_bob < depth:
            to_add = 0
        elif dist_from_bob == depth:
            to_add //= 2
        
        # if in leaf
        if max_income == float('-inf'):
            max_income = 0

        return dist_from_bob, max_income + to_add
