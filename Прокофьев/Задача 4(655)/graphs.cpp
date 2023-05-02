#include <iostream>
#include <vector>
#include <string>

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
	vector<vector<string>> printTree(TreeNode* root) 
	{
		Height = GetHeight(root);

		int n = pow(2, Height + 1) - 1;
		vector<vector<string>> tmp(Height + 1, vector<string>(n, ""));
		Result = tmp;

		Print(root, 0, (n - 1) / 2);
		return Result;
	}

private:
	vector<vector<string>> Result;
	int Height;

	int GetHeight(TreeNode* Node)
	{
		if (Node == nullptr)
		{
			return 0;
		}

		return max(GetHeight(Node->left), GetHeight(Node->right)) + 1;
	}
	
	void Print(TreeNode* Node, int r, int c)
	{
		if (Node == nullptr)
		{
			return;
		}

		Result[r][c] = to_string(Node->val);

		int Delta = pow(2, Height - r - 1);
		Print(Node->left, r + 1, c - Delta);
		Print(Node->right, r + 1, c + Delta);
	}
};


int main()
{
	
}

