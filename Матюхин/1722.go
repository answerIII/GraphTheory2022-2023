import "sort"

func dfs(
    globalReachArray []bool,
    reached *[]int,
    dfsStack []int,
    vertex int,
    adjacentVertices []map[int]bool,
) {
    dfsStackLength := 1
    dfsStack[0] = vertex
    globalReachArray[vertex] = true

    *reached = (*reached)[:0]
    *reached = append(*reached, vertex)

    for dfsStackLength > 0 {
        currentVertex := dfsStack[dfsStackLength - 1]
        dfsStackLength--

        for adjacentVertex := range adjacentVertices[currentVertex] {
            if !globalReachArray[adjacentVertex] {
                globalReachArray[adjacentVertex] = true
                *reached = append(*reached, adjacentVertex)
                dfsStack[dfsStackLength] = adjacentVertex
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
    adjacentVertices := make([]map[int]bool, len(source))
    dfsStack := make([]int, len(source))
    globalReachArray := make([]bool, len(source))
    reached := make([]int, len(source))
    reachedSource := make([]int, len(source))
    reachedTarget := make([]int, len(source))

    for mapKey := range adjacentVertices {
        adjacentVertices[mapKey] = make(map[int]bool)
    }

    for _, allowedSwap := range allowedSwaps {
        adjacentVertices[allowedSwap[0]][allowedSwap[1]] = true
        adjacentVertices[allowedSwap[1]][allowedSwap[0]] = true
    }

    for i := 0; i < len(source); i++ {
        if globalReachArray[i] {
            continue
        }

        dfs(globalReachArray, &reached, dfsStack, i, adjacentVertices)

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
