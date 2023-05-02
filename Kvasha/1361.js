/**
 * @param {number} n
 * @param {number[]} leftChild
 * @param {number[]} rightChild
 * @return {boolean}
 */
let validateBinaryTreeNodes = function (n, leftChild, rightChild) {
  function findRoot() {
    let root = 0;

    for (let i = 1; i < n; ++i) {
      let l = leftChild[i];
      let r = rightChild[i];
      if (l === root || r == root) root = i;
    }

    return root;
  }

  let root = findRoot();

  let visited = new Map();

  function dfs(node) {
    if (visited.get(node)) return false;

    visited.set(node, true);
    let l = leftChild[node];
    let r = rightChild[node];

    if (l !== -1 && !dfs(l)) return false;
    if (r !== -1 && !dfs(r)) return false;

    return true;
  }

  return dfs(root) && visited.size === n;
};
