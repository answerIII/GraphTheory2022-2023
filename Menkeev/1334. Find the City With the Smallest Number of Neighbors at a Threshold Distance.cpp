#define INF 0x3f3f3f3f
class Solution {
    int dThreshold;
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
        int count = 0;
        for (int i = 0; i < num_of_vertexes; i++) {
            if (distance[i] <= dThreshold)
                count++;
        }
        // cout << "vertex: " << src;
        // cout << " count: " << count << endl;

        return count;
    }


    int findTheCity(int n, vector<vector<int>>& edges, int distanceThreshold) {
        this->dThreshold = distanceThreshold;
        list<pair<int, int>>* adj = new list<pair<int, int>>[n];

        for (int i = 0; i < edges.size(); i++) {
            int from = edges[i][0];
            int to = edges[i][1];
            int distance = edges[i][2];
            adj[from].push_back(make_pair(to, distance));
            adj[to].push_back(make_pair(from, distance));
        }

        //  for (int i = 0; i < n; i++) {
        //     std::cout << i << ": ";
        //     for (auto adjacent : adj[i])
        //         std::cout << adjacent.first << "{" << adjacent.second << "} ";

        //     std::cout << std::endl;
        // }

        int min = INF;
        int city;
        for (int i = 0; i < n; i++) {
            int reachable_neighbors = Dijkstra_shortest_path(adj, i, n);

            if (min >= reachable_neighbors) {
                min = reachable_neighbors;
                city = i;
            }
        }


        // for (int i = 0; i < edges.size(); i++)
        // {
        //     for (int j = 0; j < edges[i].size(); j++)
        //         cout << edges[i][j] << " ";
        //     cout << endl;
        // }
        //cout << distanceThreshold;






        return city;
    }
};