class Solution {
    long maxScore = 0;
    long result = 0;
public:
    int dfs(int u, int N,vector<vector<long>>& G) { 
        long score = 1;
        long res = 1;
        for (int i = 0; i < G[u].size(); i++){
            long c = dfs(G[u][i], N, G);
            res += c;
            score *= c;
        }
        long other = N - res; 
        if (other) {score *= other;}
        if (score > maxScore) {
            maxScore = score;
            result = 1;
        } else {if (score == maxScore) {
            result++;
            }}
        return res;
    };
    int countHighestScoreNodes(vector<int>& P) {
        int N = P.size();
        vector<vector<long>> G(N); 
        for (int i = 1; i < N; i++) {
            G[P[i]].push_back(i);
            }
        dfs(0, N, G);
        return result;
    }
};