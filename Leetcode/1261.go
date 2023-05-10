/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
type FindElements struct {
  root *TreeNode  
}


func Constructor(root *TreeNode) FindElements {
    // Восстановим значения узлов дерева с помощью BFS метода
    root.Val=0
    node_queue := []*TreeNode{}
	  node_queue = append(node_queue, root)
    for ok := 1; ok != 0; ok = len(node_queue) {
      current_node := node_queue[0]
      x:=current_node.Val
      if current_node.Left != nil {
        current_node.Left.Val=2*x+1
        node_queue = append(node_queue, current_node.Left)
      }
      if current_node.Right != nil {
        current_node.Right.Val=2*x+2
        node_queue = append(node_queue, current_node.Right)
      }
      node_queue = node_queue[1:]
	  }
    var FE FindElements
    FE.root=root
    return FE
}


func (this *FindElements) Find(target int) bool {
    // Проверим, есть ли узел с заданным значением в массиве с помощью BFS метода
    node_queue := []*TreeNode{}
	  node_queue = append(node_queue, this.root)
    for ok := 1; ok != 0; ok = len(node_queue) {
        current_node := node_queue[0]
        if current_node.Val==target{
          return true
        }
        if current_node.Left != nil {
          node_queue = append(node_queue, current_node.Left)
        }
        if current_node.Right != nil {
          node_queue = append(node_queue, current_node.Right)
        }
        node_queue = node_queue[1:]
	  }
    return false
}


/**
 * Your FindElements object will be instantiated and called as such:
 * obj := Constructor(root);
 * param_1 := obj.Find(target);
 */