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

    bool BFS(TreeNode* node, string& curr_path, int x) { 
        if (node->val == x) 
            return true;
        else if (node->left && BFS(node->left, curr_path, x))  
            curr_path += 'L';
        else if (node->right && BFS(node->right, curr_path, x))   
            curr_path += 'R';
        return !curr_path.empty();
    }

public:
    string getDirections(TreeNode* root, int startValue, int destValue) {
        string shortest_path;
        string start_path = "", dest_path = "";
        BFS(root, start_path, startValue);
        BFS(root, dest_path, destValue);

        while (start_path != "" && dest_path != "" && start_path.back() == dest_path.back()) {
            start_path.pop_back();
            dest_path.pop_back();
        }
        shortest_path = string(start_path.size(), 'U');
        while (dest_path.size() > 0) {
            shortest_path += dest_path.back();
            dest_path.pop_back();
        }
        return shortest_path;
    }
};
