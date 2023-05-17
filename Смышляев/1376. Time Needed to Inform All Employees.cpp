class Solution {
    struct TreeNode {
        int t;
        TreeNode *parent;
        vector<TreeNode*> children;
        TreeNode() : t(0), parent(nullptr), children() {}
        TreeNode(int x) : t(x), parent(nullptr), children() {}
        TreeNode(int x, TreeNode *parent) : t(x), parent(parent), children() {}
      };
public:
    int findAns(TreeNode* root, long m) {
        if (root->children.empty()) {
            if(root->parent) {root->t = root->parent->t;}
            return root->t;
        }
        if (root->parent) {root->t += root->parent->t;}
        int tmp;
        for (int i = 0; i < root->children.size(); ++i) {
            tmp = findAns(root->children[i], m);
            if (tmp > m) { m = tmp;}
        }
        return m;
    }
    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        vector<TreeNode*> company(n, nullptr);
        TreeNode* head = nullptr;
        for (int i = 0; i < n; ++i) {
            company[i] = new TreeNode(informTime[i]);
        }
        for (int i = 0; i < n; ++i) {
            if (manager[i] == -1) {
                head = company[i];
                continue;
            }
            company[i]->parent = company[manager[i]];
            company[i]->parent->children.push_back(company[i]);
        }


        return findAns(head, head->t);
    }
};
