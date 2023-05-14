interface TreeNode {
    val: number;
    left: TreeNode | null;
    right: TreeNode | null;
}

function isEvenOddTree(root: TreeNode | null): boolean {
    if (root === null) {
        return false;
    }

    return isEvenOddSubtree(root, 0, []);
}

function isEvenOddSubtree(
    root: TreeNode,
    level: number,
    levelValues: number[],
): boolean {
    const levelEven = level % 2 === 0;
    const valueEven = root.val % 2 === 0;

    if (levelEven && valueEven || !levelEven && !valueEven) {
        return false;
    }

    if (
        level in levelValues && (
            levelEven && levelValues[level] >= root.val ||
            !levelEven && levelValues[level] <= root.val
        )
    ) {
        return false;
    }

    levelValues[level] = root.val;

    if (
        root.left !== null &&
        !isEvenOddSubtree(root.left, level + 1, levelValues) ||
        root.right !== null &&
        !isEvenOddSubtree(root.right, level + 1, levelValues)
    ) {
        return false;
    }

    return true;
}
