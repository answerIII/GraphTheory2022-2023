class Solution {
private: 
    int iMax, jMax;

    bool DFS(vector<vector<int>> &grid, int i, int j) { 
        if (i + 1 == iMax && j + 1 == jMax) 
            return true;
        if (i == iMax || j == jMax || grid[i][j] == 0) 
            return false;
        grid[i][j] = 0;
        return DFS(grid, i + 1, j) || DFS(grid, i, j + 1);
    }

public:
    Solution(): iMax(0), jMax(0) { }

    bool isPossibleToCutPath(vector<vector<int>>& grid) {
        iMax = grid.size();
        jMax = grid[0].size();
        
        if (!DFS(grid, 0, 0)) 
            return true;
        grid[0][0] = 1;
        return !DFS(grid, 0, 0);        
    }
};
