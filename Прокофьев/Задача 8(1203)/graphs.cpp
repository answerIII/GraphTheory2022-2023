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
	vector<int> sortItems(int n, int m, vector<int>& group, vector<vector<int>>& beforeItems)
	{
		GroupsDivision.resize(m);
		IsVisitedItem.resize(n);
		IsCanSortItem.resize(n);
		IsVisitGroup.resize(m);
		IsCanSortGroup.resize(m);
		Group = group;
		BeforeItems = beforeItems;
		for (int i = 0; i < n; i++)
		{
			if (group[i] != -1)
			{
				GroupsDivision[Group[i]].push_back(i);
			}
		}

		for (int i = 0; i < n; i++)
		{
			if (Group[i] != -1 && !SortGroup(Group[i]))
			{
				return {};
			}
			if (Group[i] == -1 && !PushNoGroupItem(i))
			{
				return {};
			}
		}

		return Result;

	}

private:
	vector<int> Group;
	vector<vector<int>> BeforeItems;

	vector<vector<int>> GroupsDivision;
	vector<bool> IsVisitedItem;
	vector<bool> IsCanSortItem;
	vector<bool> IsVisitGroup;
	vector<bool> IsCanSortGroup;

	vector<int> Result;

	bool PushNoGroupItem(int Item)
	{
		if (IsVisitedItem[Item])
		{
			return IsCanSortItem[Item];
		}

		IsVisitedItem[Item] = true;

		for (auto BeforeItem : BeforeItems[Item])
		{
			if (Group[BeforeItem] != -1 && !SortGroup(Group[BeforeItem]))
			{
				return false;
			}
			else if (Group[BeforeItem] == -1 && !PushNoGroupItem(BeforeItem))
			{
				return false;
			}
		}

		IsCanSortItem[Item] = true;

		Result.push_back(Item);
		return true;
	}

	bool CheckCanSortedGroupDFS(int Item, int GroupIndex)
	{
		if (IsVisitedItem[Item])
		{
			return IsCanSortItem[Item];
		}

		IsVisitedItem[Item] = true;

		for (auto BeforeItem : BeforeItems[Item])
		{
			if (Group[BeforeItem] != GroupIndex)
			{
				continue;
			}

			if (!CheckCanSortedGroupDFS(BeforeItem, GroupIndex))
			{
				return false;
			}
		}

		IsCanSortItem[Item] = true;

		Result.push_back(Item);

		return true;
	}

	bool SortGroup(int GroupIndex)
	{
		if (IsVisitGroup[GroupIndex])
		{
			return IsCanSortGroup[GroupIndex];
		}

		IsVisitGroup[GroupIndex] = true;

		for (auto Item : GroupsDivision[GroupIndex])
		{
			for (auto BeforeItem : BeforeItems[Item])
			{
				if (Group[BeforeItem] == -1 && !PushNoGroupItem(BeforeItem))
				{
					return false;
				}
				else if (Group[BeforeItem] != -1 && Group[BeforeItem] != GroupIndex && !SortGroup(Group[BeforeItem]))
				{
					return false;
				}
			}
		}

		for (auto Item : GroupsDivision[GroupIndex])
		{
			if (!CheckCanSortedGroupDFS(Item, GroupIndex))
			{
				return false;
			}
		}

		IsCanSortGroup[GroupIndex] = true;

		return true;
	}
};

int main()
{
	int n = 8, m = 2;
	vector<int> group = {-1, -1, 1, 0, 0, 1, 0, -1};
	vector<vector<int>> beforeItems = {{}, {6}, {5}, {6}, {3, 6}, {}, {}, {}};
	
	Solution sol;
	vector<int> res = sol.sortItems(n, m, group, beforeItems);;
	for (int i = 0; i < res.size(); i++)
	{
		cout << res[i] << " ";
	}
	
}