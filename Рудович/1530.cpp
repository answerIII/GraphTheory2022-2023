#include <vector>

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

using namespace std;

class Solution {
public:
    using Ans = pair<int, vector<int>>;
    static Ans countPairsT(TreeNode* root, int distance) {
        Ans ans({0, vector<int>(distance)});
        if (!root){
            return ans; 
        }
        if (!root->left && !root->right){
            ans.second.assign(distance, 1);
            ans.second[0] = 0; 
            return ans;
        }
        Ans lans = Solution::countPairsT(root->left, distance);
        Ans rans = Solution::countPairsT(root->right, distance);
        ans.first = lans.first + rans.first;
        for (int i = 1; i < distance; ++i){
            ans.second[i] = lans.second[i - 1] + rans.second[i - 1];
            ans.first += (lans.second[i] - lans.second[i - 1]) * rans.second[distance - i];
        }
        return ans;
    }

    static int countPairs(TreeNode* root, int distance) {
        return Solution::countPairsT(root, distance).first;
    }
};