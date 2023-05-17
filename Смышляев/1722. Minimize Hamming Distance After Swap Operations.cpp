class Solution {
public:
    int minimumHammingDistance(vector<int>& source, vector<int>& target, vector<vector<int>>& allowedSwaps) {
        int n = source.size();
        vector<vector<int>> adj (n);
        for (int i = 0; i < allowedSwaps.size(); ++i) {
            adj[allowedSwaps[i][0]].push_back(allowedSwaps[i][1]);
            adj[allowedSwaps[i][1]].push_back(allowedSwaps[i][0]);
        }
        vector<multiset<int>> conn;
        stack<int> dfsTmp;
        vector<int> aboba(n, -1);
        for (int i = 0; i < n; ++i) {
            if (aboba[i] != -1) {continue;}
            conn.push_back({});
            aboba[i] = conn.size() - 1;
            dfsTmp.push(i);
            conn[aboba[i]].insert(source[i]);
            while (!dfsTmp.empty()) {
                int tmp = dfsTmp.top();
                dfsTmp.pop();
                for (int j = 0; j < adj[tmp].size(); ++j) {
                    if (aboba[adj[tmp][j]] == -1) {
                        dfsTmp.push(adj[tmp][j]);
                        aboba[adj[tmp][j]] = conn.size() - 1;
                        conn[conn.size()-1].insert(source[adj[tmp][j]]);
                    }
                }
            }
        }

        int ans = 0;
        for (int i = 0; i < n; ++i) {
            int num = aboba[i];
            if (conn[num].find(target[i]) != conn[num].end()) {
                conn[num].erase(conn[num].find(target[i]));
            } else {
                ++ans;
            }
        }
        return ans;
    }
};
