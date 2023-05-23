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
        return (double)GetEdgeCount() / ((GetVertexCount() * 
                                            (GetVertexCount() - 1)) / 2);
    }

    int GetWeakConnCount(){
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
        return comp;
    }

    double GetMainCompToFull(){
        int max = 0;
        for (int i = 0; i < _weakComponents.size(); ++i)
            if (_weakComponents[i].size() > max)
                max = _weakComponents[i].size();
        return (double)max / GetVertexCount();
    }    
};

#endif
