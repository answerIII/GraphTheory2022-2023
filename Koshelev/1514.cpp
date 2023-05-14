class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start, int end) {
       vector<vector<pair<int, double>>> adjacency_matrix(n);
        for (int i = 0; i < edges.size(); i++)
        {
            adjacency_matrix[edges[i][0]].push_back(make_pair(edges[i][1], succProb[i]));
            adjacency_matrix[edges[i][1]].push_back(make_pair(edges[i][0], succProb[i]));
        }
        priority_queue<pair<double, int>> pq;
        pq.push(make_pair(1, start));
        vector<pair<double, bool>> nodes(n, make_pair(0, false));
        nodes[start].first = 1;
        while (!pq.empty())
        {
            double prob = pq.top().first;
            int currentNode = pq.top().second;
            pq.pop();
            if (prob != nodes[currentNode].first)
                continue;
            nodes[currentNode].second = true;
            for (int j = 0; j < adjacency_matrix[currentNode].size(); j++)
            {
                if (nodes[currentNode].first * adjacency_matrix[currentNode][j].second > nodes[adjacency_matrix[currentNode][j].first].first
                    && !nodes[adjacency_matrix[currentNode][j].first].second)
                {
                    nodes[adjacency_matrix[currentNode][j].first].first = nodes[currentNode].first * adjacency_matrix[currentNode][j].second;
                    pq.push(make_pair(nodes[adjacency_matrix[currentNode][j].first].first, adjacency_matrix[currentNode][j].first));
                }

            }
        }
        return nodes[end].first;
        
    }
};