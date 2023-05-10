// type TreeNode struct {
//   Val int
//   Left *TreeNode
//   Right *TreeNode
// }

func printTree(root *TreeNode) [][]string {
    //найдём высоту дерева с помощью BFS метода
	node_queue := []*TreeNode{}
	node_queue = append(node_queue, root)
	height := 0
	lvl_count := 1
	for ok := 1; ok != 0; ok = len(node_queue) {
		if lvl_count == 0 {
			height += 1
			lvl_count = len(node_queue)
		}
		current_node := node_queue[0]
		if current_node.Left != nil {
			node_queue = append(node_queue, current_node.Left)
		}
		if current_node.Right != nil {
			node_queue = append(node_queue, current_node.Right)
		}
		lvl_count -= 1
		node_queue = node_queue[1:]
	}

    //инициализируем массив с результатами
	m := height + 1
	n := int(math.Pow(2, float64(m))) - 1
	res := make([][]string, m)
	for i := range res {
		res[i] = make([]string, n)
	}

    //заполним массив результатов нашим деревом с помощью BFS метода
	positions := [][]int{} // массив с вычисляемыми позициями для узлов дерева
	node_queue = append(node_queue, root)
	positions = append(positions, []int{0, (n - 1) / 2})
	for ok := 1; ok != 0; ok = len(node_queue) {
		current_node := node_queue[0]
		r := positions[0][0]
		c := positions[0][1]
		res[r][c] = strconv.Itoa(current_node.Val)
		if current_node.Left != nil {
			node_queue = append(node_queue, current_node.Left)
			positions = append(positions, []int{r + 1, c - int(math.Pow(2, float64(height-r-1)))})
		}
		if current_node.Right != nil {
			node_queue = append(node_queue, current_node.Right)
			positions = append(positions, []int{r + 1, c + int(math.Pow(2, float64(height-r-1)))})
		}
		node_queue = node_queue[1:]
		positions = positions[1:]
	}
	return res
}
