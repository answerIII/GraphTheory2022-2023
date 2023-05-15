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
    string getDirections(TreeNode* root, int startValue, int destValue) {
        string pathToStart, pathToDest;
        DFS(root, startValue, pathToStart);
        DFS(root, destValue, pathToDest);

        while((pathToStart.size() || pathToDest.size()) && pathToStart.back() == pathToDest.back()){
            pathToStart.pop_back();
            pathToDest.pop_back();
        }

        string result = string(pathToStart.size(), 'U') + pathToDest;
        return result;   
    }


    bool DFS(TreeNode* root, int target, string path){
        if(root->val == target){
            return true;
        }
        if(root->left && DFS(root->left, target, path)) {
            path += 'L';
        }
        else if(root->right && DFS(root->right, target, path)){
            path += 'R';
        } 
        return path.size() > 0;        
    }
};