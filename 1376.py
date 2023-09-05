def informEmployees(n, headID, manager, informTime):
    subordinates = {}
    for i, mgr in enumerate(manager):
        if i != headID:
            if mgr not in subordinates:
                subordinates[mgr] = []
            subordinates[mgr].append(i)

    def dfs(employee_id):
        if employee_id not in subordinates:
            return 0
        max_time = 0
        for subordinate in subordinates[employee_id]:
            max_time = max(max_time, dfs(subordinate))
        return max_time + informTime[employee_id]

    return dfs(headID)

# Пример:
n = 6
headID = 2
manager = [2, 2, -1, 2, 2, 2]
informTime = [0, 0, 1, 0, 0, 0]

result = informEmployees(n, headID, manager, informTime)
print(result)  # 1

