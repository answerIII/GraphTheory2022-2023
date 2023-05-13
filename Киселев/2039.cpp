class Solution {
private:
    int n;
    int start_node;
    vector<int> dist;

    vector<int> getDist(vector<vector<int>>& edges) {
        dist[start_node] = 0;   

        queue<int> q;
        q.push(start_node);

        vector<vector<int>> adj(n);        
        for(vector<int> u : edges) {
            adj[u[0]].push_back(u[1]);
            adj[u[1]].push_back(u[0]);
        }
        int v;
        while (!q.empty()) {
            v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (dist[u] > dist[v] + 1) {
                    dist[u] = dist[v] + 1;
                    q.push(u);
                }
            }
        }
        return dist;
    }

    int getResult(vector<int>& patience){
        int res = 0;
        int extra_pay_load, last_out, last_in;
        for(int i = 1; i < n; ++i) {
            extra_pay_load = (dist[i] * 2 - 1) / patience[i]; 
			last_out = extra_pay_load * patience[i]; 
            last_in = last_out + dist[i] * 2; 
			
            res = max(res, last_in);
        }
        return ++res;
    }

public:
    Solution(): n(0), start_node(0) { }
    int networkBecomesIdle(vector<vector<int>>& edges, vector<int>& patience) {
        n = patience.size();
        dist = vector<int>(n, n);
        getDist(edges);
        return getResult(patience);
    }
};
