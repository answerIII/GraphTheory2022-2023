class Solution {
public:

    vector<vector<int>> getAncestors(int n, vector<vector<int>>& edges) {
        vector<vector<int>> result(n);
        vector<vector<int>> graphVector(n);
       
        for(auto edge: edges){
            graphVector[edge[0]].push_back(edge[1]);
        }
        for(int i = 0; i < n; i++){
            vector<bool> findedVertex(n, false);
            DFS(graphVector, result, i, i, findedVertex);
        }
        return result;

    }

    void BFS(int n, vector<vector<int>>& graphVector, int v, vector<vector<int>>& result){
        int startV = v;
        vector<bool> findedVertex(n, false);
        queue<int> q;
        
        q.push(v);
        findedVertex[v] = true;

        while (!q.empty()){
            v = q.front();
            q.pop();
            
            for (auto u: graphVector[v]){
                if (!findedVertex[u]){
                    findedVertex[u] = true;
                    q.push(u);
                    result[u].push_back(startV);
                }
            }
        }
    }

    void DFS(vector<vector<int>>& graphVector, vector<vector<int>>& result, int v, int u,vector<bool>& findedVertex){
        findedVertex[u] = true;
        for(auto vert: graphVector[u]){
            if(!findedVertex[vert]){
                result[vert].push_back(v);
                DFS(graphVector, result, v, vert, findedVertex);
            }
        }
    }






   
};
