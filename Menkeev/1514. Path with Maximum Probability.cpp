class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& pro, int start, int end) {

        list<pair<int, double>>* adj = new list<pair<int, double>>[n];

        for (int i = 0; i < edges.size(); i++) {
            int from = edges[i][0];
            int to = edges[i][1];
            double probability = pro[i];
            adj[from].push_back(make_pair(to, probability));
            adj[to].push_back(make_pair(from, probability));
        }

        vector<int> seen(n, 0);

        priority_queue<pair<double, int>> q;
        q.push({ (double)1.0, start });

        vector<double> mx(n, (double)0.0);
        mx[start] = 1.0;

        while (!q.empty()) {
            auto top = q.top();
            q.pop();
            double proba = top.first;
            int node = top.second;
            if (!seen[node]) {
                seen[node]++;
                for (auto& to : adj[node]) {
                    if (mx[to.first] < to.second * proba) {
                        mx[to.first] = to.second * proba;
                        q.push({ mx[to.first], to.first });
                    }
                }
            }
        }
        return mx[end];
    }
};