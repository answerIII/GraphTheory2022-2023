class Solution {
private: 
    int mod;
    vector<vector<pair<int, int>>> graph;
    vector<int> dist, dp;

    int DFS(int u) {
        if (u == 1)
            return 1;

        if (dp[u] != -1)
            return dp[u];

        dp[u] = 0;

        for (pair<int, int> i : graph[u]) {
            int v = i.first;
            if (dist[v] > dist[u])
                dp[u] = (dp[u] % mod + DFS(v) % mod) % mod;
        }

        return dp[u] % mod;
    }

    void dijkstra(int n) {
        vector<bool> finalized(n + 1, false);

        priority_queue< pair<int, int>, 
                        vector<pair<int, int>>, 
                        greater<pair<int, int>> > pq;
        dist[n] = 0;
        pq.push({0, n});

        while (!pq.empty()) {
            int dist_u = pq.top().first,
                u = pq.top().second;
            pq.pop();

            if (finalized[u])
                continue;

            finalized[u] = true;
            for (pair<int, int> i : graph[u]) {
                int v = i.first,
                    weight = i.second;

                if (dist_u + weight < dist[v]) {
                    dist[v] = dist_u + weight;
                    pq.push({dist[v], v});
                }
            }
        }
    }

public:
    Solution(): mod(1e9 + 7) {}

    int countRestrictedPaths(int n, vector<vector<int>> &edges) {
        graph = vector<vector<pair<int, int>>> (n + 1);
        dist = vector<int> (n + 1, INT_MAX);
        dp = vector<int> (n + 1, -1);

        for (int i = 0; i < edges.size(); ++i) {
            graph[edges[i][0]].push_back({edges[i][1], edges[i][2]});
            graph[edges[i][1]].push_back({edges[i][0], edges[i][2]});
        }

        dijkstra(n);
        return DFS(n);
    }
};
