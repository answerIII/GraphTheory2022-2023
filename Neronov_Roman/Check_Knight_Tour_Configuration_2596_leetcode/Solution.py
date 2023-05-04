class Solution:
    def checkValidGrid(self, grid: List[List[int]]) -> bool:
        size = len(grid) # размер поля
        cell_dict={} # словарь ячеек с их номером и координатами
        for row in range(size):
            for col in range(size):
                # формируем словарь ячеек
                cell_dict[grid[row][col]]=(row,col) 
        # проходимся по номерам ячеек по возрастанию и смотрим,
        # чтобы разница по координатам со следующей была 3 при этом
        # изменения ни по одной координате не были 0
        if cell_dict[0][0]!=0 or cell_dict[0][1]!=0:
            return False
        
        for i in range(size*size-1):
            x_dif = abs(cell_dict[i][0]-cell_dict[i+1][0])
            y_dif = abs(cell_dict[i][1]-cell_dict[i+1][1])
            if x_dif+y_dif!=3 or x_dif==0 or y_dif==0:
                return False
        return True
    
