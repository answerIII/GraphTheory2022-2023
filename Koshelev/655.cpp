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
    int getHeight(TreeNode *root)
    {
	    if (!root)
		    return 0;
	    return max(getHeight(root->left), getHeight(root->right)) + 1;
    }

    void DFS(TreeNode* root, vector<vector<string>> &res, int r, int c, int height)
    {
        if (!root)
            return;
        res[r][c] = to_string(root->val);
        DFS(root->left, res, r + 1, c - pow(2, height - r - 1), height);
        DFS(root->right, res, r + 1, c + pow(2, height - r - 1), height);
    }
    vector<vector<string>> printTree(TreeNode* root) {
        int height = getHeight(root) - 1;
        int m = height + 1;
        int n = pow(2, height + 1) - 1;
        vector<vector<string>> res(m, vector<string>(n, ""));
        DFS(root, res, 0, (n - 1) / 2, height);
        return res;
    }
};