#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <algorithm>
#include <unordered_set>
#include <queue>

using namespace std;

class Solution
{
public:
	int maximumMinutes(vector<vector<int>>& grid)
	{
		n = grid.size();
		m = grid[0].size();

		Grid = grid;

		vector<vector<int>> TMP(n, vector<int>(m, -1));
		FireTime = TMP;

		vector<pair<int, int>> StartFire;
		for (int i = 0; i < n; i++)
		{
			for (int j = 0; j < m; j++)
			{
				if (Grid[i][j] == 1)
				{
					FireTime[i][j] = 0;
					StartFire.push_back(pair<int, int>(i, j));
				}
			}
		}
		FireBFS(StartFire);

		int Left = 0;
		int Right = 1000000000;
		int Midle = 0;

		vector<pair<int, int>> StartPerson;
		StartPerson.push_back(pair<int, int>(0, 0));

		vector<vector<bool>> TMP3(n, vector<bool>(m, false));
		IsVisited = TMP3;
		bool Can = false;
		int Res = 0;
		while (Left <= Right)
		{
			Midle = Left + (Right - Left) / 2;
			PersonLayer = Midle;
			vector<vector<bool>> TMP3(n, vector<bool>(m, false));
			IsVisited = TMP3;

			bool Result = PersonBFS(StartPerson);
			if (Result)
			{
				Can = true;
				Res = Midle;
				Left = Midle + 1;
			}
			else
			{
				Right = Midle - 1;
				if (Right == -1)
				{
					Midle = 0;
					PersonLayer = Midle;
					vector<vector<bool>> TMP3(n, vector<bool>(m, false));
					IsVisited = TMP3;

					bool Result = PersonBFS(StartPerson);
					if (Result)
					{
						Res = Midle;
						Can = true;
					}

				}
			}
		}
		if (!Can)
		{
			return -1;
		}
		return Res;

	}
private:
	int n = 0, m = 0;
	vector<vector<int>> Grid;
	vector<vector<int>> FireTime;
	vector<vector<bool>> IsVisited;

	int FireLayer;
	int PersonLayer;

	bool PersonBFS(vector<pair<int, int>> CurrentPerson)
	{
		if (CurrentPerson.empty())
		{
			return false;
		}
		vector<pair<int, int>> NewCurrentPerson;
		for (auto CurrentPersonCell : CurrentPerson)
		{
			if ((CurrentPersonCell.first + 1 == n - 1 && CurrentPersonCell.second == m - 1 && (PersonLayer < FireTime[n - 1][m - 1] || FireTime[n - 1][m - 1] == -1))
				|| (CurrentPersonCell.first == n - 1 && CurrentPersonCell.second + 1 == m - 1 && (PersonLayer < FireTime[n - 1][m - 1] || FireTime[n - 1][m - 1] == -1)))
			{
				return true;
			}

			if (CurrentPersonCell.first < n - 1 && IsVisited[CurrentPersonCell.first + 1][CurrentPersonCell.second] == false && Grid[CurrentPersonCell.first + 1][CurrentPersonCell.second] == 0 && (PersonLayer + 1 < FireTime[CurrentPersonCell.first + 1][CurrentPersonCell.second] || FireTime[CurrentPersonCell.first + 1][CurrentPersonCell.second] == -1))
			{
				IsVisited[CurrentPersonCell.first + 1][CurrentPersonCell.second] = true;
				NewCurrentPerson.push_back(pair<int, int>(CurrentPersonCell.first + 1, CurrentPersonCell.second));
			}
			if (CurrentPersonCell.second < m - 1 && IsVisited[CurrentPersonCell.first][CurrentPersonCell.second + 1] == false && Grid[CurrentPersonCell.first][CurrentPersonCell.second + 1] == 0 && (PersonLayer + 1 < FireTime[CurrentPersonCell.first][CurrentPersonCell.second + 1] || FireTime[CurrentPersonCell.first][CurrentPersonCell.second + 1] == -1))
			{
				IsVisited[CurrentPersonCell.first][CurrentPersonCell.second + 1] = true;
				NewCurrentPerson.push_back(pair<int, int>(CurrentPersonCell.first, CurrentPersonCell.second + 1));
			}
			if (CurrentPersonCell.first > 0 && IsVisited[CurrentPersonCell.first - 1][CurrentPersonCell.second] == false && Grid[CurrentPersonCell.first - 1][CurrentPersonCell.second] == 0 && (PersonLayer + 1 < FireTime[CurrentPersonCell.first - 1][CurrentPersonCell.second] || FireTime[CurrentPersonCell.first - 1][CurrentPersonCell.second] == -1))
			{
				IsVisited[CurrentPersonCell.first - 1][CurrentPersonCell.second] = true;
				NewCurrentPerson.push_back(pair<int, int>(CurrentPersonCell.first - 1, CurrentPersonCell.second));
			}
			if (CurrentPersonCell.second > 0 && IsVisited[CurrentPersonCell.first][CurrentPersonCell.second - 1] == false && Grid[CurrentPersonCell.first][CurrentPersonCell.second - 1] == 0 && (PersonLayer + 1 < FireTime[CurrentPersonCell.first][CurrentPersonCell.second - 1] || FireTime[CurrentPersonCell.first][CurrentPersonCell.second - 1] == -1))
			{
				IsVisited[CurrentPersonCell.first][CurrentPersonCell.second - 1] = true;
				NewCurrentPerson.push_back(pair<int, int>(CurrentPersonCell.first, CurrentPersonCell.second - 1));
			}
		}
		PersonLayer++;
		CurrentPerson.clear();
		return PersonBFS(NewCurrentPerson);
	}

