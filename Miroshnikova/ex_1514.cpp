#include <vector>
#include <list>

using namespace std;

const int INF = -1;

void delete_from_queue(int n, list<int>& vertex_queue)
{
    // delete from old place in queue
    auto iterator = vertex_queue.begin();
    for (int i = 0; i < vertex_queue.size(); ++i) {
        if (*iterator == n) {
            vertex_queue.erase(iterator);
            return;
        }
        advance(iterator, 1);
    }
}

void insert_to_queue(int n, list<int>& vertex_queue, vector<double>& vertex_distance) {
    double dist = vertex_distance[n];

    auto iterator = vertex_queue.begin();
    for (int i = 0; i < vertex_queue.size(); ++i) {
        if (vertex_distance[*iterator] < 0) {
            vertex_queue.insert(iterator, n);
            return;
        }
        else if (vertex_distance[*iterator] > dist) {
            vertex_queue.insert(iterator, n);
            return;
        }
        advance(iterator, 1);
    }
    // insert to the end
    vertex_queue.insert(iterator, n);
}

// delete vertex with updated distance and then insert it to the queue to the right position
void resort_queue(int n, list<int>& vertex_queue, vector<double>& vertex_distance) {

    delete_from_queue(n, vertex_queue);

    // insert to new place
    insert_to_queue(n, vertex_queue, vertex_distance);
}

class Vertex {
public:
    int node;
    double weight;

    Vertex() {}

    Vertex(int node, double weight) : node(node), weight(weight) {};
};

class Solution {
public:
    static double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start, int end) {

        // Create queue (sorted list, start = min distance, end = max distance) of vertexes
        list<int> vertex_queue;

        vector<bool> vertes_visited;
        vector<double> vertex_distance;
        vector<vector<Vertex>> adj_to_vertex;
        for (int i = 0; i < n; ++i) {
            vertex_distance.push_back(INF);
            vertes_visited.push_back(false);
            adj_to_vertex.push_back(vector<Vertex>());
        }
        vertex_queue.push_back(start);
        vertex_distance[start] = 1;

        int i = 0;
        for (auto& edge : edges) {
            int start_ = edge[0];
            int end_ = edge[1];
            adj_to_vertex[start_].push_back(Vertex(end_, succProb[i]));
            adj_to_vertex[end_].push_back(Vertex(start_, succProb[i]));
            ++i;
        }

        while (!vertex_queue.empty()) {
            int current = vertex_queue.back();
            if (current == end)
                return vertex_distance[current];

            for (auto& new_v : adj_to_vertex[current]) {
                if (!vertes_visited[new_v.node]) {
                    double new_weight = vertex_distance[current] * new_v.weight;
                    double old_weight = vertex_distance[new_v.node];
                    if (old_weight < new_weight) {
                        vertex_distance[new_v.node] = new_weight;
                    }
                    resort_queue(new_v.node, vertex_queue, vertex_distance);
                }
            }

            delete_from_queue(current, vertex_queue);
            vertes_visited[current] = true;
        }

        if (vertex_distance[end] < 0)
            return 0;
        else
            return vertex_distance[end];
    }
};

void test_delete() {
    for (int i = 0; i < 5; ++i) {
        list<int> queue;
        for (int j = 0; j < 5; ++j) {
            queue.push_back(j);
        }
        delete_from_queue(i, queue);
    }
}

void test_insert() {
    vector<double> distances({ 1, 3, 7 });
    vector<double> insertion({ 0, 2, 5, 9 });
    vector<double> dist({ 1, 3, 7, 0, 2, 5, 9 });
    for (int i = 0; i < insertion.size(); ++i) {
        list<int> queue;
        for (int j = 0; j < distances.size(); ++j) {
            queue.push_back(j);
        }
        insert_to_queue(distances.size() + i, queue, dist);
    }
}

/*int main() {
    test_delete();
    test_insert();

    vector<vector<int>> edges;

    /*edges.push_back(vector<int>{ 0, 1 });
    edges.push_back(vector<int>{ 1, 2 });
    edges.push_back(vector<int>{ 0, 2 });

    vector<double> succProb{ 0.5,0.5,0.2 };
    int start = 0;
    int end = 2;
    int n = 3;*/

    /*edges.push_back(vector<int>{ 0, 1 });

    vector<double> succProb{ 0.5 };
    int start = 0;
    int end = 2;
    int n = 3;*/

    /*edges.push_back(vector<int>{ 0, 3 });
    edges.push_back(vector<int>{ 1, 7 });
    edges.push_back(vector<int>{ 1, 2 });
    edges.push_back(vector<int>{ 0, 9 });

    vector<double> succProb{ 0.31,0.9,0.86, 0.36 };
    int start = 2;
    int end = 3;
    int n = 10;*/

    /*    edges.push_back(vector<int>{ 1, 4 });
        edges.push_back(vector<int>{ 2, 4 });
        edges.push_back(vector<int>{ 0, 4 });
        edges.push_back(vector<int>{ 0, 3 });
        edges.push_back(vector<int>{ 0, 2 });
        edges.push_back(vector<int>{ 2, 3 });

        vector<double> succProb{ 0.37,0.17,0.93, 0.23, 0.39, 0.04 };
        int start = 3;
        int end = 4;
        int n = 5;

        Solution sol;

        double result = sol.maxProbability(n, edges, succProb, start, end);

        return 0;
    }*/

    //1514