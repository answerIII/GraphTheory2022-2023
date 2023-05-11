#include <vector>
#include <cmath>

using namespace std;

class TreeAncestor {
private:
vector<vector<int>> dp;

public:
    TreeAncestor(int n, vector<int>& parent): dp(n, vector<int>(log2(n) + 1, -1))
    {
        for (int i = 0; i < n; ++i)
        {
            fun(parent, i);
        }
    }

    void fun(vector<int>& parent, int k)
    {
        if (parent[k] == -1)
        {
            return;
        }
        if (dp[k][0] != -1)
        {
            return;
        }
        dp[k][0] = parent[k];
        for (int i = 1; i < dp[k].size(); ++i)
        {
            if (dp[k][i - 1] == -1)
            {
                dp[k][i] = -1;
            }
            else
            {
                fun(parent, dp[k][i - 1]);
                dp[k][i] = dp[dp[k][i - 1]][i - 1];
            }
        }
    }
    
    int getKthAncestor(int node, int k) 
    {
        if (node == -1)
        {
            return -1;
        }
        if (k == 0)
        {
            return node;
        }
        int p = 0;
        int s = 1;
        while(s * 2 < k)
        {
            ++p;
            s *= 2;
        }
        return getKthAncestor(dp[node][p], k - s);
    }
};