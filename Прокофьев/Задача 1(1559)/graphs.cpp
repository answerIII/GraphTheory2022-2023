#include <iostream>
#include <vector>

using namespace std;

enum CellState : short
{
	Undefined = 0,
	Current = 1,
	Blocked = 2
};

class Solution {
public:
	bool containsCycle(vector<vector<char>>& grid) 
	{
		RowsSize = grid.size();
		ColumnsSize = grid[0].size();
		vector<vector<CellState>> tmp(RowsSize,vector<CellState>(ColumnsSize));
		CellStates = tmp;
		
		for (int i = 0; i < CellStates.size(); i++)
		{
			for (int j = 0; j < CellStates[0].size(); j++)
			{
				CellStates[i][j] = CellState::Undefined;
			}
		}

		for (int i = 0; i < CellStates.size(); i++)
		{
			for (int j = 0; j < CellStates[0].size(); j++)
			{
				if (CellStates[i][j] == CellState::Blocked)
				{
					continue;
				}

				if (containsCycleDFS(grid, i, j))
				{
					return true;
				}
			}
		}

		return false;
	}
private:
	bool containsCycleDFS(vector<vector<char>>& grid, int Row, int Column, int PrevRow = -1, int PrevColumn = -1)
	{
		if (CellStates[Row][Column] == CellState::Current)
		{
			return true;
		}
		CellStates[Row][Column] = CellState::Current;

		//UP
		if (Row >= 1 && PrevRow != Row - 1)
		{
			if (grid[Row][Column] == grid[Row - 1][Column])
			{
				if (containsCycleDFS(grid, Row - 1, Column, Row, Column))
				{
					return true;
				}
			}
		}
		//Down
		if (Row < RowsSize - 1 && PrevRow != Row + 1)
		{
			if (grid[Row][Column] == grid[Row + 1][Column])
			{
				if (containsCycleDFS(grid, Row + 1, Column, Row, Column))
				{
					return true;
				}
			}
		}
		//Right
		if (Column < ColumnsSize - 1 && PrevColumn != Column + 1)
		{
			if (grid[Row][Column] == grid[Row][Column + 1])
			{
				if (containsCycleDFS(grid, Row, Column + 1, Row, Column))
				{
					return true;
				}
			}
		}
		//Left
		if (Column >= 1 && PrevColumn != Column - 1)
		{
			if (grid[Row][Column] == grid[Row][Column - 1])
			{
				if (containsCycleDFS(grid, Row, Column - 1, Row, Column))
				{
					return true;
				}
			}
		}

		CellStates[Row][Column] = CellState::Blocked;
		return false;
	}

	
	int RowsSize;
	int ColumnsSize;
	vector<vector<CellState>> CellStates;
};




