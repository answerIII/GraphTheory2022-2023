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

    vector<pair<int, int>> BFS(TreeNode* root) {
        std::queue<pair<TreeNode*, int>> temp_queue;
        std::vector<pair<int, int>> traverse_v;

        temp_queue.push(make_pair(root, 0));

        while (!temp_queue.empty()) {

            TreeNode* node = temp_queue.front().first;
            int level = temp_queue.front().second;

            traverse_v.push_back(make_pair(node->val, level));

            temp_queue.pop();


            if (node->left != NULL) {
                int next_level = level + 1;
                temp_queue.push(make_pair(node->left, next_level));
            }

            if (node->right != NULL) {
                int next_level = level + 1;
                temp_queue.push(make_pair(node->right, next_level));
            }

        }


        for (int i = 0; i < traverse_v.size(); i++)
        {
            std::cout << traverse_v[i].first << ":" << traverse_v[i].second << " ";
        }
        std::cout << std::endl;

        return traverse_v;

    }



    bool isEvenOddTree(TreeNode* root) {
        vector<pair<int, int>> traverse_v;
        traverse_v = BFS(root);


        // case on level 0:
        int i = 0, level = 0;
        if (traverse_v[i].first % 2 == 0)
            return false;

        level++; i++;
        while (i < traverse_v.size()) {

            //odd level
            if (level % 2 == 1) {
                int prev_node = -1;
                while (i < traverse_v.size() && traverse_v[i].second == level) {

                    if (traverse_v[i].first % 2 == 1)
                        return false;

                    if (prev_node != -1 && prev_node <= traverse_v[i].first)
                        return false;

                    prev_node = traverse_v[i].first;
                    i++;
                }
            }

            //even level   
            else {

                int prev_node = -1;
                while (i < traverse_v.size() && traverse_v[i].second == level) {

                    if (traverse_v[i].first % 2 == 0)
                        return false;

                    if (prev_node != -1 && prev_node >= traverse_v[i].first)
                        return false;

                    prev_node = traverse_v[i].first;
                    i++;
                }
            }

            level++;
        }

        return true;
    }
};