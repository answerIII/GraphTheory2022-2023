class TreeAncestor {

public:

    vector<vector<int>> dp;

    TreeAncestor(int n, vector<int>& parent)
    {
        //будем хранить дерево предков
        dp = vector<vector<int>>(n, vector<int>(20));

        for (int i = 0; i < n; ++i)
            dp[i][0] = parent[i];

        for (int i = 0; i < 20; ++i)
            dp[0][i] = -1;

        for (int i = 1; i < 20; ++i)
        {
            for (int j = 1; j < n; ++j)
            {
                int parent1 = dp[j][i - 1];
                if (parent1 == -1)
                    dp[j][i] = -1;
                else
                    dp[j][i] = dp[parent1][i - 1];
            }
        }

    }

    int getKthAncestor(int node, int k) {
        int row = 0;
        while (k)
        {
            if (k & 1)
            {
                node = dp[node][row];
                if (node == -1)
                    return -1;
            }
            k = k >> 1;
            ++row;
        }

        return node;

    }
};