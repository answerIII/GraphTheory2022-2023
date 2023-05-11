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
    TreeNode* sol(TreeNode* root, int limit, int sum)
    {
        if (!root)
        {
            return root;
        }
        // если root это лист, то смотрим сумму:
        //1) если меньше чем limit, вернём null
        //2) иначе вернём root
        if (!root->left && !root->right)
        {
            if (sum + root->val < limit)
            {
                return NULL;
            }
            else
            {
                return root;
            }
        }

        //вызываем для левого и правого с текущей суммой
        TreeNode* l = sol(root->left, limit, sum + root->val);
        TreeNode* r = sol(root->right, limit, sum + root->val);

        //если слева/справа null, то обнуляем левое/правое значение root 
        //если оба null, то вернём null 
        if (l == NULL)
        {
            root->left = NULL;
        }

        if (r == NULL)
        {
            root->right = NULL;
        }

        if (r == NULL && l == NULL)
        {
            return NULL;
        }

        return root;
    }

    TreeNode* sufficientSubset(TreeNode* root, int limit)
    {
        return sol(root, limit, 0);
    }

};