class TreeAncestor {
    private sparseTable: number[][] = [];

    constructor(_: number, parentNumbers: number[]) {
        this.sparseTable[0] = [...parentNumbers];
        let isSparseTableFilled = false;

        for (let i = 1; !isSparseTableFilled; ++i) {
            this.sparseTable[i] = new Array(parentNumbers.length).fill(-1);
            isSparseTableFilled = true;

            for (let j = 0; j < parentNumbers.length; ++j) {
                const prevAncestor = this.sparseTable[i - 1][j];

                if (prevAncestor !== -1) {
                    this.sparseTable[i][j] = parentNumbers[prevAncestor];

                    if (this.sparseTable[i][j] !== -1) {
                        isSparseTableFilled = false;
                    }
                }
            }
        }
    }

    getKthAncestor(node: number, k: number): number {
        return k === 0 ? node : k < this.sparseTable.length ?
            this.sparseTable[k - 1][node] : -1;
    }
}
