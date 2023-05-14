class Solution {
public: 
    double DFS(vector<vector<int>>& adjacency_matrix, vector<bool>& visited, int t, int target, int start, double probability)
    {
        visited[start] = true;
        int numberOfNeighbors;
        if (start == 1)
            numberOfNeighbors = adjacency_matrix[start].size();
        else
            numberOfNeighbors = adjacency_matrix[start].size() - 1;
        if (t == 0 || numberOfNeighbors == 0)
        {
            if (target == start)
                return probability;
            else
                return 0;
        }

        for (int i = 0; i < adjacency_matrix[start].size(); i++)
        {
            if (!visited[adjacency_matrix[start][i]])
            {
                double prob = DFS(adjacency_matrix, visited, t - 1, target, adjacency_matrix[start][i], probability * 1 / numberOfNeighbors);
                if (prob > 0)
                    return prob;
            }
        }
        return 0;
    }

    double frogPosition(int n, vector<vector<int>>& edges, int t, int target) {
        vector<vector<int>> adjacency_matrix(n + 1);
	    vector<bool> visited(n + 1);
        for (int i = 0; i < edges.size(); i++)
        {
            adjacency_matrix[edges[i][0]].push_back(edges[i][1]);
            adjacency_matrix[edges[i][1]].push_back(edges[i][0]);
        }
        return DFS(adjacency_matrix, visited, t, target, 1, 1);
    }
};