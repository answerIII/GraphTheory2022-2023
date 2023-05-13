class FindElements:
    def __init__(self, root):
        self.node_values = {}
        self._traverse_tree(root, 0)

    def _traverse_tree(self, node, val):
        if node is None:
            return
        node.val = val
        self.node_values[val] = True
        self._traverse_tree(node.left, 2 * val + 1)
        self._traverse_tree(node.right, 2 * val + 2)

    def find(self, target):
        return target in self.node_values
