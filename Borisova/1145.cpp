class Solution {
    int l = 0;
    int r = 0;
public:
    int DFS(TreeNode *root, int x){
        if (!root){return 0;}
        int L = DFS(root->left, x);
        int R = DFS(root->right, x);
        if (root->val == x){
            l = L;
            r = R;
            }
        return 1 + L + R;
    }
    bool btreeGameWinningMove(TreeNode* root, int n, int x) {
        int dfs = DFS(root, x);
        int res = max({l, r, dfs - 1 - l - r});
        return res > dfs - res;
    }
};