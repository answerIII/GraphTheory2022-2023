#ifndef STATIC_GRAPH_CLASS
#define STATIC_GRAPH_CLASS

#include <vector>
#include <unordered_set>
#include <queue>


class StaticGraph
{
private:
    int _vertexCount = 0;
    int _edgeCount = 0;
    int _mainCompCount = 0;
    std::vector<std::unordered_set<int>> _staticGraph;
    std::vector<std::vector<int>> _weakComponents;

    std::pair<int,int> _mainRadius;
    std::pair<int,int> _mainDiameter;
    std::pair<int,int> _mainPerc90;

    void weakConnCalc(){
        if (_weakComponents.size() == 0){
            int n = GetVertexCount();
            std::vector<bool> visited(n+1);
            std::queue<int> bfs;
            int comp = 0;
            for(int i = 1; i <= n; ++i){
                if (!visited[i]){
                    bfs.push(i);
                    _weakComponents.push_back({i});
                    visited[i] = true;
                    while(!bfs.empty()){
                        int front = bfs.front();
                        bfs.pop();
                        for (auto v: _staticGraph[front]){
                            if (!visited[v]){
                                bfs.push(v);
                                _weakComponents[comp].push_back(v);
                                visited[v] = true;
                            }
                        }
                    }
                    ++comp;
                }
            } 
        }
    }

    int perc(std::vector<int>& vec, int p){
        //TODO
        return 0;
    }

    void calcRadDimPerc90(std::vector<std::vector<int>>& adj, int type){
        int n = adj.size();
        for (int k = 0; k < n; ++k)
            for (int i = 0; i < n; ++i)
                for (int j = 0; j < n; ++j)
                    adj[i][j] = std::min(adj[i][j], adj[i][k] + adj[k][j]);
        int rad = INT_MAX, dim = 0, perc90 = 0, max = 0;
        std::vector<int> dist;
        for(int i = 0; i < n; ++i){
            max = 0;
            for(int j = 0; j < n; ++j){
                if (adj[i][j] != INT_MAX){
                    if (adj[i][j] > max)
                        max = adj[i][j];
                    dist.push_back(adj[i][j]);
                }   
            }
            if (max != 0){
                if (max < rad)
                    rad = max;
                if (max > dim)
                    dim = max;
            }
        }
        perc90 = perc(dist, 90);
        if (type == 0){
            _mainRadius.first = rad;
            _mainDiameter.first = dim;
            _mainPerc90.first = perc90;
        }
        else{
            _mainRadius.second = rad;
            _mainDiameter.second = dim;
            _mainPerc90.second = perc90;
        }
    }

    void handleRadDimPerc90(){
        int n = GetVertexCount();
        if (n > 500){
            std::vector<std::vector<int>> rand = randGraph();
            calcRadDimPerc90(rand, 0);
            std::vector<std::vector<int>> snow = snowGraph();
            calcRadDimPerc90(snow, 1);
        }
        else{
            std::vector<std::vector<int>> adj = adjGraph();
            calcRadDimPerc90(adj, 0);
        }
    }

    std::vector<std::vector<int>> adjGraph(){
        return {{0}};
    }

    std::vector<std::vector<int>> randGraph(){
        return {{0}};
    }

    std::vector<std::vector<int>> snowGraph(){
        return {{0}};
    }

public:  
    void SetVertex(int n){
        _staticGraph.resize(n+1); 
    }

    void Push(int x, int y){
        if (x != y) {
            _staticGraph[x].insert(y);
            _staticGraph[y].insert(x);
        }
    }

    int GetVertexCount(){
        return _staticGraph.size() - 1;
    }

    int GetEdgeCount(){
        if (_edgeCount == 0){
            for (auto v: _staticGraph)
                _edgeCount += v.size();
        }
        return _edgeCount / 2;
    }

    double GetDensity(){
        return (double)GetEdgeCount() / ((GetVertexCount() * (GetVertexCount() - 1)) / 2);
    }

    int GetWeakConnCount(){
        if (_weakComponents.size() == 0)
            weakConnCalc();
        return _weakComponents.size();
    }

    double GetMainCompToFull(){
        if (_weakComponents.size() == 0)
            weakConnCalc();
        int max = 0;
        for (int i = 0; i < _weakComponents.size(); ++i)
            if (_weakComponents[i].size() > max)
                max = _weakComponents[i].size();
        return (double)max / GetVertexCount();
    }

    int GetRadius(){
        if (_weakComponents.size() == 0)
            return 0;
        return 0;
    }
};

#endif
