/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */

func DFS(node *TreeNode, distance int, result int ) ([]int, int){
    if (node.Left==nil && node.Right==nil){ // если узел - лист, создаём массив, в котором будет храниться на i позиции кол-во листов с высотой i
        height_count:=make([]int,distance+1)
        height_count[1]+=1
        return height_count, result
    }
    left:=make([]int,distance+1) // массив левой ветки
    right:=make([]int,distance+1) // массив правой ветки
    if (node.Left!=nil){
        left, result=DFS(node.Left, distance, result)
    }
    if (node.Right!=nil){
        right, result=DFS(node.Right, distance, result)
    }
    // проверим, есть ли пары высоты r+l
    for l:=1;l<len(left);l++{
        for r:=distance-1;r>=0;r--{
            if r+l<=distance{
                result+=(left[l]*right[r])
            }
        }
    }
    // для узлов, у которых есть потомки, перепишем массив с высотами
    height_count:=make([]int,distance)
    for i:=len(height_count)-2;i>=1;i--{
        height_count[i+1]=left[i]+right[i]
    }
    return height_count, result
}

func countPairs(root *TreeNode, distance int) int {
    _,result:=DFS(root, distance, 0)
    return result
}