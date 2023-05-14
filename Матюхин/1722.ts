function dfs(
    numberVertices: number,
    vertex: number,
    edges: number[][],
    globalReachArray: boolean[],
): boolean[] {
    const reachArray = new Array(numberVertices).fill(false);
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

    return reachArray;
}

function minimumHammingDistance(
    source: number[],
    target: number[],
    allowedSwaps: number[][],
): number {
    let distance = source.length;
    const globalReachArray = new Array(source.length).fill(false);

    for (let i = 0; i < source.length; ++i) {
        if (globalReachArray[i]) {
            continue;
        }

        const reachArray = dfs(
            source.length,
            i,
            allowedSwaps,
            globalReachArray,
        );

        let targetSet = new Set(target.filter((_, index) => reachArray[index]));

        distance -= source.reduce((sum, value, index) => {
            return reachArray[index] && targetSet.has(value) ? sum + 1 : sum;
        }, 0);
    }

    return distance;
}
