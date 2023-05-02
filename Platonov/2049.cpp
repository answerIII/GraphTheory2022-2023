class Solution {
public:
    int countHighestScoreNodes(vector<int>& parents) {
        int n = parents.size();
        int* degree = new int[n];
        int* sum = new int[n];
        long long* score = new long long[n];
        for (int i = 0; i < n; ++i) {
            degree[i] = 0;
            score[i] = 1;
            sum[i] = 1;
        }
        for (int i = 0; i < n; ++i) {
            if (parents[i] != -1) {
                ++degree[parents[i]];
            }
        }
        for (int i = 0; i < n; ++i) {
            if (degree[i] == 0) {
                int v = i;
                int count = 1;
                score[i] = n - 1;
                while (parents[v] != -1) {
                    if (degree[parents[v]] == 1) {
                        sum[parents[v]] += count;
                        score[parents[v]] *= count;
                        count = sum[parents[v]];
                        if (parents[parents[v]] != -1)
                            score[parents[v]] *= (n - sum[parents[v]]);
                        v = parents[v];
                    }
                    else {
                        sum[parents[v]] += count;
                        --degree[parents[v]];
                        score[parents[v]] *= count;
                        break;
                    }
                }
            }
        }
        long long maxScore = 1;
        int countMaxScoreNodes = 0;
        for (int i = 0; i < n; ++i) {
            if (maxScore < score[i]) {
                maxScore = score[i];
                countMaxScoreNodes = 1;
            } else if (score[i] == maxScore) {
                ++countMaxScoreNodes;
            }
        }
        return countMaxScoreNodes;
    }
};