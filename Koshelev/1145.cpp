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
    int CountNodeLeft, CountNodeRight;
    int DFS(TreeNode* node, int x)
    {
        if (!node)
            return 0;
        int left = DFS(node->left, x);
        int right = DFS(node->right, x);
        if (node->val == x)
        {
            CountNodeLeft = left;
            CountNodeRight = right;
        }    
        return left + right + 1;        
    }
    bool btreeGameWinningMove(TreeNode* root, int n, int x) {
        DFS(root, x);
        return max(n - (CountNodeLeft + CountNodeRight + 1), max(CountNodeLeft, CountNodeRight)) > (n/2);
    }
};