/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func kthLargestLevelSum(root *TreeNode, k int) int64 {
    height := 0
    sum := []int64{} 
    sum, height = bfs(root, height)
    if height < k {
        return int64(-1)
    }
    if k > len(sum){
        return -1
    }
    sort.Slice(sum, func(i, j int) bool {
        return sum[i] > sum[j]
    })
    return sum[k-1]
   
}


func bfs(node *TreeNode, height int) ([]int64, int) {
    sum := []int64{}
    if height >= len(sum) { //расширение слайса
        sum = append(sum, 0)
    }
    sum[height] += int64(node.Val) //складываем ноду в свою высоту
    neighbours := []*TreeNode{node} //массив соседей ноды
    for len(neighbours) > 0 {
        height++
        if height >= len(sum) { //расширение слайса
            sum = append(sum, 0)
        }
        nextNodes := make([]*TreeNode, 0, len(neighbours)) 
        for _, node := range neighbours {
            if node.Right != nil {
                nextNodes = append(nextNodes, node.Right)
				sum[height] += int64(node.Right.Val)
            }
            if node.Left != nil {
				nextNodes = append(nextNodes, node.Left)
				sum[height] += int64(node.Left.Val)
			}
        }
        neighbours = nextNodes // расширяем масссив соседей
		
    }
    return sum, height
}