# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def amountOfTime(self, root: Optional[TreeNode], start: int) -> int:
        def makeGraph(root: TreeNode):
            G = defaultdict(list)

            stack = [(root, None)]
            while stack:
                node, parent = stack.pop()
                if parent:
                    G[parent.val].append(node.val)
                    G[node.val].append(parent.val)
                if node.left: stack.append((node.left, node))
                if node.right: stack.append((node.right, node))
            return G
        
        graph = makeGraph(root)

        def maxWay(G: dict, curr_nodes: list, ) -> int:
            visited = dict()
            while curr_nodes:
                u, time = curr_nodes.pop()

                if u in visited:
                    continue
                
                visited[u] = time
                
                for v in G[u]:
                    if v in visited:
                        continue
                    curr_nodes.append((v, time + 1))
            
            return max(visited.values())
        
        curr_nodes = [(start, 0)]
        return maxWay(graph, curr_nodes)