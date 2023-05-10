func highestPeak(isWater [][]int) [][]int {
    m:=len(isWater)
    n:=len(isWater[0])
	height := make([][]int, m)
	for i := range height {
		height[i] = make([]int, n)
	}

    cell_queue:=[][]int{} //очередь клеток итераций BFS

    //инициализация карты высот и добавление в очередь клеток с водой
    for i:=0; i<m;i++{
        for j:=0; j<n;j++{
            if isWater[i][j]==0{
                height[i][j]=-1
            }else{
                height[i][j]=0
                cell_queue=append(cell_queue,[]int{i,j})
            }
        }
    }

    for ok := 1; ok != 0; ok = len(cell_queue) {
		x := cell_queue[0][0]
		y := cell_queue[0][1]
		cur_height := height[x][y]
		if (x-1 >= 0 && height[x-1][y] == -1) { //рассматривается клетка сверху
			height[x-1][y] = cur_height + 1
			cell_queue = append(cell_queue, []int{x - 1, y})
		}
		if (x+1 < m && height[x+1][y] == -1) { //рассматривается клетка снизу
			height[x+1][y] = cur_height + 1
			cell_queue = append(cell_queue, []int{x + 1, y})
		}
		if (y-1 >= 0 && height[x][y-1] == -1) { //рассматривается клетка слева
			height[x][y-1] = cur_height + 1
			cell_queue = append(cell_queue, []int{x, y - 1})
		}
		if (y+1 < n && height[x][y+1] == -1) { //рассматривается клетка справа
			height[x][y+1] = cur_height + 1
			cell_queue = append(cell_queue, []int{x, y + 1})
		}
		cell_queue = cell_queue[1:] //убирается из очереди первый элемент
	}
	return height
}