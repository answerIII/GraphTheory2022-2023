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

struct SubtreeData {
    int sum;
    int maxSum;
    int leftMinValue;
    int leftMaxValue;
    int rightMinValue;
    int rightMaxValue;
    SubtreeData() : sum(0), maxSum(0), leftMinValue(0), leftMaxValue(0), rightMinValue(0), rightMaxValue(0) {}
    SubtreeData(int sum, int maxSum, int leftMinValue, int leftMaxValue, int rightMinValue, int rightMaxValue) : sum(sum), maxSum(maxSum), leftMinValue(leftMinValue), leftMaxValue(leftMaxValue), rightMinValue(rightMinValue), rightMaxValue(rightMaxValue) {}
};

class Solution {
public:
    int maxSumBST(TreeNode* root) {
        return max(0, dfs(root)->maxSum);
    }

    SubtreeData* dfs(TreeNode* currentNode) {
        SubtreeData* subtreeData = new SubtreeData();
        if (currentNode == nullptr) {
            subtreeData->sum = -1e9;
            subtreeData->maxSum = -1e9;
            subtreeData->leftMinValue = 1e9;
            subtreeData->leftMaxValue = -1e9;
            subtreeData->rightMinValue = 1e9;
            subtreeData->rightMaxValue = -1e9;
        }
        else if (currentNode->left && currentNode->right) {
            SubtreeData* leftData = dfs(currentNode->left);
            SubtreeData* rightData = dfs(currentNode->right);
            if (leftData->sum > -1e9 && rightData->sum > -1e9 && leftData->rightMaxValue < currentNode->val && currentNode->val < rightData->leftMinValue) {
                int sum = leftData->sum + rightData->sum + currentNode->val;
                subtreeData->sum = sum; 
                subtreeData->maxSum = max({sum, leftData->maxSum, rightData->maxSum}); 
                subtreeData->leftMinValue = leftData->leftMinValue; 
                subtreeData->leftMaxValue = leftData->rightMaxValue; 
                subtreeData->rightMinValue = rightData->leftMinValue; 
                subtreeData->rightMaxValue = rightData->rightMaxValue;
            } else {
                subtreeData->sum = -1e9;
                subtreeData->maxSum = max(leftData->maxSum, rightData->maxSum);
                subtreeData->leftMinValue = 1e9;
                subtreeData->leftMaxValue = -1e9;
                subtreeData->rightMinValue = 1e9;
                subtreeData->rightMaxValue = -1e9;
            }
        } else if (currentNode->left) {
            SubtreeData* leftData = dfs(currentNode->left);
            if (leftData->sum > -1e9 && leftData->rightMaxValue < currentNode->val) {
                int sum = leftData->sum + currentNode->val;
                subtreeData->sum = sum;
                subtreeData->maxSum = max(leftData->maxSum, sum);
                subtreeData->leftMinValue = leftData->leftMinValue;
                subtreeData->leftMaxValue = leftData->rightMaxValue;
                subtreeData->rightMinValue = currentNode->val;
                subtreeData->rightMaxValue = currentNode->val;
            } else {
                subtreeData->sum = -1e9;
                subtreeData->maxSum = leftData->maxSum;
                subtreeData->leftMinValue = 1e9;
                subtreeData->leftMaxValue = -1e9;
                subtreeData->rightMinValue = 1e9;
                subtreeData->rightMaxValue = -1e9;
            }
        } else if (currentNode ->right) {
            SubtreeData* rightData = dfs(currentNode->right);
            if (rightData->sum > -1e9 && currentNode->val < rightData->leftMinValue) {
                int sum = rightData->sum + currentNode->val;
                subtreeData->sum = sum;
                subtreeData->maxSum = max(rightData->maxSum, sum);
                subtreeData->leftMinValue = currentNode->val;
                subtreeData->leftMaxValue = currentNode->val;
                subtreeData->rightMinValue = rightData->leftMinValue;
                subtreeData->rightMaxValue = rightData->rightMaxValue;
            } else {
                subtreeData->sum = -1e9;
                subtreeData->maxSum = rightData->maxSum;
                subtreeData->leftMinValue = 1e9;
                subtreeData->leftMaxValue = -1e9;
                subtreeData->rightMinValue = 1e9;
                subtreeData->rightMaxValue = -1e9;
            }
        } else {
            subtreeData->sum = currentNode->val;
            subtreeData->maxSum = currentNode->val;
            subtreeData->leftMinValue = currentNode->val;
            subtreeData->leftMaxValue = currentNode->val;
            subtreeData->rightMinValue = currentNode->val;
            subtreeData->rightMaxValue = currentNode->val;
        }
        return subtreeData;
    }
};