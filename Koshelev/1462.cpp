class Solution {
public:
    void Floyd_Warshall(vector<vector<bool>> &adjacency_matrix)
    {
        for (int k = 0; k < adjacency_matrix.size(); k++)
        {
            for (int i = 0; i < adjacency_matrix.size(); i++)
            {
                for (int j = 0; j < adjacency_matrix.size(); j++)
                {
                    adjacency_matrix[i][j] = adjacency_matrix[i][j] | adjacency_matrix[i][k] & adjacency_matrix[k][j];
                }
            }
        }
    }

    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        vector<bool> answer(queries.size());

        vector<vector<bool>> adjacency_matrix(numCourses, vector<bool>(numCourses));
        for (int i = 0; i < prerequisites.size(); i++)
        {
            adjacency_matrix[prerequisites[i][0]][prerequisites[i][1]] = true;
        }

        Floyd_Warshall(adjacency_matrix);

        for (int i = 0; i < queries.size(); i++)
        {
            answer[i] = adjacency_matrix[queries[i][0]][queries[i][1]];
        }
        return answer;
    }
};