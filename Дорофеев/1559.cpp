class Solution
{
public:
    bool answer = false;
    int row, col;

    void DFS(vector<vector<char>>& grid, vector<vector<bool>>& visited,
        int r, int c, int pr, int pc)
    {
        if (visited[r][c])
        {
            answer = true;
            return;
        }
        visited[r][c] = true;
        if (r + 1 < row && r + 1 != pr && grid[r + 1][c] == grid[r][c])
            DFS(grid, visited, r + 1, c, r, c);
        if (c + 1 < col && c + 1 != pc && grid[r][c + 1] == grid[r][c])
            DFS(grid, visited, r, c + 1, r, c);
        if (r - 1 >= 0 && r - 1 != pr && grid[r - 1][c] == grid[r][c])
            DFS(grid, visited, r - 1, c, r, c);
        if (c - 1 >= 0 && c - 1 != pc && grid[r][c - 1] == grid[r][c])
            DFS(grid, visited, r, c - 1, r, c);
    }

    bool containsCycle(vector<vector<char>>& grid)
    {
        row = grid.size();
        col = grid[0].size();

        vector<vector<bool>> visited(row, vector<bool>(col, false));

        for (int i = 0; i < visited.size(); ++i)
            for (int j = 0; j < visited[0].size(); ++j)
                if (!visited[i][j])
                    DFS(grid, visited, i, j, -1, -1);

        return answer;
    }
};