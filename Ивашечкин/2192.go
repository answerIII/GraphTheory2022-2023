func getAncestors(n int, edges [][]int) [][]int {
    answer := make ([][]int, n)
    matrix := make([][]int, n)
    
    //для адекватного вида матрицы смежности, т.к. даны лишь рёбра 
    for _, i := range edges {
        matrix[i[0]] = append(matrix[i[0]], i[1])
    }


    for i:=0; i<n; i++ {
        bfs(i, matrix, answer)
    }
    return answer
}

func bfs(i int, edges [][]int, answer [][]int)  {
    visited := make(map[int]bool)
    visited[i] = true

    nextNodes := make([]int, 0)
    nextNodes = append(nextNodes, i)
    for len(nextNodes) > 0 {
        node := nextNodes[0]
        for _, j := range edges[node] {
            if visited[j] == false {
                visited[j] = true
                nextNodes = append(nextNodes, j)
                answer[j] = append(answer[j], i)
            }
        }
        nextNodes = nextNodes[1:]
    }
}