#include <tuple>
class Solution {
    int res = 0;
public:
    std::tuple<int, bool, int, int> DFS(TreeNode *root){
        if (!root){
            return std::make_tuple(0, true, 40000, -40000);
        }
        int L, R, minL, minR, maxL, maxR;
        bool L_, R_;
        std::tie(L, L_, minL, maxL)= DFS(root->left);
        std::tie(R, R_, minR, maxR)= DFS(root->right);
        if (L_ && R_ && (maxL<root->val) && (root->val<minR)){
            int r = root->val + L + R;
            res = max(res, r);
            return std::make_tuple(r, true, min(minL, root->val), max(maxR, root->val));
            }
        return std::make_tuple(0, false, 40000, -40000);
    };
    int maxSumBST(TreeNode* root) {
        DFS(root);
        return(res);
    };
};