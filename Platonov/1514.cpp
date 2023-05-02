class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start, int end) {
        double dist[n];
        int m = edges.size();
        for (int i = 0; i < n; ++i) {
            dist[i] = 1e9;
        }
        for (int i = 0; i < m; ++i) {
            succProb[i] = -log(succProb[i]);
        }
        dist[start] = 0;
        bool ok;
        do {
            ok = false;
            for (int j = 0; j < m; ++j) {
                int from = edges[j][0];
                int to = edges[j][1];
                if (dist[from] < 1e9) {
                    double newDistance = dist[from] + succProb[j];
                    if (dist[to] > newDistance) {
                        dist[to] = newDistance;
                        ok = true;
                    } 
                }
                swap(from, to);
                if (dist[from] < 1e9) {
                    double newDistance = dist[from] + succProb[j];
                    if (dist[to] > newDistance) {
                        dist[to] = newDistance;
                        ok = true;
                    } 
                }
            }
        } while(ok);
        if (dist[end] == 1e9) return 0;
        else {
            return exp(-dist[end]);
        }
    }
};