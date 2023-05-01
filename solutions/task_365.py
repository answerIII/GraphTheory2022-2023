class Solution(object):
    def canMeasureWater(self, jug1Capacity, jug2Capacity, targetCapacity):
        """
        :type jug1Capacity: int
        :type jug2Capacity: int
        :type targetCapacity: int
        :rtype: bool
        """
        repeat = set()

        def dfs(curr):
            if curr == targetCapacity:
                return True
            if curr < 0 or curr in repeat or curr > jug1Capacity + jug2Capacity:
                return False
            repeat.add(curr)

            return dfs(curr + jug1Capacity) or\
                dfs(curr - jug1Capacity)or\
                dfs(curr + jug2Capacity)or\
                dfs(curr - jug2Capacity)
                
        return dfs(0)