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

    void inorder(vector<int>& vec, TreeNode* root)
    {
        if (root == NULL)
        {
            return;
        }
        inorder(vec, root->left);
        vec.push_back(root->val);
        inorder(vec, root->right);
    }

    vector<vector<int>> closestNodes(TreeNode* root, vector<int>& queries)
    {

        vector<vector<int>> answer;
        vector<int> vec;
        inorder(vec, root);
        int n = vec.size();
        int mini, maxi;

        for (int q : queries)
        {
            mini = maxi = -1;
            //если элемент нашёлся, тогда он и мин, и макс
            if (binary_search(vec.begin(), vec.end(), q))
            {
                maxi = mini = q;
            }
            else
            {
                if (q >= vec[0])
                {
                    mini = lower_bound(vec.begin(), vec.end(), q) - vec.begin();
                    --mini;
                    if (mini >= 0)
                    {
                        mini = vec[mini];
                    }
                }
                if (q < vec[n - 1])
                {
                    maxi = upper_bound(vec.begin(), vec.end(), q) - vec.begin();
                    maxi = vec[maxi];
                }
            }

            answer.push_back({ mini,maxi });
        }

        return answer;
    }
};