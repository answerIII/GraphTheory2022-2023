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
    bool BFS(vector<TreeNode*> LevelNodes, int level)
    {
        if (LevelNodes.size() == 0)
            return true;
        else
        {
            if (LevelNodes.size() > 1)
            {
                for (int i = 0; i < LevelNodes.size() - 1; i++)
                {
                    if (level % 2 == 0)
                    {
                        if (LevelNodes[i]->val >= LevelNodes[i + 1]->val || LevelNodes[i]->val % 2 == 0)
                            return false;
                    }
                    else if (LevelNodes[i]->val <= LevelNodes[i + 1]->val || LevelNodes[i]->val % 2 == 1)
                        return false;
                }
            }

            if (LevelNodes[LevelNodes.size() - 1]->val % 2 == level % 2)
                return false;

            vector<TreeNode*> NewLevelNodes;

            for (int i = 0; i < LevelNodes.size(); i++)
            {
                if (LevelNodes[i]->left != nullptr)
                    NewLevelNodes.push_back(LevelNodes[i]->left);
                if (LevelNodes[i]->right != nullptr)
                    NewLevelNodes.push_back(LevelNodes[i]->right);
            }

            return BFS(NewLevelNodes, level + 1);
        }
    }

    bool isEvenOddTree(TreeNode* root) {
        vector<TreeNode*> LevelNode;
        LevelNode.push_back(root);
        return BFS(LevelNode, 0);                
    }
};