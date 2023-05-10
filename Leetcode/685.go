func findCycle(m map[int][]int, invm map[int][]int, iter int, ln int) (map[int][]int, int) {
	cycle_count := 0
	visited := make([]bool, ln)
	visited[iter] = true
	breaking_node := -1
	queue := []int{}
	queue = append(queue, iter)
	// Найдём вершину, которая ведёт в уже посещённую вершину, от неё будем строить цикл
	for i := 1; i != 0; i = len(queue) {
		node := queue[0]
		next := m[node]
		for j := 0; j < len(next); j++ {
			next_node := next[j]
			if visited[next_node] == false {
				queue = append(queue, next_node)
			} else {
				breaking_node = next_node
				break
			}
		}
		queue = queue[1:]
		visited[node] = true
	}
	cycleMap := map[int][]int{}
	visited = make([]bool, ln)
	visited[breaking_node] = true
	for value, ok := invm[iter]; ok; value, ok = invm[iter] {
		cycle_count += 1
		cycleMap[iter] = []int{}
		iter = value[0]
		if visited[iter] == true {
			break
		}
		visited[iter] = true
	}
	return cycleMap, cycle_count
}

func BFS(m map[int][]int, root int, ln int) int {
	n := 0
	visited := make([]bool, ln)
	visited[root] = true
	queue := []int{}
	queue = append(queue, root)
	for i := 1; i != 0; i = len(queue) {
		node := queue[0]
		next := m[node]
		for j := 0; j < len(next); j++ {
			next_node := next[j]
			if visited[next_node] == false {
				queue = append(queue, next_node)
			}
		}
		queue = queue[1:]
		visited[node] = true
		n += 1
	}
	return n
}

func findRedundantDirectedConnection(edges [][]int) (result []int) {
	// Есть два случая:
	// 1) вершина точно определена
	// 2) вершина где-то в цикле

	// Карты где ключ - узел из которого выходит ребро, значение - конец ребра
	m1 := map[int][]int{}
	m2 := map[int][]int{}
	m := map[int][]int{}
	// Карты где ключ - узел в который входит ребро, значение - начало ребра
	invm1 := map[int][]int{}
	invm2 := map[int][]int{}
	invm := map[int][]int{}
	// Кандидаты, в случае, где есть вершина
	edge_1 := []int{}
	edge_2 := []int{}
	// Инициализация карт
	for i := 0; i < len(edges); i++ {
		next := edges[i][1] - 1
		current := edges[i][0] - 1
		m[current] = append(m[current], next)
		invm[next] = append(invm[next], current)
	}
	// 1 случай
	// Если есть узел, в который входит два ребра - в графе нет цикла, эти два ребра потенциально возможные результаты
	for i := 0; i < len(edges); i++ {
		if len(invm[i]) == 2 {
			edge_1 = append(edge_1, invm[i][0], i)
			edge_2 = append(edge_2, invm[i][1], i)
			break
		}
	}
	if len(edge_1) != 0 {
		root1 := -1
		root2 := -1
		// Инициализация карт без ребёр в прошлом пункте
		for i := 0; i < len(edges); i++ {
			next := edges[i][1] - 1
			current := edges[i][0] - 1
			if current != edge_1[0] || next != edge_1[1] {
				invm1[next] = append(invm1[next], current)
				m1[current] = append(m1[current], next)
			}
			if current != edge_2[0] || next != edge_2[1] {
				invm2[next] = append(invm2[next], current)
				m2[current] = append(m2[current], next)
			}
		}
		// Инициализация корневых узлов
		for i := 0; i < len(edges); i++ {
			_, ok := invm1[i]
			if len(invm1[i]) == 0 || !ok {
				root1 = i
				break
			}
		}
		for i := 0; i < len(edges); i++ {
			_, ok := invm2[i]
			if len(invm2[i]) == 0 || !ok {
				root2 = i
				break
			}
		}
		// Найдём, сколько вершин входит в компоненту связности с корневым узлом, без ребёр
		n1 := BFS(m1, root1, len(edges))
		n2 := BFS(m2, root2, len(edges))
		// Если без какого-то ребра, получилось, что число компоненты связности!=количеству вершин, то одно из ребёр можем выбрать в качестве результата
		if n1 > n2 {
			return []int{edge_1[0] + 1, edge_1[1] + 1}
		}
		if n2 > n1 {
			return []int{edge_2[0] + 1, edge_2[1] + 1}
		}
		// Если они одинаковы, то будем искать первое встретившееся ребро
		if n1 == n2 {
			for i := 0; i < len(edges); i++ {
				next := edges[i][1] - 1
				current := edges[i][0] - 1
				if current == edge_1[0] && next == edge_1[1] {
					return []int{edge_2[0] + 1, edge_2[1] + 1}
				}
				if current == edge_2[0] && next == edge_2[1] {
					return []int{edge_1[0] + 1, edge_1[1] + 1}
				}
			}
		}
	}
	// 2 случай
	// Инициализируем количество вершин в цикле и карту для вершин в цикле
	cycle_count := 0
	cycleMap := map[int][]int{}
	// Найдём цикл и его вершины
	for i := 0; i < len(edges)-1; i++ {
		_, ok := m[i]
		if ok {
			cycleMap, cycle_count = findCycle(m, invm, i, len(edges))
			break
		}
	}
	// Потенциально из цикла можем убрать любое из рёбер, проверяем, какое встречается в цикле последним
	for i := 0; i < len(edges); i++ {
		next := edges[i][1] - 1
		current := edges[i][0] - 1
		// Проверяем есть ли значения с вершинами в цикле
		_, ok1 := cycleMap[current]
		_, ok2 := cycleMap[next]
		if ok1 && ok2 {
			if cycle_count == 1 {
				return edges[i]
			} else {
				cycle_count -= 1
				cycleMap[current] = append(cycleMap[current], next)
			}
		}
	}
	return result
}