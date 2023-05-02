
class Solution
{
private:

    bool cycleFinder(vector<vector<char>>& grid, vector<vector<bool>>& visited, const int x, const  int y, int preX, int preY)
    {

        visited[x][y] = true;

        if (y != grid[0].size() - 1 && grid[x][y + 1] == grid[preX][preY] && y + 1 != preY) // !!
        {
            if (visited[x][y + 1] || cycleFinder(grid, visited, x, y + 1, x, y)) {
                return true;
            }
        }

        if (x != grid.size() - 1 && grid[x + 1][y] == grid[preX][preY] && x + 1 != preX)
        {
            if (visited[x + 1][y] || cycleFinder(grid, visited, x + 1, y, x, y)) {
                return true;
            }
        }

        if (y && grid[x][y - 1] == grid[preX][preY] && y - 1 != preY)
        {
            if (visited[x][y - 1] || cycleFinder(grid, visited, x, y - 1, x, y)) {
                return true;
            }
        }

        if (x && grid[x - 1][y] == grid[preX][preY] && x - 1 != preX)
        {
            if (visited[x - 1][y] || cycleFinder(grid, visited, x - 1, y, x, y)) {
                return true;
            }
        }
        return false;
    }

public:
    bool containsCycle(vector<vector<char>>& grid)
    {
        vector<vector<bool>> visited(grid.size(), vector<bool>(grid[0].size(), false));

        for (int i = 0; i < grid.size(); ++i)
        {
            for (int j = 0; j < grid[i].size(); ++j)
            {
                if (!visited[i][j] && cycleFinder(grid, visited, i, j, i, j))
                {
                    return true;
                }
            }
        }
        return false;
    }
};
