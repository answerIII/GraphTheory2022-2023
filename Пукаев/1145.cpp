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
    bool btreeGameWinningMove(TreeNode* root, int n, int x) {
        TreeNode* xNode = findNode(root, x);
        int rightXCount = countChild(xNode->right);
        int leftXCount = countChild(xNode->left);
        int anotherXCount = n - rightXCount - leftXCount - 1;
        if(rightXCount > n/2 || leftXCount > n/2 || anotherXCount > n/2) return true;
        else return false;

    }

    TreeNode* findNode(TreeNode* root, int x){
        if(!root) return nullptr;
        if(root->val == x) return root;
        
        TreeNode* left = findNode(root->left, x);
        TreeNode* right = findNode(root->right, x);

        if(left){
            return left;
        }
        else if(right){
            return right;
        }
        else{
            return nullptr;
        }

    }

    int countChild(TreeNode* node){
        if(!node) return 0;
        else return 1+countChild(node->left)+countChild(node->right);
    }

};