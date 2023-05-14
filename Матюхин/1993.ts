interface LockingTreeNode {
    childNumbers: number[];
    lockedBy: number | null;
    parentNumber: number;
}

class LockingTree {
    private nodes: LockingTreeNode[];

    constructor(parentNumbers: number[]) {
        this.nodes = parentNumbers.map((parentNumber: number) => ({
            parentNumber,
            childNumbers: [],
            lockedBy: null,
        }));

        parentNumbers.forEach((parentNumber: number, nodeNumber: number) => {
            if (parentNumber !== -1) {
                this.nodes[parentNumber].childNumbers.push(nodeNumber);
            }
        });
    }

    lock(nodeNumber: number, user: number): boolean {
        const node = this.nodes[nodeNumber];

        if (node.lockedBy !== null) {
            return false;
        }
    
        node.lockedBy = user;
        return true;
    }

    unlock(nodeNumber: number, user: number): boolean {
        const node = this.nodes[nodeNumber];

        if (node.lockedBy !== user) {
            return false;
        }
        
        node.lockedBy = null;
        return true;
    }

    upgrade(nodeNumber: number, user: number): boolean {
        let currentNodeNumber = nodeNumber;

        while (currentNodeNumber !== -1) {
            const currentNode = this.nodes[currentNodeNumber];

            if (currentNode.lockedBy !== null) {
                return false;
            }

            currentNodeNumber = currentNode.parentNumber;
        }

        if (!this.isAnyChildLocked(nodeNumber)) {
            return false;
        }

        this.unlockAllChildren(nodeNumber);
        this.nodes[nodeNumber].lockedBy = user;
        return true;
    }

    private isAnyChildLocked(nodeNumber: number): boolean {
        return this.nodes[nodeNumber].childNumbers.some((childNumber) => {
            return this.nodes[childNumber].lockedBy !== null ||
                this.isAnyChildLocked(childNumber);
        });
    }

    private unlockAllChildren(nodeNumber: number): void {
        this.nodes[nodeNumber].childNumbers.forEach((childNumber) => {
            this.nodes[childNumber].lockedBy = null;
            this.unlockAllChildren(childNumber);
        });
    }
}
