class Solution {
public:
int countServers(std::vector<std::vector<int>>& grid) {
    int result = 0;
    int m = grid.size(), n = grid[0].size();
    std::vector<int> column(n,0), row(m,0);
    for(int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            if (grid[i][j] == 1)
                ++row[i], ++column[j], ++result;
    for (int i = 0; i < m; ++i)
        for (int j = 0; j < n; ++j)
            if (grid[i][j] == 1 && row[i] == 1 && column[j] == 1)
                --result;
    return result;
}
};
