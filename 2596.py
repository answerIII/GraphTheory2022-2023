class Solution:
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        # составляем словарь шагов фигуры НомерШага[Координаты]
        # для каждого шага: если разница с предыдущим по xy = (2,1) или (1,2), то все ок
        n = len(grid)
        dict_steps = {}
        for i in range(n):
            for j in range(n):
                dict_steps[grid[i][j]] = [i, j]

        if grid[0][0] != 0:
            return False

        for step in range(n ** 2 - 1):
            if step + 1 in dict_steps:
                x_dif = abs(dict_steps[step][0] - dict_steps[step + 1][0])
                y_dif = abs(dict_steps[step][1] - dict_steps[step + 1][1])
            else:
                return False
            if not ((x_dif == 2 and y_dif == 1) or (x_dif == 1 and y_dif == 2)):
                return False
        return True