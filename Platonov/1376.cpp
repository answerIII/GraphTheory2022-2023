class Solution {
public:
    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        int* degree = new int[n];
        int* maxTimeToInform = new int[n];
        for (int i = 0; i < n; ++i) {
            degree[i] = 0;
            maxTimeToInform[i] = 0;
        }
        for (int i = 0; i < n; ++i) {
            if (manager[i] != -1) {
                ++degree[manager[i]];
            }
        }
        for (int i = 0; i < n; ++i) {
            if (degree[i] == 0) {
                int v = i;
                while (manager[v] != -1) {
                    maxTimeToInform[manager[v]] = max(maxTimeToInform[manager[v]], informTime[manager[v]] + maxTimeToInform[v]);
                    if (degree[manager[v]] == 1) {
                        v = manager[v];
                    } else {
                        --degree[manager[v]];
                        break;
                    }
                }
            }
        }
        int result = 0;
        for (int i = 0; i < n; ++i) {
            result = max(result, maxTimeToInform[i]);
        }
        return result;
    }
};