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
private:
    int left_sum;
    int right_sum;

    int DFS(TreeNode* node, int x) {
        if (!node) 
            return 0;

        if (node->val == x) {
            left_sum = DFS(node->left, x);
            right_sum = DFS(node->right, x);
            return 0;
        }

        return DFS(node->left, x) + DFS(node->right, x) + 1;
    }

public:
    Solution(): left_sum(0), right_sum(0) {}

    bool btreeGameWinningMove(TreeNode* root, int n, int x) {
        if (n == 1) 
            return false;

        DFS(root, x);  
        int total = n - 1 - (left_sum + right_sum);  

        return (total > left_sum + right_sum || 
                left_sum > right_sum + total || 
                right_sum > left_sum + total);
    }
};
