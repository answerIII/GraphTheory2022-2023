class Solution {
public:
    int minimumObstacles(vector<vector<int>>& grid) {
        int n = grid.size();
        int m = grid[0].size();

        //vector<vector<vector<int>>> graphList(n*m);
        /*for(int i = 0; i < n; i++){
            for(int j = 0; j < m; j++){
                if(j - 1 >= 0) graphList[i * m + j].push_back({ i * m  + j - 1, grid[i][j - 1]});
                if(j + 1 <  m) graphList[i * m + j].push_back({ i * m  + j + 1, grid[i][j + 1]});
                if(i - 1 >= 0) graphList[i * m + j].push_back({(i - 1) * m + j, grid[i - 1][j]});
                if(i + 1 <  n) graphList[i * m + j].push_back({(i + 1) * m + j, grid[i + 1][j]});
            }
        }*/

        //vector<int> dist(n*m, 1000000);
        //dist[0] = 0;
        vector<vector<int>>dist(n, vector<int>(m, 1e9));
        priority_queue<pair<int, pair<int, int>>, vector<pair<int, pair<int, int>>>, greater<pair<int, pair<int, int>>>> bfsQueue;

        dist[0][0] = 0;
        bfsQueue.push({ 0, {0,0} });
        while (!bfsQueue.empty()) {
            int i = bfsQueue.top().second.first;
            int j = bfsQueue.top().second.second;
            int weight = bfsQueue.top().first;
            //cout << "w, i, j: " << weight << " " << i << " " << j << endl; 
            bfsQueue.pop();
            if (i + 1 < n) {
                if (weight + grid[i + 1][j] < dist[i + 1][j]) {
                    dist[i + 1][j] = grid[i + 1][j] + weight;
                    bfsQueue.push({ dist[i + 1][j], {i + 1, j} });
                }
            }
            if (j + 1 < m) {
                if (weight + grid[i][j + 1] < dist[i][j + 1]) {
                    dist[i][j + 1] = grid[i][j + 1] + weight;
                    bfsQueue.push({ dist[i][j + 1], {i, j + 1} });
                }
            }
            if (i - 1 >= 0) {
                if (weight + grid[i - 1][j] < dist[i - 1][j]) {
                    dist[i - 1][j] = grid[i - 1][j] + weight;
                    bfsQueue.push({ dist[i - 1][j], {i - 1, j} });
                }
            }
            if (j - 1 >= 0) {
                if (weight + grid[i][j - 1] < dist[i][j - 1]) {
                    dist[i][j - 1] = grid[i][j - 1] + weight;
                    bfsQueue.push({ dist[i][j - 1], {i, j - 1} });
                }
            }
        }
        return dist[n - 1][m - 1];
    }

};