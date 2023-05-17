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
                if (distance[a] <= w && distance[b] > w) {
                    distance[b] = w;
                    q.push({-distance[b], b});
                }
            }
        }
        return distance;
    }
    vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        meetings.push_back({0, firstPerson, 0});
        vector<vector<pair<int, long long>>> adj (n);
        for (int i = 0; i < meetings.size(); ++i) {
            adj[meetings[i][0]].push_back({meetings[i][1], meetings[i][2]});
            adj[meetings[i][1]].push_back({meetings[i][0], meetings[i][2]});
        }
        vector<long long> d = dej(n, adj, 0);
        vector<int> ans;
        for (int i = 0; i < d.size(); ++i) {
            if (d[i] < LLONG_MAX) {ans.push_back(i);}
        }
        return ans;
    }
};
