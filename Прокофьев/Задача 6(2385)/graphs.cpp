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
	int amountOfTime(TreeNode* root, int start)
	{
		InfectionValues.resize(100001);

		TreeNode* StartTreeNode = GetTreeNodeByValue(root, start);
		vector<TreeNode*> StartSet;
		StartSet.push_back(StartTreeNode);
		BFS(StartSet);
		return layer - 1;
	}

private:
	vector<bool> InfectionValues;
	queue<TreeNode*> StartPath;
	int layer = 0;
	TreeNode* GetTreeNodeByValue(TreeNode* CurrentNode, int value)
	{
		if (CurrentNode == nullptr)
		{
			return nullptr;
		}

		if (CurrentNode->val == value)
		{
			return CurrentNode;
		}

		TreeNode* TreeNodeLeft = GetTreeNodeByValue(CurrentNode->left, value);
		if (TreeNodeLeft != nullptr)
		{
			StartPath.push(CurrentNode);
			return TreeNodeLeft;
		}

		TreeNode* TreeNodeRight = GetTreeNodeByValue(CurrentNode->right, value);
		if (TreeNodeRight != nullptr)
		{
			StartPath.push(CurrentNode);
			return TreeNodeRight;
		}

		return nullptr;
	}

	void BFS(vector<TreeNode*>& CurrentTreeNodes)
	{
		if (CurrentTreeNodes.empty())
		{
			return;
		}

		vector<TreeNode*> newVec;
		for (auto CurrentTreeNode : CurrentTreeNodes)
		{
			if (!InfectionValues[CurrentTreeNode->val])
			{
				InfectionValues[CurrentTreeNode->val] = true;
			}
			if (CurrentTreeNode->left != nullptr && !InfectionValues[CurrentTreeNode->left->val])
			{
				newVec.push_back(CurrentTreeNode->left);
				InfectionValues[CurrentTreeNode->left->val] = true;
			}
			if (CurrentTreeNode->right != nullptr && !InfectionValues[CurrentTreeNode->right->val])
			{
				newVec.push_back(CurrentTreeNode->right);
				InfectionValues[CurrentTreeNode->right->val] = true;
			}

			if (CurrentTreeNodes.empty())
			{
				break;
			}
		}

		if (!StartPath.empty())
		{
			TreeNode* Parent = StartPath.front();
			StartPath.pop();
			newVec.push_back(Parent);
			InfectionValues[Parent->val] = true;
		}

		layer++;

		BFS(newVec);
	}

};

int main()
{
	TreeNode Root(1);
	Solution sol;

	TreeNode Root2(2);
	TreeNode Root3(3);
	TreeNode Root4(4);
	TreeNode Root5(5);
	TreeNode Root6(6);
	TreeNode Root7(7);
	TreeNode Root8(8);
	TreeNode Root9(9);
	TreeNode Root10(10);

	/*Root.left = &Root5;
	Root5.right = &Root4;
	Root4.left = &Root9;
	Root4.right = &Root2;
	Root.right = &Root3;
	Root3.left = &Root10;
	Root3.right = &Root6;*/

	/*Root.left = &Root2;
	Root2.left = &Root3;
	Root3.left = &Root4;
	Root4.left = &Root5;*/

	/*Root2.left = &Root5;*/

	Root5.right = &Root3;
	Root5.left = &Root2;
	Root2.left = &Root4;
	Root4.left = &Root;


	cout << sol.amountOfTime(&Root5, 4);
}

