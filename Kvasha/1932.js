/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode[]} trees
 * @return {TreeNode}
 */
let canMerge = function (trees) {
  let nodesFreq = {};
  let roots = new Map();
  let root;
  let queue = new Array();

  for (let tree of trees) {
    roots.set(tree.val, tree);
    if (tree.left) {
      if (!nodesFreq[tree.left.val]) nodesFreq[tree.left.val] = 0;
      nodesFreq[tree.left.val]++;
    }

    if (tree.right) {
      if (!nodesFreq[tree.right.val]) nodesFreq[tree.right.val] = 0;
      nodesFreq[tree.right.val]++;
    }
  }

  for (let tree of trees) {
    if (!nodesFreq[tree.val]) {
      if (root) return null;
      root = tree;
    }
  }

  if (!root) return null;
  queue.push([root, -Infinity, Infinity]);

  while (queue.length) {
    let [node, min, max] = queue.shift();
    let left = node.left;
    let right = node.right;

    if (node.val <= min || node.val >= max) return null;

    if (left) {
      if (roots.has(left.val)) {
        node.left = roots.get(left.val);
        roots.delete(left.val);
      }
      queue.push([node.left, min, node.val]);
    }

    if (right) {
      if (roots.has(right.val)) {
        node.right = roots.get(right.val);
        roots.delete(right.val);
      }
      queue.push([node.right, node.val, max]);
    }
  }

  if (roots.size === 1) return root;
  return null;
};
