#include <vector>
#include <iostream>
using namespace std;

class Solution {
private:
    int n;
    long max_result = 0;
    int count_max_result = 0;
    int dfs(vector<vector<int>>& children, int pos) {
        long result = 1;
        int sum = 0;
        for (int i = 0; i < children[pos].size(); i++) {
            int tmp = dfs(children, children[pos][i]);
            sum += tmp;
            result *= tmp;
        }
        int rem = n - sum - 1;
        if (rem > 0)
            result *= rem;
        if (result > max_result) {
            max_result = result;
            count_max_result = 1;
        }
        else if (result == max_result)
            count_max_result += 1;
        return sum + 1;
    }
public:

    int countHighestScoreNodes(vector<int>& parents) {
        n = parents.size();
        vector<vector<int>> children(n);
        for (int i = 1; i < n; i++) {
            children[parents[i]].push_back(i);
        }
        dfs(children, 0);

        return count_max_result;
    }
};