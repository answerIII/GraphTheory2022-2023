#define INF 0x3f3f3f3f

class Solution {
public:
    int Dijkstra_shortest_path(list<pair<int, int>>* adj, int src, int num_of_vertexes) {

        //очень странный синтаксис, нужно для приоритетной очереди с минимумом 
        std::priority_queue< pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>> > pqueue;

        std::vector<int> distance(num_of_vertexes, INF);

        pqueue.push(make_pair(0, src));
        distance[src] = 0;

        while (!pqueue.empty()) {

            int u = pqueue.top().second;
            pqueue.pop();

            list<pair<int, int>>::iterator i;
            for (i = adj[u].begin(); i != adj[u].end(); ++i) {

                int v = (*i).first;
                int weight = (*i).second;


                if (distance[v] > distance[u] + weight) {

                    distance[v] = distance[u] + weight;
                    pqueue.push(make_pair(distance[v], v));
                }
            }
        }

        // for (int i = 0; i < num_of_vertexes; ++i)
        //     cout << i << ": " << distance[i] << endl;

        //возвращаем дистанцию от вершины src до вершины num_of_vertexes - 1
        return distance[num_of_vertexes - 1];
    }

    int minCost(vector<vector<int>>& grid) {
        int result = 0;
        int rows = grid.size();
        int cols = grid[0].size();
        std::list<pair<int, int>>* adjList = new std::list<pair<int, int>>[rows * cols];

        //Преобразование растра в граф в виде списка смежности
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                if ((j + 1) < cols) //проверяем правого соседа
                    if (grid[i][j] == 1)
                        adjList[i * cols + j].push_back(make_pair(i * cols + j + 1, 0));
                    else
                        adjList[i * cols + j].push_back(make_pair(i * cols + j + 1, 1));

                if ((j - 1) > -1) //проверяем левого соседа
                    if (grid[i][j] == 2)
                        adjList[i * cols + j].push_back(make_pair(i * cols + j - 1, 0));
                    else
                        adjList[i * cols + j].push_back(make_pair(i * cols + j - 1, 1));

                if ((i + 1) < rows) //проверяем нижнего соседа
                    if (grid[i][j] == 3)
                        adjList[i * cols + j].push_back(make_pair((i + 1) * cols + j, 0));
                    else
                        adjList[i * cols + j].push_back(make_pair((i + 1) * cols + j, 1));

                if ((i - 1) > -1) //проверяем верхнего соседа
                    if (grid[i][j] == 4)
                        adjList[i * cols + j].push_back(make_pair((i - 1) * cols + j, 0));
                    else
                        adjList[i * cols + j].push_back(make_pair((i - 1) * cols + j, 1));

            }
        }

        // for (int i = 0; i < rows*cols; i++) {
        //     std::cout << i << ": ";
        //     while (!adjList[i].empty())
        //     {
        //         std::cout << adjList[i].front().first << "(" << adjList[i].front().second << ") ";
        //         adjList[i].pop_front();
        //     }
        //     std::cout << std::endl;
        // }

        result = Dijkstra_shortest_path(adjList, 0, rows * cols);

        return result;
    }
};