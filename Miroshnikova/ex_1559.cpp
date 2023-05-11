#include <vector>
using namespace std;

const int FROM_UP = 0;
const int FROM_DOWN = 1;
const int FROM_LEFT = 2;
const int FROM_RIGHT = 3;
const int FROM_NONE = 4;

bool DFS(int idx, int jdx, vector<vector<char>>& grid, vector<vector<bool>>& visited, int side) {
    if (visited[idx][jdx] == true)
        return true;
    else
        visited[idx][jdx] = true;
    char sample = grid[idx][jdx];
    int m = grid.size();
    int n = grid[0].size();
    bool result = false;

    if (side == FROM_UP) {
        if ((idx < m - 1) && (grid[idx + 1][jdx] == sample))
            result += DFS(idx + 1, jdx, grid, visited, FROM_UP);
        if ((jdx < n - 1) && (grid[idx][jdx + 1] == sample))
            result += DFS(idx, jdx + 1, grid, visited, FROM_LEFT);
        if ((jdx > 0) && (grid[idx][jdx - 1] == sample))
            result += DFS(idx, jdx - 1, grid, visited, FROM_RIGHT);
    }
    else if (side == FROM_DOWN) {
        if ((jdx < n - 1) && (grid[idx][jdx + 1] == sample))
            result += DFS(idx, jdx + 1, grid, visited, FROM_LEFT);
        if ((idx > 0) && (grid[idx - 1][jdx] == sample))
            result += DFS(idx - 1, jdx, grid, visited, FROM_DOWN);
        if ((jdx > 0) && (grid[idx][jdx - 1] == sample))
            result += DFS(idx, jdx - 1, grid, visited, FROM_RIGHT);
    }
    else if (side == FROM_LEFT) {
        if ((idx < m - 1) && (grid[idx + 1][jdx] == sample))
            result += DFS(idx + 1, jdx, grid, visited, FROM_UP);
        if ((jdx < n - 1) && (grid[idx][jdx + 1] == sample))
            result += DFS(idx, jdx + 1, grid, visited, FROM_LEFT);
        if ((idx > 0) && (grid[idx - 1][jdx] == sample))
            result += DFS(idx - 1, jdx, grid, visited, FROM_DOWN);
    }
    else if (side == FROM_RIGHT) {
        if ((idx < m - 1) && (grid[idx + 1][jdx] == sample))
            result += DFS(idx + 1, jdx, grid, visited, FROM_UP);
        if ((idx > 0) && (grid[idx - 1][jdx] == sample))
            result += DFS(idx - 1, jdx, grid, visited, FROM_DOWN);
        if ((jdx > 0) && (grid[idx][jdx - 1] == sample))
            result += DFS(idx, jdx - 1, grid, visited, FROM_RIGHT);
    }
    else if (side == FROM_NONE) {
        if ((idx < m - 1) && (grid[idx + 1][jdx] == sample))
            result += DFS(idx + 1, jdx, grid, visited, FROM_UP);
        if ((idx > 0) && (grid[idx - 1][jdx] == sample))
            result += DFS(idx - 1, jdx, grid, visited, FROM_DOWN);
        if ((jdx < n - 1) && (grid[idx][jdx + 1] == sample))
            result += DFS(idx, jdx + 1, grid, visited, FROM_LEFT);
        if ((jdx > 0) && (grid[idx][jdx - 1] == sample))
            result += DFS(idx, jdx - 1, grid, visited, FROM_RIGHT);
    }
    return result;
}

class Solution {
public:
    bool containsCycle(vector<vector<char>>& grid) {

        // copy of grid with isVisited flags
        vector<vector<bool>> visited;
        int m = grid.size();
        int n = grid[0].size();
        for (int i = 0; i < m; ++i)
        {
            visited.push_back(vector<bool>());
            for (int j = 0; j < n; ++j)
                visited[i].push_back(false);
        }

        for (int i = 0; i < m; ++i)
        {
            for (int j = 0; j < n; ++j) {
                if (!visited[i][j])
                    if (DFS(i, j, grid, visited, FROM_NONE))
                        return true;
            }
        }
        return false;
    }
};

/*int main() {
    vector<vector<char>> grid;
    grid.push_back(vector<char>({'f', 'a', 'a', 'c', 'b'}));
    grid.push_back(vector<char>({ 'e', 'a', 'a', 'e', 'c'}));
    grid.push_back(vector<char>({ 'c', 'f', 'b', 'b', 'b'}));
    grid.push_back(vector<char>({ 'f', 'e', 'f', 'b', 'f'}));
    Solution sol;

    bool result = sol.containsCycle(grid);
    return 0;
}*/

// 1559