func DFS(grid [][]int, cost [][]int, queue [][]int, directions [][]int, current_cost int, x int, y int, n int, m int) ([][]int, [][]int) {
	if x >= m || y >= n || x < 0 || y < 0 { // вершина вышла за границы массива
		return cost, queue
	}
	for {
		if x >= m || y >= n || x < 0 || y < 0 || current_cost >= cost[x][y] { // вершина вышла за границы массива + не имеет смысла добавлять вершины с большей или равной стоимостью
			return cost, queue
		}
		queue = append(queue, []int{x, y})
		cost[x][y] = current_cost
		next := directions[grid[x][y]]
		x += next[0]
		y += next[1]
	}
}

func minCost(grid [][]int) int {
    // Основная идея - пойти из вершины DFS'ом по стрелкам, параллельно записывая вершины, ориентацию которых можно изменить
	m := len(grid)
	n := len(grid[0])
	inf := 1000000
	directions := [][]int{{0, 0}, {0, 1}, {0, -1}, {1, 0}, {-1, 0}}
	cost := make([][]int, m) // массив минимального пути до вершин
	for i := 0; i < m; i++ {
		cost[i] = make([]int, n)
		for j := 0; j < n; j++ {
			cost[i][j] = inf
		}
	}
	queue := [][]int{} // очередь вершин, у которых можно поменять направление
	cost, queue = DFS(grid, cost, queue, directions, 0, 0, 0, n, m)
	for i := len(queue); i != 0; i = len(queue) {
		next := queue[0]
		for j := 1; j < len(directions); j++ { // проверяем каждое из 4 направлений
			if j == grid[next[0]][next[1]] {
				continue
			}
			dx := directions[j][0]
			dy := directions[j][1]
			x := next[0]
			y := next[1]
			current_cost := cost[x][y] + 1
			x += dx
			y += dy
			cost, queue = DFS(grid, cost, queue, directions, current_cost, x, y, n, m)
		}
		queue = queue[1:]
	}
	return cost[m-1][n-1]
}
