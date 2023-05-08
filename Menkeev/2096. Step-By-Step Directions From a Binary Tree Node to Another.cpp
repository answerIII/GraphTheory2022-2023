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
    bool find(TreeNode* node, int val, string& path) {
        if (node->val == val)
            return true;
        if (node->left && find(node->left, val, path))
            path.push_back('L');
        else if (node->right && find(node->right, val, path))
            path.push_back('R');
        return !path.empty();
    }

    string getDirections(TreeNode* root, int startValue, int destValue) {
        string src_p, dest_p;
        find(root, startValue, src_p);
        find(root, destValue, dest_p);
        while (!src_p.empty() && !dest_p.empty() && src_p.back() == dest_p.back()) {
            src_p.pop_back();
            dest_p.pop_back();
        }
        return string(src_p.size(), 'U') + string(rbegin(dest_p), rend(dest_p));
    }
};