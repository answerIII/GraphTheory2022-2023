class Solution {
public:
    double maxProbability(int n, vector<vector<int>>& edges, vector<double>& succProb, int start, int end) {
        
        vector<pair<int, double>> wList[n];
        vector<double> distProb(n);
        
        for(unsigned i = 0; i < edges.size(); ++i)
        {
          vector<int> edge = edges[i];
          wList[edge[0]].push_back(make_pair(edge[1], succProb[i]));
          wList[edge[1]].push_back(make_pair(edge[0], succProb[i]));
        }

        priority_queue <pair<double, int>> pq;
        pq.push(make_pair(1., start));
        distProb[start] = 1.;
        
        while(!pq.empty())
        {
          pair<double, int> top = pq.top();
          pq.pop();

          for(pair<int, double> i : wList[top.second])
          {
              if(i.second * top.first > distProb[i.first])
              {
                distProb[i.first] = i.second * top.first;
                pq.push({distProb[i.first], i.first});
              }
          }
        }
        
        return distProb[end];
    }
};
