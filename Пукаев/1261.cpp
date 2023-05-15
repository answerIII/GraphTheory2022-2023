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
class FindElements {
public:
    TreeNode* node;
  
    FindElements(TreeNode* root) {
        this->node = root;
        stack<TreeNode*> stackNode;
        root->val = 0;
        stackNode.push(root);
        while(!stackNode.empty()){
            if(stackNode.top()->left && stackNode.top()->left->val == -1){
                stackNode.top()->left->val = 2*stackNode.top()->val + 1;
                cout <<  stackNode.top()->left->val << " ";
               
                stackNode.push(stackNode.top()->left);
                //cout << "top stack: " << stackNode.top()->val;
            }else if(stackNode.top()->right && stackNode.top()->right->val == -1){
                stackNode.top()->right->val = 2*stackNode.top()->val + 2;
                cout <<  stackNode.top()->right->val << " ";
                
                stackNode.push(stackNode.top()->right);
                //cout << "top stack: " << stackNode.top()->val;
                
            }else{
                stackNode.pop();
            }
            
        }
       
    }
    
    bool find(int target) {
        stack<TreeNode*> stackNode;
        stackNode.push(node);
        while(!stackNode.empty()){
            TreeNode* currentNode = stackNode.top();
            stackNode.pop();
            if(currentNode->val == target){
                return true;
            }
            if(currentNode->left){
                stackNode.push(currentNode->left);
            }
            
             if(currentNode->right){
                stackNode.push(currentNode->right);
            }
        }
        return false;
    }
};

/**
 * Your FindElements object will be instantiated and called as such:
 * FindElements* obj = new FindElements(root);
 * bool param_1 = obj->find(target);
 */