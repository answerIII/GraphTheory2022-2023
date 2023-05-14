function frogPosition(
    numberVertices: number,
    edges: number[][],
    targetTime: number,
    targetVertex: number,
): number {
    const vertexProbability = new Array(numberVertices).fill(null);
    const dfsStack = [{ currentTime: 0, currentVertex: 1 }];
    vertexProbability[0] = 1;

    while (dfsStack.length !== 0) {
        const { currentTime, currentVertex } = dfsStack.pop()!;
        const nextTime = currentTime + 1;
        let currentVertexChildren = 0;

        edges.forEach((edge) => {
            if (edge[0] === currentVertex) {
                ++currentVertexChildren;
            }
        });

        if (
            targetVertex === currentVertex && (
                targetTime === currentTime ||
                currentVertexChildren === 0 &&
                targetTime >= currentTime
            )
        ) {
            return vertexProbability[currentVertex - 1];
        }
    
        edges.forEach((edge) => {
            const fromVertexIndex = edge[0] - 1;
            const toVertexIndex = edge[1] - 1;

            if (
                edge[0] === currentVertex &&
                vertexProbability[toVertexIndex] === null
            ) {
                vertexProbability[toVertexIndex] =
                    vertexProbability[fromVertexIndex] *
                    (1 / currentVertexChildren);

                dfsStack.push({
                    currentTime: nextTime,
                    currentVertex: edge[1],
                });
            }
        });
    }

    return 0;
}
