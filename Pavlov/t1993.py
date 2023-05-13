class LockingTree:
    def __init__(self, parent):
        self.parent, self.children = parent, [[] for _ in range(len(parent))]
        for i in range(1, len(parent)):
            self.children[parent[i]].append(i)
        self.locked = [-1] * len(parent)

    def lock(self, num, user):
        if self.locked[num] != -1:
            return False
        self.locked[num] = user
        return True

    def unlock(self, num, user):
        if self.locked[num] != user:
            return False
        self.locked[num] = -1
        return True

    def _has_locked_child(self, num):
        stack = [num]
        while stack:
            curr_node = stack.pop()
            if self.locked[curr_node] != -1:
                return True
            stack += self.children[curr_node]
        return False

    def _has_locked_parent(self, num):
        curr_node = self.parent[num]
        while curr_node != -1:
            if self.locked[curr_node] != -1:
                return True
            curr_node = self.parent[curr_node]
        return False

    def _unlock_children(self, num):
        self.locked[num] = -1
        for child in self.children[num]:
            self._unlock_children(child)

    def upgrade(self, num, user):
        if self.locked[num] != -1:
            return False
        if not self._has_locked_child(num):
            return False
        if self._has_locked_parent(num):
            return False
        self._unlock_children(num)
        self.locked[num] = user
        return True
