function getReachableFrom(
    numberVertices: number,
    vertex: number,
    edges: number[][],
) {
    const reachArray = new Array(numberVertices).fill(false);
    const bfsQueue = [vertex];
    reachArray[vertex] = true;

    while (bfsQueue.length !== 0) {
        const currentVertex = bfsQueue.shift();

        edges.forEach((edge) => {
            if (edge[0] === currentVertex && !reachArray[edge[1]]) {
                reachArray[edge[1]] = true;
                bfsQueue.push(edge[1]);
            }
        })
    }

    return reachArray;
}

function checkIfPrerequisite(
    numberCourses: number,
    prerequisites: number[][],
    queries: number[][],
): boolean[] {
    const reachMatrix = Array.from(
        new Array(numberCourses),
        (_, index) => getReachableFrom(numberCourses, index, prerequisites),
    );

    return queries.map((query) => reachMatrix[query[0]][query[1]]);
};
