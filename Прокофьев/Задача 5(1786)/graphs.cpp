#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <set>

using namespace std;

class Solution
{
public:
	int countRestrictedPaths(int n, vector<vector<int>>& edges)
	{
		vector<vector<pair<int, int>>> EdgesList(n);

		for (auto Edge : edges)
		{
			EdgesList[Edge[0] - 1].push_back(pair<int, int>(Edge[1] - 1, Edge[2]));
			EdgesList[Edge[1] - 1].push_back(pair<int, int>(Edge[0] - 1, Edge[2]));
		}

		vector<int> Tmp(n, INT_MAX);
		PathToLast = Tmp;

		Dijkstra(n, EdgesList);

		vector<int> CountPaths(n, -1);
		CountPaths[0] = 1;

		return GetCountRestrictedPaths(n - 1, EdgesList, 0, CountPaths);
	}
private:
	int Mod = 1e9 + 7;
	long long Sum = 0;
	vector<int> PathToLast;
	void Dijkstra(int n, vector<vector<pair<int, int>>>& EdgesList)
	{
		PathToLast[n - 1] = 0;
		set<pair<int, int>> EdgesSet;
		EdgesSet.insert(pair<int, int>(0, n - 1));

		while (!EdgesSet.empty())
		{
			auto FirstEdge = *(EdgesSet.begin());
			EdgesSet.erase(EdgesSet.begin());

			for (auto Edge : EdgesList[FirstEdge.second])
			{
				if (PathToLast[Edge.first] > PathToLast[FirstEdge.second] + Edge.second)
				{
					auto BadEdge = EdgesSet.find(pair<int, int>(PathToLast[Edge.first], Edge.first));

					if (BadEdge != EdgesSet.end())
					{
						EdgesSet.erase(BadEdge);
					}

					PathToLast[Edge.first] = PathToLast[FirstEdge.second] + Edge.second;
					EdgesSet.insert(make_pair(PathToLast[Edge.first], Edge.first));
				}
			}
		}
	}


	int GetCountRestrictedPaths(int index, vector<vector<pair<int, int>>>& EdgesList, int Distance, vector<int>& CountPaths)
	{
		if (index == 0)
		{
			return 1;
		}

		if (CountPaths[index] != -1)
		{
			return CountPaths[index];
		}

		unsigned long long Sum = 0;

		for (auto Edge : EdgesList[index])
		{
			if (Distance < PathToLast[Edge.first])
			{
				Sum = (Sum % Mod + GetCountRestrictedPaths(Edge.first, EdgesList, PathToLast[Edge.first], CountPaths) % Mod) % Mod;
			}
		}
		CountPaths[index] = Sum;
		return  CountPaths[index];
	}
};
 

int main()
{
	int n = 9;
	int m = 5;
	const int k = 10;
	vector<vector<int>> edges2 {{1, 2, 3}, {1, 3, 3}, {2, 3, 1}, {1, 4, 2}, {5, 2, 2}, {3, 5, 1}, {5, 4, 10}};
	vector<vector<int>> edges {{6, 2, 35129}, {3, 4, 99499}, {2, 7, 43547}, {8, 1, 78671}, {2, 1, 66308}, {9, 6, 33462}, {5, 1, 48249}, {2, 3, 44414}, {6, 7, 44602}, {1, 7, 14931}, {8, 9, 38171}, {4, 5, 30827}, {3, 9, 79166}, {4, 8, 93731}, {5, 9, 64068}, {7, 5, 17741}, {6, 3, 76017}, {9, 4, 72244}};
	vector<vector<int>> edges3 {{9, 10, 8}, {9, 6, 5}, {1, 5, 9}, {6, 8, 10}, {1, 8, 1}, {8, 10, 7}, {10, 7, 9}, {5, 7, 3}, {4, 2, 9}, {2, 3, 9}, {3, 10, 4}, {1, 4, 7}, {7, 6, 1}, {3, 9, 8}, {9, 1, 6}, {4, 7, 10}, {9, 4, 9}};

	Solution sol;

	cout << sol.countRestrictedPaths(m, edges2);
}

