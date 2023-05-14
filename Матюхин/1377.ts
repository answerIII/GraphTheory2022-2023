interface FrogDFSStackElement {
    currentTime: number,
    currentVertex: number,
}

function frogDFSPushEdge(
    edge: number[],
    dfsStack: FrogDFSStackElement[],
    currentTime: number,
    currentVertex: number,
    currentVertexChildren: number,
    vertexProbability: number[],
) {
    const edgeIndex = [edge[0] - 1, edge[1] - 1];
    const nextTime = currentTime + 1;

    if (
        edge[0] === currentVertex &&
        vertexProbability[edgeIndex[1]] === null
    ) {
        vertexProbability[edgeIndex[1]] =
            vertexProbability[edgeIndex[0]] *
            (1 / currentVertexChildren);

        dfsStack.push({
            currentTime: nextTime,
            currentVertex: edge[1],
        });
    }
}

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
        let currentVertexChildren = 0;

        edges.forEach((edge) => {
            if (
                edge[0] === currentVertex &&
                vertexProbability[edge[1] - 1] === null ||
                edge[1] === currentVertex &&
                vertexProbability[edge[0] - 1] === null
            ) {
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
            frogDFSPushEdge(
                edge,
                dfsStack,
                currentTime,
                currentVertex,
                currentVertexChildren,
                vertexProbability,
            );

            frogDFSPushEdge(
                [edge[1], edge[0]],
                dfsStack,
                currentTime,
                currentVertex,
                currentVertexChildren,
                vertexProbability,
            );
        });
    }

    return 0;
}
