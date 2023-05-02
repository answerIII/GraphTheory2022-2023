#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <unordered_set>
#include <queue>

using namespace std;


struct TreeNode 
{
	int val;
	TreeNode *left;
	TreeNode *right;
	TreeNode() : val(0), left(nullptr), right(nullptr) {}
	TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
	TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};
 
class Solution
{
public:
	bool isEvenOddTree(TreeNode* root)
	{
		vector<TreeNode*> StartVec;
		StartVec.push_back(root);
		if (root->val % 2 == 0)
		{
			return false;
		}
		return BFS(StartVec);
	}

private:
	int layer = 0;


	bool BFS(vector<TreeNode*>& CurrentTreeNodes)
	{
		if (CurrentTreeNodes.empty())
		{
			return true;
		}

		vector<TreeNode*> newVec;
		for (auto CurrentTreeNode : CurrentTreeNodes)
		{
			if (CurrentTreeNode->left != nullptr)
			{
				newVec.push_back(CurrentTreeNode->left);
				if ((layer + 1) % 2 == 0 && (CurrentTreeNode->left->val % 2 == 0 || (newVec.size() > 1 && newVec[newVec.size() - 1]->val <= newVec[newVec.size() - 2]->val)))
				{
					cout << "1 if";
					return false;
				}
				else if ((layer + 1) % 2 == 1 && (CurrentTreeNode->left->val % 2 == 1 || (newVec.size() > 1 && newVec[newVec.size() - 1]->val >= newVec[newVec.size() - 2]->val)))
				{
					cout << "2 if";
					return false;
				}
			}
			if (CurrentTreeNode->right != nullptr)
			{
				newVec.push_back(CurrentTreeNode->right);
				if ((layer + 1) % 2 == 0 && (CurrentTreeNode->right->val % 2 == 0 || (newVec.size() > 1 && newVec[newVec.size() - 1]->val <= newVec[newVec.size() - 2]->val)))
				{
					cout << "3 if";
					return false;
				}
				else if ((layer + 1) % 2 == 1 && (CurrentTreeNode->right->val % 2 == 1 || (newVec.size() > 1 && newVec[newVec.size() - 1]->val >= newVec[newVec.size() - 2]->val)))
				{
					return false;
				}
			}
		}

		layer++;

		if (!BFS(newVec))
		{
			return false;
		}

		return true;
	}

};

int main()
{
	TreeNode Root(1);
	Solution sol;

	TreeNode Root2(2);
	TreeNode Root3(3);
	TreeNode Root3ver2(3);
	TreeNode Root4(4);
	TreeNode Root5(5);
	TreeNode Root6(6);
	TreeNode Root7(7);
	TreeNode Root8(8);
	TreeNode Root9(9);
	TreeNode Root10(10);
	TreeNode Root12(12);
	TreeNode Root18(18);
	TreeNode Root16(16);

	Root2.left = &Root12;
	Root2.right = &Root8;
	Root12.left = &Root5;
	Root12.right = &Root9;
	Root5.left = &Root18;
	Root5.right = &Root16;
	



	cout << sol.isEvenOddTree(&Root);
}

