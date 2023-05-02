class Solution {
public:
    // int reverse_DFS(vector<int> &manager, vector<int> &informTime, int i)
    // {
    //     if (manager[i] != -1)
    //     {
    //         informTime[i] += reverse_DFS(manager, informTime, manager[i]);
    //         manager[i] = -1;
    //     }
    //     return informTime[i];
    // }

    int DFS(vector<int>& informTime, vector<vector<int>>& adjacency_matrix, int i)
    {
        if (informTime[i] == 0)
            return 0;

        int maxTime = 0;
        for (int j = 0; j < adjacency_matrix[i].size(); j++)
        {
            maxTime = max(maxTime, DFS(informTime, adjacency_matrix, adjacency_matrix[i][j]));
        }
        return maxTime + informTime[i];
    }

    int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
        vector<vector<int>> adjacency_matrix(n);
        
        int maxTime = 0;
        // for (int i = 0; i < n; i++)
        // {
        //     int NodeTime = reverse_DFS(manager, informTime, i);
        //     if (maxTime < NodeTime)
        //         maxTime = NodeTime;
        // }

        for (int i = 0; i < n; i++)
        {
            if (manager[i] != -1)
                adjacency_matrix[manager[i]].push_back(i);
        }

        maxTime = DFS(informTime, adjacency_matrix, headID);
        return maxTime;
    }
};