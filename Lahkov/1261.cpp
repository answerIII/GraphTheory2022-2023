#include <queue>
#include <iostream>
using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* left, TreeNode* right) : val(x), left(left), right(right) {}
};

class FindElements {
private:
    vector<int> rec;
public:
    FindElements(TreeNode* root) {
        queue<pair<TreeNode*, int>> q;
        q.push({ root,0 });
        while (q.size() != 0) {
            pair<TreeNode*, int> tmp = q.front();
            q.pop();
            rec.push_back(tmp.second);
            if (tmp.first->left != nullptr) q.push({ tmp.first->left,tmp.second * 2 + 1 });
            if (tmp.first->right != nullptr) q.push({ tmp.first->right,tmp.second * 2 + 2 });
        }
    }

    bool find(int target) {
        return std::find(rec.begin(), rec.end(), target) != rec.end();
    }

};