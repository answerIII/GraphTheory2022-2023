func findCycle(m map[int][]int, visited []bool, favorite []int, iter int, maxCycleLen int) ([]bool, int) {
	visited[iter] = true
	current_chain_len := map[int]int{} // карта для хранения длины цикла на текущей итерации
	current_chain_len[iter] = 0
	cycle_count := 0
	for j := 1; j > 0; j++ {
		next := favorite[iter]
		count, ok := current_chain_len[next]
		if ok {
			currentLen := cycle_count - count + 1
			if maxCycleLen < currentLen {
				maxCycleLen = currentLen
			}
			break
		}
		if visited[next] {
			break
		}
		visited[next] = true
		cycle_count += 1
		current_chain_len[next] = cycle_count
		iter = next
	}
	return visited, maxCycleLen
}

func BFS(m map[int][]int, root int, visited []bool, pair_node int) ([]bool, int) {
	n := 1
	queue := []int{}
	current_chain_len := map[int]int{} // карта для хранения длины цикла на текущей итерации
	current_chain_len[root] = 1
	queue = append(queue, root)
	for i := 1; i != 0; i = len(queue) {
		node := queue[0]
		next := m[node]
		for j := 0; j < len(next); j++ {
			next_node := next[j]
			if next_node == pair_node {
				continue
			}
			current_chain_len[next_node] = current_chain_len[node] + 1
			queue = append(queue, next_node)
			n = MAX(n, current_chain_len[next_node])
		}
		queue = queue[1:]
		visited[node] = true
	}
	return visited, n
}

func MAX(a int, b int) int {
	if a > b {
		return a
	}
	return b
}

func maximumInvitations(favorite []int) int {
	// Есть два случая, один из которых будет ответом:
	// 1) Существует цикл наибольшей длины
	// 2) Существует несколько парных вершин, образующих цикл. Здесь нужно найти сумму максимальных путей от этих вершин до листов в реверсивном дереве и сложить длины всех таких парных вершин
	// 1 случай
	maxCycleLen := 0
	m := map[int][]int{} // Карта где ключ - вершина из которого выходит ребро, значение - конец ребра
	invm := map[int][]int{} // Карта где ключ - вершина в которую входит ребро, значение - начало ребра
	for i := 0; i < len(favorite); i++ {
		next := favorite[i]
		m[i] = append(m[i], next)
		invm[next] = append(invm[next], i)
	}
	visited := make([]bool, len(favorite))
	//Найдём с помощью DFS'а
	for i := 0; i < len(favorite); i++ {
		if !visited[i] {
			visited, maxCycleLen = findCycle(m, visited, favorite, i, maxCycleLen)
		}
	}
	//2 случай
	maxPairCycle := 0
	visited = make([]bool, len(favorite))
	for i := 0; i < len(favorite); i++ {
		if visited[i] == true {
			continue
		}
		// вершина является favorite от своего favorite
		if favorite[favorite[i]] == i {
			visited, n1 := BFS(invm, i, visited, favorite[i])
			visited, n2 := BFS(invm, favorite[i], visited, i)
			maxPairCycle += n1 + n2
		}
	}
	return MAX(maxPairCycle, maxCycleLen)
}
