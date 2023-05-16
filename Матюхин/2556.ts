function isPossibleToCutPath(grid: number[][]): boolean {
    const rows = grid.length;
    const cols = grid[0].length;
    const size = rows * cols;

    if (size === 2) {
        return false;
    }

    const first = 0;
    const last = size - 1;

    const adjacentVertices =Array.from(
        new Array(size),
        () => new Set<number>(),
    );

    const reachArray = new Array(size).fill(false);

    for (let i = 0; i< rows; ++i) {
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

    const dfsStack = [first];
    reachArray[first] = true;

    while (dfsStack.length !== 0) {
        for (const vertex of adjacentVertices[dfsStack.pop()!]) {
            if (!reachArray[vertex]) {
                reachArray[vertex] = true;
                dfsStack.push(vertex);
            } else if (vertex === last) {
                return false;
            }
        }
    }

    return true;
}
