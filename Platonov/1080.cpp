/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    TreeNode* sufficientSubset(TreeNode* root, int limit) {
        if (dfs(root, 0, limit) < limit) {
            root = nullptr;
        }
        return root;
    }

    int dfs(TreeNode* currentNode, int currentSum, int limit) {
        if (currentNode == nullptr) return -(1e5+10);
        if (currentNode->left == nullptr && currentNode->right == nullptr) {
            int sum = currentSum + currentNode->val; 
            if (sum < limit) {
                currentNode = nullptr;
            }
            return sum;
        }
        int leftSum = dfs(currentNode->left, currentSum + currentNode->val, limit);
        int rightSum = dfs(currentNode->right, currentSum + currentNode->val, limit);
        if (leftSum < limit) {
            currentNode->left = nullptr;
        }
        if (rightSum < limit) {
            currentNode->right = nullptr;
        }
        int maxValue = (leftSum > rightSum) ? leftSum : rightSum;
        if (maxValue < limit) {
            currentNode = nullptr;
        }
        return maxValue;
    }
};
