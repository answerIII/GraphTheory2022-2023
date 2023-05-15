func amountOfTime(root *TreeNode, start int) int {
	parent := make(map[int]*TreeNode)
	startNode := &(root)
	initMap(root, parent, start, startNode)
	return infect(*startNode, parent)
}

//функция инициализации мапы родителей. С мапой удобнее работать, нежели с переменной start в infected
func initMap(node *TreeNode, parent map[int]*TreeNode, start int, startNode **TreeNode) {
	if node.Val == start {
		*startNode = node
	}
	if node.Left != nil {
		parent[node.Left.Val] = node
		initMap(node.Left, parent, start, startNode)
	}
	if node.Right != nil {
		parent[node.Right.Val] = node
		initMap(node.Right, parent, start, startNode)
	}
}

//основная функция заражения
func infect(node *TreeNode, parent map[int]*TreeNode) int {
	infected := make(map[int]bool)
	infected[node.Val] = true
	step := 0
	neighbours := []*TreeNode{node} //массив соседей ноды
	for len(neighbours) > 0 {
		nextNodes := make([]*TreeNode, 0, len(neighbours)) //добавляем заражённые ноды для некст рассмотрения их соседей
		for _, node := range neighbours {
			if node.Right != nil && infected[node.Right.Val] == false {
				nextNodes = append(nextNodes, node.Right)
				infected[node.Right.Val] = true
			}
			if node.Left != nil && infected[node.Left.Val] == false {
				nextNodes = append(nextNodes, node.Left)
				infected[node.Left.Val] = true
			}
			if parent[node.Val] != nil && infected[parent[node.Val].Val] == false {
				infected[parent[node.Val].Val] = true
				nextNodes = append(nextNodes, parent[node.Val])
			}
		}
		neighbours = nextNodes
		step++
	}
	return step - 1 //-1 т.к. при единственной ноде у нас ++ будет, но ответ должен быть нулевым по условию
}