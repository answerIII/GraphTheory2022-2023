/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
type FindElements struct {
  	data map[int]bool
}



func Constructor(root *TreeNode) FindElements {
  	data := make(map[int]bool)
		root.Val = 0
 		data = recovery(root, data)
  	return FindElements{data: data}
}

func recovery(root *TreeNode, data map[int]bool) map[int]bool {
  	if root == nil {
				return data
		}
		data[root.Val] = true
		if root.Left != nil {
				root.Left.Val = root.Val*2 + 1
				data = recovery(root.Left, data)
		}
		if root.Right != nil {
				root.Right.Val = root.Val*2 + 2
				data = recovery(root.Right, data)
		}
		return data
}


func (this *FindElements) Find(target int) bool {
    return this.data[target]
}


/**
 * Your FindElements object will be instantiated and called as such:
 * obj := Constructor(root);
 * param_1 := obj.Find(target);
 */