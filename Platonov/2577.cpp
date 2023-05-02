int dx[4] = {0,  0, 1, -1};
int dy[4] = {1, -1, 0,  0};

class Solution {
public:
    int minimumTime(vector<vector<int>>& grid) {    
        if (grid[1][0] - grid[0][0] > 1 && grid[0][1] - grid[0][0] > 1) {
            return -1;
        }
        priority_queue<pair<int, pair<int, int> >, vector<pair<int, pair<int, int> > >, greater<pair<int, pair<int, int> > > > pq;
        int m = grid.size();
        int n = grid[0].size();
        int** dist = new int*[m];
        for (int i = 0; i < m; ++i) {
            dist[i] = new int[n];
            for (int j = 0; j < n; ++j) {
                dist[i][j] = 1e9;
            }
        }
        dist[0][0] = 0;
        pq.push(make_pair(0, make_pair(0, 0)));
        while (!pq.empty()) {
            pair<int, pair<int, int> > e = pq.top();
            int x = e.second.first;
            int y = e.second.second;
            pq.pop();
            for (int i = 0; i < 4; ++i) {
                int toX = x + dx[i];
                int toY = y + dy[i];
                if (!(toX < 0 || toX >= m || toY < 0 || toY >= n)) {
                    int d;
                    if (grid[toX][toY] >= dist[x][y] + 1 + (1 - (grid[toX][toY] - dist[x][y]) % 2)) {
                        d = grid[toX][toY] + (1 - (grid[toX][toY] - dist[x][y]) % 2);
                    } else {
                        d = dist[x][y] + 1;
                    }
                    if (grid[toX][toY] <= d && dist[toX][toY] > d) {
                        dist[toX][toY] = d;
                        pq.push(make_pair(dist[toX][toY], make_pair(toX, toY)));
                    }
                }
            }
        }
        return dist[m-1][n-1] == 1e9 ? -1 : dist[m-1][n-1];
    }
};