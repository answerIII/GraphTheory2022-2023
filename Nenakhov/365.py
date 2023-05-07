class Solution(object): 
    def canMeasureWater(self, jug1Capacity, jug2Capacity, targetCapacity):
        """
        :type jug1Capacity: int
        :type jug2Capacity: int
        :type targetCapacity: int
        :rtype: bool
        """
        my_stack = collections.deque()
        my_stack.append((0,0))
        memory = set((0,0))
        #пройдемся DFS-ом
        while my_stack:
            arr = my_stack.pop()
            a = arr[0]
            b = arr[1]
            if a+b == targetCapacity:
                return True
            #смотрим все возможные дальнейшие операции, которые доступны из условия
            for i in [(jug1Capacity,b), (a,jug2Capacity), (0,b), (a,0), (min(a+b,jug1Capacity), max(b-(jug1Capacity-a),0)), (max(a-(jug2Capacity-b),0),min(a+b,jug2Capacity))]:
                if i not in memory:
                    memory.add(i)
                    my_stack.append(i)
        return False 
