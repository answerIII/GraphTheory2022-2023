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
    TreeNode* helper(TreeNode* root, int limit, int sumTillNow)
    {
        if (root == NULL)  return NULL;

        if (root->left == NULL && root->right == NULL)
            return root->val + sumTillNow < limit ? NULL : root;

        root->left = helper(root->left, limit, sumTillNow + root->val);
        root->right = helper(root->right, limit, sumTillNow + root->val);

        return root->left == NULL && root->right == NULL ? NULL : root;
    }


    TreeNode* sufficientSubset(TreeNode* root, int _limit) {
        return helper(root, _limit, 0);
    }
};

