class Solution {
public:
    int Depth(TreeNode *root) {
        if (!root){
            return 0;
        }
        return 1+max(Depth(root->left),Depth(root->right));
    }
    void dfs(TreeNode *root, vector<vector<string>> &res, int start, int end, int d){
        if (!root) return;
        int M = (start + end) / 2;
        res[d][M] = to_string(root->val);
        d++;
        dfs(root->left, res, start, M, d);
        dfs(root->right, res, M + 1, end, d);
    }
    vector<vector<string>> printTree(TreeNode* root) {
        int d = Depth(root);
        int n = pow(2,d) - 1;
        vector<vector<string>> res(d, vector<string>(n));
        dfs(root, res, 0, n, 0);
        return res;
    }
};