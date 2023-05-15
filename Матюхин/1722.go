package main

import "sort"

func dfs(
    globalReachArray []bool,
    reachArray []bool,
    dfsStack []int,
    vertex int,
    edges [][]int,
) {
    dfsStackLength := 1
    dfsStack[0] = vertex
    globalReachArray[vertex] = true

    for i := range reachArray {
        reachArray[i] = false
    }

    reachArray[vertex] = true

    for dfsStackLength > 0 {
        currentVertex := dfsStack[dfsStackLength - 1]
        dfsStackLength--

        for _, edge := range edges {
            if edge[0] == currentVertex && !reachArray[edge[1]] {
                globalReachArray[edge[1]] = true
                reachArray[edge[1]] = true
                dfsStack[dfsStackLength] = edge[1]
                dfsStackLength++
            }

            if edge[1] == currentVertex && !reachArray[edge[0]] {
                globalReachArray[edge[0]] = true
                reachArray[edge[0]] = true
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
    reachArray := make([]bool, len(source))
    reachedSource := make([]int, len(source))
    reachedTarget := make([]int, len(source))

    for i := 0; i < len(source); i++ {
        if globalReachArray[i] {
            continue
        }

        dfs(globalReachArray, reachArray, dfsStack, i, allowedSwaps)

        reachedSourceIndex := 0
        reachedTargetIndex := 0
        sameElementsNumber := 0
        reachedLength := 0

        for j := 0; j < len(source); j++ {
            if reachArray[j] {
                reachedSource[reachedLength] = source[j]
                reachedTarget[reachedLength] = target[j]
                reachedLength++
            }
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
