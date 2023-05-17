class Solution {
public:
    bool checkInner(vector<vector<int>>& grid, int row, int col, int color) {
        bool flagRow = false;
        bool flagCol = false;
        if (col == 0 or col + 1 == grid[0].size()) {flagCol = false;}
        else if (grid[row][col+1] == color && grid[row][col-1] == color) {flagCol = true;}
        if (row == 0 or row + 1 == grid.size()) {flagRow = false;}
        else if (grid[row+1][col] == color && grid[row-1][col] == color) {flagRow = true;}
        if (flagRow && flagCol) {return true;}
        else {return false;}
    }

    void walkTheGrid(vector<vector<int>>& grid, vector<vector<int>>& walkedGrid, vector<pair<int, int>>& border, int row, int col, int color) {
        walkedGrid[row][col] = 1;
        if (!checkInner(grid, row, col, color)) {border.push_back({row, col});}
        if (col != 0) {
            if (grid[row][col-1] == color && walkedGrid[row][col-1] == 0) {walkTheGrid(grid, walkedGrid, border, row, col-1, color);}
        }
        if (col + 1 != grid[0].size()) {
            if (grid[row][col+1] == color && walkedGrid[row][col+1] == 0) {walkTheGrid(grid, walkedGrid, border, row, col+1, color);}
        }
        if (row != 0) {
            if (grid[row-1][col] == color && walkedGrid[row-1][col] == 0) {walkTheGrid(grid, walkedGrid, border, row-1, col, color);}
        }
        if (row + 1 != grid.size()) {
            if (grid[row+1][col] == color && walkedGrid[row+1][col] == 0) {walkTheGrid(grid, walkedGrid, border, row+1, col, color);}
        }
    }

    vector<vector<int>> colorBorder(vector<vector<int>>& grid, int row, int col, int color) {
        vector<vector<int>> walkedGrid(grid.size(), vector<int>(grid[0].size(), 0));
        vector<pair<int, int>> border;
        walkTheGrid(grid, walkedGrid, border, row, col, grid[row][col]);
        for (int i = 0; i < border.size(); ++i) {
            grid[border[i].first][border[i].second] = color;
        }
        return grid;
    }
};
