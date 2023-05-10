func DFS(tree [][]int, informTime []int, cur_id int) int {
	totalTime := 0
	for i := 0; i < len(tree[cur_id]); i++ {
        next_id:=tree[cur_id][i]
        newTime:=informTime[cur_id]
        if len(tree[next_id]) != 0 {
            newTime = DFS(tree, informTime, next_id)+informTime[cur_id]
        }
		totalTime = int(math.Max(float64(totalTime), float64(newTime)))
	}
	return totalTime
}

func numOfMinutes(n int, headID int, manager []int, informTime []int) int {
    //созданим двумерный массив, где для i-ого человека будет сопоставлен массив с номерами его подчинённых
	tree := make([][]int, n)
	for i := 0; i < n; i++ {
		if i != headID {
			tree[manager[i]] = append(tree[manager[i]], i)
		}
	}
    //пройдёмся по структуре дерева с помощью DFS метода
	totalTime := DFS(tree, informTime, headID)
	return totalTime
}