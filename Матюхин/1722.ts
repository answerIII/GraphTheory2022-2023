function dfs(
    globalReachArray: boolean[],
    reachArray: boolean[],
    vertex: number,
    edges: number[][],
): void {
    reachArray = reachArray.fill(false);
    const dfsStack = [vertex];
    globalReachArray[vertex] = true;
    reachArray[vertex] = true;

    while (dfsStack.length !== 0) {
        const currentVertex = dfsStack.pop();

        edges.forEach((edge) => {
            if (edge[0] === currentVertex && !reachArray[edge[1]]) {
                globalReachArray[edge[1]] = true;
                reachArray[edge[1]] = true;
                dfsStack.push(edge[1]);
            }

            if (edge[1] === currentVertex && !reachArray[edge[0]]) {
                globalReachArray[edge[0]] = true;
                reachArray[edge[0]] = true;
                dfsStack.push(edge[0]);
            }
        })
    }
}

function minimumHammingDistance(
    source: number[],
    target: number[],
    allowedSwaps: number[][],
): number {
    let distance = source.length;
    const globalReachArray = new Array(source.length).fill(false);
    const reachArray = new Array(source.length);
    const reachedSource = new Array(source.length);
    const reachedTarget = new Array(target.length);

    for (let i = 0; i < source.length; ++i) {
        if (globalReachArray[i]) {
            continue;
        }

        dfs(
            globalReachArray,
            reachArray,
            i,
            allowedSwaps,
        );

        let reachedSourceIndex = 0;
        let reachedTargetIndex = 0;
        let sameElementsNumber = 0;
        reachedSource.length = 0;
        reachedTarget.length = 0;

        for (let j = 0; j < source.length; ++j) {
            if (reachArray[j]) {
                reachedSource[reachedSource.length] = source[j];
                reachedTarget[reachedTarget.length] = target[j];
            }
        }

        reachedSource.sort((x, y) => x - y);
        reachedTarget.sort((x, y) => x - y);

        while (
            reachedSourceIndex < reachedSource.length &&
            reachedTargetIndex < reachedTarget.length
        ) {
            if (
                reachedSource[reachedSourceIndex] <
                reachedTarget[reachedTargetIndex]
            ) {
                ++reachedSourceIndex;
            } else if (
                reachedSource[reachedSourceIndex] >
                reachedTarget[reachedTargetIndex]
            ) {
                ++reachedTargetIndex;
            } else {
                ++sameElementsNumber;
                ++reachedSourceIndex;
                ++reachedTargetIndex;
            }
        }

        distance -= sameElementsNumber;
    }

    return distance;
}
