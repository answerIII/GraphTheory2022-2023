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
    bool isEvenOddTree(TreeNode* root) {
        std::queue<TreeNode*> v;
        v.push(root);
        int currVal = -INT_MAX;
        unsigned level = 0;
        while (v.size())
        {
            std::queue<TreeNode*> newV;
            bool OddLevel = level % 2;  
            for (TreeNode* x = v.front(); v.size(); x = v.front())
            {
                if(OddLevel)
                {
                    if(x->val % 2 == 0 && x->val < currVal)
                    {
                        currVal = x->val;
                    }
                    else
                    {
                        return false;
                    }
                }
                else
                {
                    if(x->val % 2 == 1 && x->val > currVal)
                    {
                        currVal = x->val;
                    }
                    else
                    {
                        return false;
                    }
                }

                if (x->left)
                {
                    newV.push(x->left);
                }
                if (x->right)
                {
                    newV.push(x->right);
                }
                v.pop();
            }
            v = newV;
            currVal = INT_MAX * (OddLevel ? -1: 1); 
            level++;
        }
        return true;
    }
};
