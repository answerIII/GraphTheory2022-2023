
class Solution {
private:
    const long long INF;
    vector<pair<int, long long>> adjacency[100000];
    
    vector<long long> Dijkstra(int &src , int &n) {        
        vector<long long> distance(n + 1, INF);
        distance[src] = 0;    

        vector<bool> visited(n, false);        
        priority_queue<pair<long long, int>, 
                       vector<pair<long long, int>>, 
                       greater<pair<long long, int>>> q;
        q.push({0, src});
        
        while (!q.empty()) {
            long long wt = q.top().first;
            int v = q.top().second;
            q.pop();
            
            if (visited[v]) continue;
            
            visited[v] = true;
            for (pair<int, long long> ch: adjacency[v]) {
                if (!visited[ch.first] && wt + ch.second < distance[ch.first]) {
                    distance[ch.first] = wt + ch.second;
                    q.push({distance[ch.first], ch.first});
                }
            }
        }
        return distance;        
    }

    long long getAnswer(int &n, vector<vector<int>>& edges, int &src1, int &src2, int &dest){
        for (vector<int> v: edges) 
            adjacency[v[0]].push_back({v[1], v[2]});

        vector<long long> dist1 = Dijkstra(src1, n);
        vector<long long> dist2 = Dijkstra(src2, n);
        
        for (vector<pair<int, long long>> &v: adjacency) 
            v.clear();
        for (vector<int> v: edges) 
            adjacency[v[1]].push_back({v[0], v[2]});
        
        vector<long long> dist3 = Dijkstra(dest, n);
        
        if (dist1[dest] == INF || dist2[dest] == INF) 
            return -1;           
        
        long long ans = dist1[dest] + dist2[dest];
        for (int i = 0; i < n; ++i)
            ans = min(ans, dist1[i] + dist2[i] + dist3[i]);

        return ans;
    }

public:  
    Solution(): INF((long long)1e16) {}

    long long minimumWeight(int n, vector<vector<int>>& edges, int src1, int src2, int dest) {
        return getAnswer(n, edges, src1, src2, dest);
    }
};
