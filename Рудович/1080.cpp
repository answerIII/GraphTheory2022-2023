struct TreeNode 
{
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution 
{
public:
    TreeNode* sufficientSubset(TreeNode* root, int limit) 
    {
        if (!fun(root, limit, 0))
        {
            return nullptr;
        }
        return root;
    }

    bool fun(TreeNode* root, int limit, long long sum)
    {
        if (!root) return false;
        
        if (!root->left && !root->right)
        {
            if (sum + root->val < limit) return false;
            return true;
        }

        if (!fun(root->left, limit, sum + root->val))
        {
            if (root->left) delete root->left;
            root->left = nullptr;
        }
        
        if (!fun(root->right, limit, sum + root->val))
        {
            if (root->right) delete root->right;
            root->right = nullptr;
        }

        if (!root->left && !root->right) return false;
        return true;
    }
};