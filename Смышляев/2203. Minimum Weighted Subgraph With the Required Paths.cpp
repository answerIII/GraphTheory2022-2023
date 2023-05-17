class Solution {
public:
    vector<long long> dej(int n, vector<vector<pair<int, long long>>>& adj, int x) {
        priority_queue<pair<long long, int>> q;
        vector<long long> distance(n);
        vector<bool> processed(n);
        for (int i = 0; i < n; i++) {
            distance[i] = LLONG_MAX;
        }
        distance[x] = 0;
        q.push({0, x});
        while (!q.empty()) {
            int a = q.top().second; q.pop();
            if (processed[a]) continue;
            processed[a] = true;
            for (auto u : adj[a]) {
                long long b = u.first, w = u.second;
                if (distance[a] + w < distance[b]) {
                    distance[b] = distance[a] + w;
                    q.push({-distance[b], b});
                }
            }
        }
        return distance;
    }

    vector<vector<pair<int, long long>>> generAdj(int n, vector<vector<int>>& edges, bool backwards=false) {
        vector<vector<pair<int, long long>>> mamba(n);
        for (int i = 0; i < edges.size(); ++i) {
            if (backwards) {mamba[edges[i][1]].push_back({edges[i][0], edges[i][2]});}
            else {mamba[edges[i][0]].push_back({edges[i][1], edges[i][2]});}
        }
        return mamba;
    }

    long long minimumWeight(int n, vector<vector<int>>& edges, int src1, int src2, int dest) {
        vector<vector<pair<int, long long>>> adj = generAdj(n, edges);
        vector<vector<pair<int, long long>>> adjBack = generAdj(n, edges, true);
        vector<long long> src1dist = dej(n, adj, src1);
        vector<long long> src2dist = dej(n, adj, src2);
        vector<long long> destDist = dej(n, adjBack, dest);
        long long ans = LLONG_MAX;
        for (int i = 0; i < n; ++i) {
            if (src1dist[i] == LLONG_MAX ||
                src2dist[i] == LLONG_MAX ||
                destDist[i] == LLONG_MAX) {continue;}
            ans = min(ans, src1dist[i] + src2dist[i] + destDist[i]);
        }
        if (ans == LLONG_MAX) {return -1;}
        return ans;
    }
};
