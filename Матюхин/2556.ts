function dfsUntilLast(
    reachArray: boolean[],
    firstVertex: number,
    lastVertex: number,
    adjacentVertices: Set<number>[],
): boolean {
    const dfsStack = [firstVertex];

    while (dfsStack.length !== 0) {
        const currentVertex = dfsStack.pop()!;
        reachArray[currentVertex] = true;

        for (const vertex of adjacentVertices[currentVertex]) {
            if (vertex === lastVertex) {
                return true;
            }

            if (!reachArray[vertex]) {
                dfsStack.push(vertex);
            }
        }
    }

    return false;
}

function isPossibleToCutPath(grid: number[][]): boolean {
    const rows = grid.length;
    const cols = grid[0].length;
    const size = rows * cols;

    const firstVertex = 0;
    const lastVertex = size - 1;

    if (firstVertex === lastVertex) {
        return false;
    }

    const adjacentVertices =Array.from(
        new Array(size),
        () => new Set<number>(),
    );

    const reachArray = new Array(size).fill(false);

    for (let i = 0; i < rows; ++i) {
        for (let j = 0; j < cols; ++j) {
            if (grid[i][j] === 0) {
                continue;
            }

            const pos = i * cols + j;

            if (j > 0 && grid[i][j - 1] === 1) {
                adjacentVertices[pos].add(pos - 1);
            }

            if (i > 0 && grid[i - 1][j] === 1) {
                adjacentVertices[pos].add(pos - cols);
            }

            if (j < cols - 1 && grid[i][j + 1] === 1) {
                adjacentVertices[pos].add(pos + 1);
            }

            if (i < rows - 1 && grid[i + 1][j] === 1) {
                adjacentVertices[pos].add(pos + cols);
            }
        }
    }

    if (!dfsUntilLast(
        reachArray,
        firstVertex,
        lastVertex,
        adjacentVertices,
    )) {
        return true;
    }

    return !dfsUntilLast(
        reachArray,
        firstVertex,
        lastVertex,
        adjacentVertices,
    );
}
