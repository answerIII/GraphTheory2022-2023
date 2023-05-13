class Solution {
private: 
    void DFS(vector<int> adj[], int node, vector<int> &ans, int depth) {
        ans[node] = depth;
        for(int curr: adj[node]) {
            if(!ans[curr]) 
                DFS(adj, curr, ans, (depth + 1) % 5);
            else if(ans[curr] == ans[node]) 
                DFS(adj, node, ans, (depth + 1) % 5);
        }
    }
public:
    vector<int> gardenNoAdj(int n, vector<vector<int>>& paths) {
        vector<int> ans(n + 1, 0);
        vector<int> adj[n + 1];
        for(int i = 0; i < paths.size(); ++i) {
            adj[paths[i][0]].push_back(paths[i][1]);
            adj[paths[i][1]].push_back(paths[i][0]);
        }
        for(int i = 1; i <= n; ++i) {
            if(!ans[i]) 
                DFS(adj, i, ans, 1);
        }
        ans.erase(ans.begin());
        return ans;
    }
};
