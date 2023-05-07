class Solution(object):
    def numOfMinutes(self, n, headID, manager, informTime):
        """
        :type n: int
        :type headID: int
        :type manager: List[int]
        :type informTime: List[int]
        :rtype: int
        """
        descendants = [set({}) for i in range(n)]
        BFS_queue = collections.deque()
        employee_time = [0 for i in range(n)]

        BFS_queue.append(headID)
        employee_time[headID] = 0

        for i in range(n):
            if(manager[i]!=-1):
                descendants[manager[i]].add(i)

        while(BFS_queue):
            employee = BFS_queue.popleft()

            for i in descendants[employee]:
                BFS_queue.append(i)
                employee_time[i] = employee_time[employee] + informTime[employee]
        
        return max(employee_time)
