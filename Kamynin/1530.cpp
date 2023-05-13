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
int res = 0;
int d;

vector<int> dfs(TreeNode* node){
    if (!node->left && !node->right)
        return {0};
    vector<int> left;
    vector<int> right;
    if (node->left){
        left = dfs(node->left);
        for(int i = 0; i < left.size(); ++i)
            ++left[i];
    }
    if (node->right){
        right = dfs(node->right);
        for(int i = 0; i < right.size(); ++i)
            ++right[i];
    }
    for(auto l: left)
        for(auto r: right)
            if (l + r <= d)
                ++res;
    vector<int> v(left);
    v.insert(v.end(), right.begin(), right.end());
    return v;
}

int countPairs(TreeNode* root, int distance){
    res = 0;
    d = distance;
    dfs(root);
    return res;
}
};
