/**
 * Definition for a binary tree node.
 * function TreeNode(val, left, right) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.left = (left===undefined ? null : left)
 *     this.right = (right===undefined ? null : right)
 * }
 */
/**
 * @param {TreeNode} root
 * @param {number} limit
 * @return {TreeNode}
 */
var sufficientSubset = function (root, limit) {
  DFS = (root, sum) => {
    if (!root) return null;
    sum += root.val;
    if (!root.left && !root.right) {
      if (sum < limit) return null;
      return root;
    }
    root.left = DFS(root.left, sum);
    root.right = DFS(root.right, sum);
    if (!root.left && !root.right) {
      return null;
    }
    return root;
  };
  return DFS(root, 0);
};
