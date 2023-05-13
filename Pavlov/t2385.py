# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def _get_graph(self, root):
        graph, queue = {}, [(root, -1)]
        while queue:
            node, parent = queue.pop(0)
            if parent != -1:
                if parent not in graph:
                    graph[parent] = []
                if node.val not in graph:
                    graph[node.val] = []
                graph[parent].append(node.val)
                graph[node.val].append(parent)
            if node.left:
                queue.append((node.left, node.val))
            if node.right:
                queue.append((node.right, node.val))
        return graph

    def amountOfTime(self, root, start_node):
        answer = 0
        graph, queue, visited = self._get_graph(root), [start_node], {start_node}

        while queue:
            answer += 1
            for _ in range(len(queue)):
                u = queue.pop(0)
                if u not in graph:
                    continue
                for v in graph[u]:
                    if v in visited:
                        continue
                    queue.append(v)
                    visited.add(v)

        return answer - 1
