class TreeAncestor {
    private sparseTable: number[][];

    private dfsSparceTable(adjacentVertices: Set<number>[]): void {
        const reachArray = new Array(adjacentVertices.length).fill(false);
        const dfsStack = [0];

        while (dfsStack.length !== 0) {
            const currentVertex = dfsStack.pop()!;

            if (!reachArray[currentVertex]) {
                for (let j = 1; j < this.sparseTable.length; ++j) {
                    const aboveRow = this.sparseTable[j - 1];
                    const aboveVertex = aboveRow[currentVertex];
                    const currentRow = this.sparseTable[j];

                    if (aboveVertex !== -1) {
                        // Assign 2^j-th ancestor to the current position.
                        currentRow[currentVertex] = aboveRow[aboveVertex];
                    }
                }
            }

            for (const vertex of adjacentVertices[currentVertex]) {
                if (!reachArray[vertex]) {
                    reachArray[currentVertex] = true;
                    dfsStack.push(vertex);
                }
            }
        }
    }

    constructor(_: number, parentNumbers: number[]) {
        const adjacentVertices = Array.from(
            { length: parentNumbers.length },
            () => new Set<number>(),
        );

        this.sparseTable = [[...parentNumbers], ...Array.from({
            length: Math.floor(Math.log2(parentNumbers.length)) + 1,
        }, () => new Array(parentNumbers.length).fill(-1))];

        parentNumbers.forEach((parentNumber, vertex) => {
            if (parentNumber !== -1) {
                adjacentVertices[vertex].add(parentNumber);
                adjacentVertices[parentNumber].add(vertex);
            }
        });

        this.dfsSparceTable(adjacentVertices);
    }

    getKthAncestor(node: number, k: number): number {
        while (k !== 0) {
            if (node === -1) {
                return -1;
            }

            const kPower2 = Math.floor(Math.log2(k));
            node = this.sparseTable[kPower2][node];
            k -= 2 ** kPower2;
        }

        return node;
    }
}
