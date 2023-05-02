#include <iostream>
#include <vector>

using namespace std;

enum State : char
{
	None = 0,
	One = 1,
	Many = 2
};

class Solution {
public:
	int countServers(vector<vector<int>>& grid) 
	{
		RowsSize = grid.size();
		ColumnsSize = grid[0].size();

		vector<State> tmp(RowsSize, State::None);
		RowStates = tmp;

		vector<State> tmp2(ColumnsSize, State::None);
		ColumnStates = tmp2;


		for (int i = 0; i < RowsSize; i++)
		{
			for (int j = 0; j < ColumnsSize; j++)
			{
				if (grid[i][j] == 1)
				{
					if (RowStates[i] == State::None)
					{
						RowStates[i] = State::One;
					}
					else if (RowStates[i] == State::One)
					{
						RowStates[i] = State::Many;
					}

					if (ColumnStates[j] == State::None)
					{
						ColumnStates[j] = State::One;
					}
					else if (ColumnStates[j] == State::One)
					{
						ColumnStates[j] = State::Many;
					}
				}
			}
		}

		int GoodServers = 0;
		for (int i = 0; i < RowsSize; i++)
		{
			for (int j = 0; j < ColumnsSize; j++)
			{
				if (grid[i][j] == 1 && (RowStates[i] == State::Many || ColumnStates[j] == State::Many))
				{
					GoodServers += 1;
				}
			}
		}

		return GoodServers;
	}
private:

	int RowsSize;
	int ColumnsSize;
	vector<State> RowStates;
	vector<State> ColumnStates;
};


int main()
{
	Solution sol;

	vector<vector<int>> ex{{1,0}, {1,1}};

	cout << sol.countServers(ex);
}

