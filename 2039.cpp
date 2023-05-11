#include <vector>
#include <queue>

using namespace std;

class Solution {
public:
    int networkBecomesIdle(vector<vector<int>>& edges, vector<int>& patience) 
    {
        int n = patience.size();
        vector<vector<int>> graph(n);
        for (auto &i : edges)
        {
            graph[i[0]].emplace_back(i[1]);
            graph[i[1]].emplace_back(i[0]);
        }

        vector<int> path(n, INT_MAX);
        path[0] = 0;
        queue<int> q;
        q.push(0);
        while(!q.empty())
        {
            int nd = q.front();
            q.pop();
            for (int i = 0; i < graph[nd].size(); ++i)
            {
                if (path[graph[nd][i]] == INT_MAX)
                {
                    path[graph[nd][i]] = path[nd] + 1;
                    q.push(graph[nd][i]);
                }
            }
        }
        int ans = 0;
        for (int i = 1; i < n; ++i)
        {
            int path_size = path[i] * 2;
            int p = path_size % patience[i];

            if (path_size <= patience[i]) ans = max(ans, path_size + 1);
            else if (p != 0) ans = max(ans, path_size + path_size - p + 1);
            else ans = max(ans, path_size + path_size - patience[i] + 1);
        }
        return ans;
    }
};