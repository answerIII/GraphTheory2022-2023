class Solution {
public:

    bool DFS_contains_cycle(std::list<int>* adjList, int numberOfVertexes) {

        bool has_cycle = false;
        bool* visited = new bool[numberOfVertexes];
        int* parent = new int[numberOfVertexes];

        for (int i = 0; i < numberOfVertexes; i++) {
            visited[i] = false;
            parent[i] = -1;
        }

        for (int i = 0; i < numberOfVertexes; i++)
            if (!visited[i])
                DFS_visit(adjList, i, visited, parent, has_cycle);

        delete[] visited;
        delete[] parent;
        return has_cycle;
    }

    void DFS_visit(std::list<int>* adjList, int vertex, bool* visited, int* parent, bool& has_cycle) {

        visited[vertex] = true;

        while (!adjList[vertex].empty())
        {
            int adj_vertex = adjList[vertex].front();

            if (visited[adj_vertex] == false)
            {
                parent[adj_vertex] = vertex;
                DFS_visit(adjList, adj_vertex, visited, parent, has_cycle);
            }

            else if (parent[vertex] != adj_vertex)
                has_cycle = true;

            adjList[vertex].pop_front();
        }

    }


    bool containsCycle(vector<vector<char>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();
        std::list<int>* adjList = new std::list<int>[rows * cols];

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++)
            {
                if ((j + 1) < cols && grid[i][j] == grid[i][j + 1])
                    adjList[i * cols + j].push_back(i * cols + j + 1);

                if ((j - 1) > -1 && grid[i][j] == grid[i][j - 1])
                    adjList[i * cols + j].push_back(i * cols + j - 1);

                if ((i - 1) > -1 && grid[i][j] == grid[i - 1][j])
                    adjList[i * cols + j].push_back((i - 1) * cols + j);

                if ((i + 1) < rows && grid[i][j] == grid[i + 1][j])
                    adjList[i * cols + j].push_back((i + 1) * cols + j);
            }
        }

        // for (int i = 0; i < rows*cols; i++) {
        //     std::cout << i << ": ";
        //     while (!adjList[i].empty())
        //     {
        //         std::cout << adjList[i].front() << " ";
        //         adjList[i].pop_front();
        //     }
        //     std::cout << std::endl;
        // }
        bool result = DFS_contains_cycle(adjList, rows * cols);
        delete[] adjList;

        return result;
    }
};