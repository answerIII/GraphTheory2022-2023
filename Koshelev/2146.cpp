class Solution {
public:
    vector<vector<int>> highestRankedKItems(vector<vector<int>>& grid, vector<int>& pricing, vector<int>& start, int k) {
        queue<vector<int>> q;
        vector<vector<bool>> visited(grid.size(), vector<bool>(grid[0].size(), false));
        vector<vector<int>> items;
        q.push({ start[0], start[1], 0 });
        while (q.size() != 0)
        {
            vector<int> cell = q.front();
            q.pop();
            if (visited[cell[0]][cell[1]])
                continue;
            if (grid[cell[0]][cell[1]] == 0)
                continue;
            visited[cell[0]][cell[1]] = true;
            if (grid[cell[0]][cell[1]] != 1 && grid[cell[0]][cell[1]] >= pricing[0] && grid[cell[0]][cell[1]] <= pricing[1])
            {
                items.push_back({ cell[2], grid[cell[0]][cell[1]], cell[0], cell[1] });
            }
            if (cell[0] - 1 >= 0)
                q.push({ cell[0] - 1, cell[1], cell[2] + 1 });
            if (cell[0] + 1 <= grid.size() - 1)
                q.push({ cell[0] + 1, cell[1], cell[2] + 1 });
            if (cell[1] - 1 >= 0)
                q.push({ cell[0], cell[1] - 1, cell[2] + 1 });
            if (cell[1] + 1 <= grid[0].size() - 1)
                q.push({ cell[0], cell[1] + 1, cell[2] + 1 });
        }
        sort(items.begin(), items.end());
        vector<vector<int>> result;
        for (int i = 0; i < min(k, int(items.size())); i++)
            result.push_back({ items[i][2], items[i][3] });
        return result;
    }
};