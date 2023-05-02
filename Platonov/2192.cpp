class Solution {
public:
    vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
        vector<vector<int> > edges1(n);
        for (int i = 0; i < edges.size(); ++i) {
            edges1[edges[i][1]].push_back(edges[i][0]);
        }
        vector<bool> used(n, false);
        queue<int> q;
        int v;
        vector<vector<int> > result(n);
        for (int start = 0; start < n; ++start) {
            used[start] = true;
            q.push(start);
            while (!q.empty()) {
                v = q.front();
                q.pop();
                for (int i = 0; i < edges1[v].size(); ++i) {
                    if (!used[edges1[v][i]]) {
                        used[edges1[v][i]] = true;
                        q.push(edges1[v][i]);
                    }
                }
            }
            for (int i = 0; i < n; ++i) {
                if (used[i]) {
                    if (i != start) {
                        result[start].push_back(i);
                    }
                    used[i] = false;
                }
            }
        }
        return result;
    }
};