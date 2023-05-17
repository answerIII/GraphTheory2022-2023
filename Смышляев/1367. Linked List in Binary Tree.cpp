/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
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
    bool isSubPath(ListNode* head, TreeNode* root, stack<ListNode*> toCheck = {}) {
        if (!head) {return true;}
        else {toCheck.push(head);}
        if (!root) {return false;}
        ListNode* cur = nullptr;
        stack<ListNode*> nextToCheck;
        while(!toCheck.empty()) {
            cur = toCheck.top();
            if (cur->val == root->val) {
                if (!cur->next) {return true;}
                nextToCheck.push(cur->next);
            }
            toCheck.pop();
        }
        return (isSubPath(head, root->left, nextToCheck) || isSubPath(head, root->right, nextToCheck));
    }
};
