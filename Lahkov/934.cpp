#include <vector>
#include <iostream>
using namespace std;

class Solution {
public:
    void bfs(vector<vector<int>>& _grid, vector<pair<int, int>>& _q, int _i, int _j) {
        if (!(_i >= 0 && _i < _grid.size() && _j >= 0 && _j < _grid.size() && _grid[_i][_j] == 1)) return;
        _grid[_i][_j] = 2;
        if ((_i >= 1 && _grid[_i - 1][_j] == 0) || (_i < _grid.size() - 1 && _grid[_i + 1][_j] == 0) || (_j >= 1 && _grid[_i][_j - 1] == 0) || (_j < _grid.size() - 1 && _grid[_i][_j + 1] == 0))
            _q.push_back({ _i,_j });
        bfs(_grid, _q, _i + 1, _j);
        bfs(_grid, _q, _i - 1, _j);
        bfs(_grid, _q, _i, _j + 1);
        bfs(_grid, _q, _i, _j - 1);
    }
    int shortestBridge(vector<vector<int>>& grid) {
        vector<pair<int, int>> q;
        bool flag = false;
        for (int i = 0; i < grid.size(); i++) {
            for (int j = 0; j < grid.size(); j++) {
                if (grid[i][j] == 1) {
                    bfs(grid, q, i, j);
                    flag = true;
                    break;
                }
            }
            if (flag == true) break;
        }


        int distance = 0;
        vector<pair<int, int>> q2;
        while (!q.empty()) {
            q2.clear();

            for (vector<pair<int, int>>::iterator it = q.begin(); it != q.end(); ++it) {
                if (grid[it->first][it->second] == -1) continue;
                grid[it->first][it->second] = -1;
                if (it->first > 0) {
                    if (grid[it->first - 1][it->second] == 1) return distance;
                    else if (grid[it->first - 1][it->second] == 0) q2.push_back({ it->first - 1 ,it->second });
                }
                if (it->first < grid.size() - 1) {
                    if (grid[it->first + 1][it->second] == 1) return distance;
                    else if (grid[it->first + 1][it->second] == 0) q2.push_back({ it->first + 1 ,it->second });
                }
                if (it->second > 0) {
                    if (grid[it->first][it->second - 1] == 1) return distance;
                    else if (grid[it->first][it->second - 1] == 0) q2.push_back({ it->first ,it->second - 1 });
                }
                if (it->second < grid.size() - 1) {
                    if (grid[it->first][it->second + 1] == 1) return distance;
                    else if (grid[it->first][it->second + 1] == 0) q2.push_back({ it->first ,it->second + 1 });
                }

            }
            if (!q2.empty())
            {
                swap(q, q2);
                distance++;
            }
        }
        return -1;
    }
};