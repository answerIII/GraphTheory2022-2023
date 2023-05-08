class Solution {
    bool hasCycleOfLength2 = false;
    vector<int> uv;
    int vertexes;
public:

    int BFS(list<int>* adj, int start_vertex) {
        bool* visited = new bool[vertexes];
        for (int i = 0; i < vertexes; i++)
            visited[i] = false;

        for (int i = 0; i < uv.size(); i++)
            visited[uv[i]] = true;

        std::queue<pair<int, int>> temp_queue;
        //std::vector<pair<int, int>> traverse_v;

        temp_queue.push(make_pair(start_vertex, 1));
        visited[start_vertex] = true;

        int level;
        while (!temp_queue.empty()) {

            int cur_vertex = temp_queue.front().first;
            level = temp_queue.front().second;

            //traverse_v.push_back(make_pair(cur_vertex, level));

            temp_queue.pop();

            for (auto adjacent : adj[cur_vertex]) {
                if (!visited[adjacent]) {
                    visited[adjacent] = true;
                    int next_level = level + 1;
                    temp_queue.push(make_pair(adjacent, next_level));
                }
            }

        }

        // for (int i=0; i < traverse_v.size(); i++)
        //     std::cout << traverse_v[i].first << ":" << traverse_v[i].second << " ";

        // std::cout << std::endl;

        // std::cout << "*level* " << level << std::endl;

        delete[] visited;
        return level;
    }




    void DFS_util(list<int>* adj, int v, bool visited[], int& count)
    {
        visited[v] = true;
        uv.push_back(v);
        //cout << v << " ";
        count++;

        list<int>::iterator i;
        for (i = adj[v].begin(); i != adj[v].end(); ++i)
            if (!visited[*i])
                DFS_util(adj, *i, visited, count);
    }

    //по сути DFS, для сохранения порядка используется stack
    void fillOrder(list<int>* adj, int v, bool visited[], stack<int>& Stack)
    {
        visited[v] = true;

        list<int>::iterator i;
        for (i = adj[v].begin(); i != adj[v].end(); ++i)
            if (!visited[*i])
                fillOrder(adj, *i, visited, Stack);

        Stack.push(v);
    }

    //поиск компонент сильной связности
    int StrongConnectedComponents(list<int>* adj, list<int>* adj_inv)
    {
        stack<int> Stack;
        bool* visited = new bool[vertexes];
        for (int i = 0; i < vertexes; i++)
            visited[i] = false;

        for (int i = 0; i < vertexes; i++)
            if (visited[i] == false)
                fillOrder(adj, i, visited, Stack);

        for (int i = 0; i < vertexes; i++)
            visited[i] = false;

        int max = 0;
        while (Stack.empty() == false)
        {
            int count = 0;
            int v = Stack.top();
            Stack.pop();

            if (visited[v] == false)
            {
                DFS_util(adj_inv, v, visited, count);

                //cout << "count:::" << count << endl;

                if (count > max)
                    max = count;

                if (count == 2) {
                    hasCycleOfLength2 = true;
                }
                else {
                    while (count > 0) {
                        uv.pop_back();
                        count--;
                    }
                }
            }
        }
        delete[] visited;
        return max;
    }



    int maximumInvitations(vector<int>& favorite) {
        int cycleLength = 0;
        vertexes = favorite.size();
        std::list<int>* adjList = new std::list<int>[vertexes];
        std::list<int>* adjList_inverted = new std::list<int>[vertexes];

        for (int i = 0; i < vertexes; i++) {
            adjList[favorite[i]].push_back(i);
            adjList_inverted[i].push_back(favorite[i]);
        }


        // for (int i = 0; i < vertexes; i++) {
        //     std::cout << i << ": ";
        //     for (auto adjacent : adjList[i])
        //         std::cout << adjacent << " ";

        //     std::cout << std::endl;
        // }

        // std::cout << std::endl;

        // for (int i = 0; i < vertexes; i++) {
        //     std::cout << i << ": ";
        //     for (auto adjacent : adjList_inverted[i])
        //         std::cout << adjacent << " ";

        //     std::cout << std::endl;
        // }
        // std::cout << std::endl;

        cycleLength = StrongConnectedComponents(adjList, adjList_inverted);

        // cout << endl;
        // for (auto vertex : uv) {
        //         std::cout << "cycle2 ->" << vertex << "<-  ";
        // }
        // cout << endl;

        if (!hasCycleOfLength2) {
            return cycleLength;
        }
        else {
            int sum = 0;
            for (int i = 0; i < uv.size(); i = i + 2) {
                int max_U = BFS(adjList, uv[i]);
                int max_V = BFS(adjList, uv[i + 1]);
                sum += max_U + max_V;
            }

            int result = sum > cycleLength ? sum : cycleLength;

            return result;
        }

        return 0;

    }
};