/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func sufficientSubset(root *TreeNode, limit int) *TreeNode {
    if root.Left==nil && root.Right==nil{ //если узел - лист, проверяем условие
        if root.Val<limit{
            return nil
        }else{
            return root
        }
    }
    if root.Left!=nil{ // если есть левый потомок, то запускаем рекурсию с уменьшением limit'а
        root.Left=sufficientSubset(root.Left, limit-root.Val)
    }
    if root.Right!=nil{ // если есть правый потомок, то запускаем рекурсию с уменьшением limit'а
        root.Right=sufficientSubset(root.Right,limit-root.Val)
    }
    if root.Left!=nil || root.Right!=nil{ //если после рекурсий у узла не осталось потомков - этот узел insufficient
        return root
    }
    return nil
}