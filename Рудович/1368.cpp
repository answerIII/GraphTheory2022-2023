#include <vector>
#include <queue>

using namespace std;

class Solution {
public:

    pair<int, int> next(pair<int, int> pr, int m)
    {
        if (m == 1) return {pr.first, pr.second + 1};
        if (m == 2) return {pr.first, pr.second - 1};
        if (m == 3) return {pr.first + 1, pr.second};
        return {pr.first - 1, pr.second};
    }

    bool check(pair<int, int> pr, int n, int m)
    {
        if (pr.first < 0 || pr.first >= n || pr.second < 0 || pr.second >= m) return false;
        return true;
    }

    void addAll(queue<pair<int, int>> &q, vector<vector<int>>& v, vector<vector<int>>& grid, pair<int, int> pr, int t)
    {
        while(check(pr, grid.size(), grid[0].size()) && v[pr.first][pr.second] == -1)
        {
            v[pr.first][pr.second] = t;
            q.push(pr);
            pr = next(pr, grid[pr.first][pr.second]);
        }
    }

    int minCost(vector<vector<int>>& grid) 
    {
        int n = grid.size();
        int m = grid[0].size();
        vector<vector<int>> v(n, vector<int> (m, -1));
        queue<pair<int, int>> q;

        addAll(q, v, grid, {0, 0}, 0);
        
        while(!q.empty())
        {
            pair<int, int> cur = q.front();
            pair<int, int> tmp;
            if (grid[cur.first][cur.second] != 1) addAll(q, v, grid, next(cur, 1), v[cur.first][cur.second] + 1);
            if (grid[cur.first][cur.second] != 2) addAll(q, v, grid, next(cur, 2), v[cur.first][cur.second] + 1);
            if (grid[cur.first][cur.second] != 3) addAll(q, v, grid, next(cur, 3), v[cur.first][cur.second] + 1);
            if (grid[cur.first][cur.second] != 4) addAll(q, v, grid, next(cur, 4), v[cur.first][cur.second] + 1);
            q.pop();
        }
        return v[n - 1][m - 1];
    }
};