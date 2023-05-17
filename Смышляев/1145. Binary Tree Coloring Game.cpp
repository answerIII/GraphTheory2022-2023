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
    TreeNode* findChsn(TreeNode* root, int x) {
        if (!root) {return root;}
        if (root->val == x) {return root;}
        TreeNode* ans = findChsn(root->left, x);
        if (ans) {return ans;}
        ans = findChsn(root->right, x);
        return ans;
    }
    int countSubtree(TreeNode* root) {
        if (!root) {return 0;}
        int counter = 1;
        counter += countSubtree(root->left) + countSubtree(root->right);
        return counter;
    }
    bool btreeGameWinningMove(TreeNode* root, int n, int x) {
        TreeNode* first = findChsn(root, x);
        if (!first->left && !first->right) {return true;}
        if (first == root) {
            if (abs(countSubtree(root->left) - countSubtree(root->right)) > 1) {return true;}
        }
        int left = countSubtree(first->left);
        int right = countSubtree(first->right);
        int top = countSubtree(root) - left - right - 1;
        if (left > n/2 || right > n/2 || top > n/2) {return true;}
        return false;
    }
};
