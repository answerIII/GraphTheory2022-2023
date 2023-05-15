import "sort"

func dfs(
    globalReachArray []bool,
    reached *[]int,
    dfsStack []int,
    vertex int,
    edges [][]int,
) {
    dfsStackLength := 1
    dfsStack[0] = vertex
    globalReachArray[vertex] = true

    *reached = (*reached)[:0]
    *reached = append(*reached, vertex)

    for dfsStackLength > 0 {
        currentVertex := dfsStack[dfsStackLength - 1]
        dfsStackLength--

        for _, edge := range edges {
            if edge[0] == currentVertex && !globalReachArray[edge[1]] {
                globalReachArray[edge[1]] = true
                *reached = append(*reached, edge[1])
                dfsStack[dfsStackLength] = edge[1]
                dfsStackLength++
            }

            if edge[1] == currentVertex && !globalReachArray[edge[0]] {
                globalReachArray[edge[0]] = true
                *reached = append(*reached, edge[0])
                dfsStack[dfsStackLength] = edge[0]
                dfsStackLength++
            }
        }
    }
}

func minimumHammingDistance(
    source []int,
    target []int,
    allowedSwaps [][]int,
) int {
    distance := len(source)
    dfsStack := make([]int, len(source))
    globalReachArray := make([]bool, len(source))
    reached := make([]int, len(source))
    reachedSource := make([]int, len(source))
    reachedTarget := make([]int, len(source))

    for i := 0; i < len(source); i++ {
        if globalReachArray[i] {
            continue
        }

        dfs(globalReachArray, &reached, dfsStack, i, allowedSwaps)

        reachedSourceIndex := 0
        reachedTargetIndex := 0
        sameElementsNumber := 0
        reachedLength := 0

        for _, j := range reached {
            reachedSource[reachedLength] = source[j]
            reachedTarget[reachedLength] = target[j]
            reachedLength++
        }

        sort.Ints(reachedSource[:reachedLength])
        sort.Ints(reachedTarget[:reachedLength])

        for reachedSourceIndex < reachedLength &&
                reachedTargetIndex < reachedLength {
            if reachedSource[reachedSourceIndex] <
                    reachedTarget[reachedTargetIndex] {
                reachedSourceIndex++
            } else if reachedSource[reachedSourceIndex] >
                    reachedTarget[reachedTargetIndex] {
                reachedTargetIndex++
            } else {
                sameElementsNumber++
                reachedSourceIndex++
                reachedTargetIndex++
            }
        }

        distance -= sameElementsNumber
    }

    return distance
}
