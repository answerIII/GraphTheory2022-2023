#include <tuple>

class Solution {
    int res = -1;
    int Start;
public:
    std::tuple<int, int> dfs(TreeNode *node) {
        if (!node) {
            return make_pair(-1, -1);
        }
        int l1, l2, r1, r2;
        std::tie(l1, l2) = dfs(node->left);
        std::tie(r1, r2) = dfs(node->right);
        int d=-1;
        if (node->val == Start) {
            res = max(l1, r1) + 1;
            d = 0;
        } else if (l2 >= 0) {
            res = max(res, r1 + l2 + 2);
            d = l2 + 1;
        } else if (r2 >= 0) {
            res = max(res, l1+r2 + 2);
            d = r2 + 1;
        }
        return std::make_tuple(max(l1, r1) + 1, d);  
    }

    int amountOfTime(TreeNode* root, int start) {
        Start = start;
        dfs(root);
        return res;
    }
};