	void FireBFS(vector<pair<int, int>> CurrentFire)
	{
		if (CurrentFire.empty())
		{
			return;
		}
		vector<pair<int, int>> NewCurrentFire;
		for (auto CurrentFireCell : CurrentFire)
		{
			if (CurrentFireCell.first > 0 && FireTime[CurrentFireCell.first - 1][CurrentFireCell.second] == -1 && Grid[CurrentFireCell.first - 1][CurrentFireCell.second] == 0)
			{
				FireTime[CurrentFireCell.first - 1][CurrentFireCell.second] = FireLayer + 1;
				NewCurrentFire.push_back(pair<int, int>(CurrentFireCell.first - 1, CurrentFireCell.second));
			}
			if (CurrentFireCell.second > 0 && FireTime[CurrentFireCell.first][CurrentFireCell.second - 1] == -1 && Grid[CurrentFireCell.first][CurrentFireCell.second - 1] == 0)
			{
				FireTime[CurrentFireCell.first][CurrentFireCell.second - 1] = FireLayer + 1;
				NewCurrentFire.push_back(pair<int, int>(CurrentFireCell.first, CurrentFireCell.second - 1));
			}
			if (CurrentFireCell.first < n - 1 && FireTime[CurrentFireCell.first + 1][CurrentFireCell.second] == -1 && Grid[CurrentFireCell.first + 1][CurrentFireCell.second] == 0)
			{
				FireTime[CurrentFireCell.first + 1][CurrentFireCell.second] = FireLayer + 1;
				NewCurrentFire.push_back(pair<int, int>(CurrentFireCell.first + 1, CurrentFireCell.second));
			}
			if (CurrentFireCell.second < m - 1 && FireTime[CurrentFireCell.first][CurrentFireCell.second + 1] == -1 && Grid[CurrentFireCell.first][CurrentFireCell.second + 1] == 0)
			{
				FireTime[CurrentFireCell.first][CurrentFireCell.second + 1] = FireLayer + 1;
				NewCurrentFire.push_back(pair<int, int>(CurrentFireCell.first, CurrentFireCell.second + 1));
			}
		}
		FireLayer++;
		CurrentFire.clear();
		FireBFS(NewCurrentFire);
	}
};
 


int main()
{

	Solution sol;

	vector<vector<int>> grid = { {0, 2, 0, 0, 0, 0, 0}, {0, 0, 0, 2, 2, 1, 0}, {0, 2, 0, 0, 1, 2, 0}, {0, 0, 2, 2, 2, 0, 2}, {0, 0, 0, 0, 0, 0, 0} };

	vector<vector<int>> grid2 = { {0, 0, 0},{2, 2, 0 }, {1, 2, 0} };

	vector<vector<int>> grid3 = {{0, 0, 0, 0}, {0, 1, 2, 0}, {0, 2, 0, 0}};

	vector<vector<int>> grid4 = {{0, 2, 0, 0, 1}, {0, 2, 0, 2, 2}, {0, 2, 0, 0, 0}, {0, 0, 2, 2, 0}, {0, 0, 0, 0, 0}};
	
	vector<vector<int>> grid5 = {{0, 2, 1, 0, 0, 0, 0}, {0, 2, 2, 2, 2, 2, 0}, {0, 2, 0, 0, 0, 0, 0}, {0, 2, 0, 2, 2, 2, 2}, {0, 2, 0, 0, 0, 0, 0}, {0, 2, 2, 2, 2, 2, 0}, {0, 2, 0, 0, 0, 0, 0}, {0, 2, 0, 2, 2, 2, 2}, {0, 0, 0, 0, 0, 0, 0}};

	vector<vector<int>> grid6 = {{0, 0, 0, 0, 0}, {0, 2, 0, 2, 0}, {0, 2, 0, 2, 0}, {0, 2, 1, 2, 0}, {0, 2, 2, 2, 0}, {0, 0, 0, 0, 0}};
	cout << sol.maximumMinutes(grid6);
	
	
}

