#ifndef STATIC_GRAPH_CLASS
#define STATIC_GRAPH_CLASS

#include <vector>
#include <unordered_set>
#include <queue>
#include <climits>
#include <algorithm>
#include <cmath>

class StaticGraph
{
private:
    int _vertexCount = 0;
    int _edgeCount = 0;
    int _mainCompCount = 0;
    int _mainCompIdx = 0;
    double _clCoeff = -1.0;
    double _assortCoeff = -1.0;
    std::vector<std::unordered_set<int>> _staticGraph;
    std::vector<std::vector<int>> _weakComponents;

    std::pair<int,int> _mainRadius;
    std::pair<int,int> _mainDiameter;
    std::pair<int,int> _mainPerc90;

    
    int perc(std::vector<int>& vec, int p){
        if (p < 100){
            std::sort(vec.begin(), vec.end());
            return vec[std::floor(vec.size() * p / 100.0)];
        }
        return -1;
    }

    void weakConnCalc(){
        if (_weakComponents.size() == 0 && _mainCompCount == 0){
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
            for (int i = 0; i < _weakComponents.size(); ++i)
                if (_weakComponents[i].size() > _mainCompCount){
                    _mainCompCount = _weakComponents[i].size();
                    _mainCompIdx = i;
                }
        }
    } 

    void calcRadDimPerc90(std::vector<std::vector<int>>& adj, int type){
        int n = adj.size();
        for (int k = 0; k < n; ++k)
            for (int i = 0; i < n; ++i)
                for (int j = 0; j < n; ++j)
                    adj[i][j] = std::min(adj[i][j], adj[i][k] + adj[k][j]);
        int rad = INT_MAX / 2 - 1, dim = 0, perc90 = 0, max = 0;
        std::vector<int> dist;
        for(int i = 0; i < n; ++i){
            max = 0;
            for(int j = 0; j < n; ++j){
                if (adj[i][j] != INT_MAX / 2 - 1){
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
            std::vector<std::vector<int>> randAdj;
            randGraph(randAdj);
            calcRadDimPerc90(randAdj, 0);
            std::vector<std::vector<int>> snowAdj;
            snowGraph(snowAdj);
            calcRadDimPerc90(snowAdj, 1);
        }
        else{
            std::vector<std::vector<int>> adj; 
            adjGraph(adj);
            calcRadDimPerc90(adj, 0);
        }
    }

    void adjGraph(std::vector<std::vector<int>>& adj){
        int maxCompIdx = 0;
        int maxCompSize = 0;
        for(int i = 0; i < _weakComponents.size(); ++i){ 
            if(_weakComponents[i].size() > maxCompSize){
                maxCompIdx = i;
                maxCompSize = _weakComponents[i].size();
            }
        }

        for(int i = 0; i < maxCompSize; ++i){
            std::vector<int> maxIntVec(maxCompSize, INT_MAX / 2 - 1); 
            adj.push_back(maxIntVec);
        }

        for(int i = 0; i < maxCompSize; ++i)
            for(auto v: _staticGraph[_weakComponents[maxCompIdx][i]])
                adj[_weakComponents[maxCompIdx][i] - 1][v - 1] = 1;
    }

    void randGraph(std::vector<std::vector<int>>& adj){
        int size = 500; 
        for(int i = 0; i < size; ++i){
            std::vector<int> maxIntVec(size, INT_MAX / 2 - 1); 
            adj.push_back(maxIntVec);
        }

        int maxCompIdx = 0;
        int maxCompSize = 0;
        for(int i = 0; i < _weakComponents.size(); ++i){ 
            if(_weakComponents[i].size() > maxCompSize){
                maxCompIdx = i;
                maxCompSize = _weakComponents[i].size();
            }
        }

        int randNum;
        srand(time(NULL));
        std::vector<int> randomVertex;
        std::vector<int> component(_weakComponents[maxCompIdx]);
        for(int i = 0; i < size; ++i){
            randNum = rand() % (component.size() - 1); 
            randomVertex.push_back(component[randNum]);
            component.erase(component.begin() + randNum);
        }

        for(int i = 0; i < size; ++i){
            for(int j = 0; j < size; ++j){
                if(auto v =_staticGraph[randomVertex[i]].find(randomVertex[j]); 
                        v != _staticGraph[randomVertex[i]].end())
                    adj[i][j] = 1;
            }
        }

    }

    void snowGraph(std::vector<std::vector<int>>& adj){
        //to do
        adj = {{0}};
    }

    bool isExistEdge(int x, int y){
        std::unordered_set<int>::const_iterator exist = _staticGraph[x].find(y);
        if (exist == _staticGraph[x].end())
            return false;
        return true;
    }

    void calcClCoeff(){
        if (_mainCompCount != 0 && _clCoeff == -1.0){
            double clu = 0.0;
            int ncount = 0;
            int v = 0;
            _clCoeff = 0.0;
            for(int i = 0; i < _weakComponents[_mainCompIdx].size(); ++i){
                ncount = 0;
                v = _weakComponents[_mainCompIdx][i];
                if (_staticGraph[v].size() >= 2){
                    for(auto v1: _staticGraph[v])
                        for(auto v2: _staticGraph[v])
                            if (v1 != v2 && isExistEdge(v1, v2))
                                ++ncount;
                    clu = (double)ncount / 
                        (_staticGraph[v].size() * (_staticGraph[v].size() - 1));
                }
                _clCoeff += clu;
            }
            _clCoeff /= _mainCompCount; 
        }
    }
    
    void calcAssortCoeff(){
        if (_mainCompCount != 0 && _assortCoeff == -1.0){
            double r1 = 0.0, r2 = 0.0, r3 = 0.0, re = 0.0;
            int v = 0;
            int ncount = 0, ncount2 = 0;
            double num = 0.0, denum = 0.0;
            for(int i = 0; i < _weakComponents[_mainCompIdx].size(); ++i){
                v = _weakComponents[_mainCompIdx][i];
                for(auto v1: _staticGraph[v]){
                    re += _staticGraph[i].size() * _staticGraph[v1].size();
                }
                ncount = _staticGraph[v].size(); 
                ncount2 = ncount * ncount;
                r1 += ncount;
                r2 += ncount2;
                r3 += ncount2 * ncount;
            } 
            re /= 2;
            _assortCoeff = (re*r1 - r2*r2)/(r3*r1 - r2*r2);
        }
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
        return (double)GetEdgeCount() / 
            ((GetVertexCount() * (GetVertexCount() - 1)) / 2);
    }

    int GetWeakConnCount(){
        if (_weakComponents.size() == 0)
            weakConnCalc();
        return _weakComponents.size();
    }

    double GetMainCompToFull(){
        if (_weakComponents.size() == 0)
            weakConnCalc();
        return (double)_mainCompCount / GetVertexCount();
    }

    std::pair<int,int> GetRadius(){
        if (_mainRadius.first == 0)
            handleRadDimPerc90();
        return {_mainRadius.first, _mainRadius.second};
    }

    std::pair<int,int> GetDiameter(){
        if (_mainDiameter.first == 0)
            handleRadDimPerc90();
        return {_mainDiameter.first, _mainDiameter.second};
    }

    std::pair<int, int> GetPerc90(){
        if (_mainPerc90.first == 0)
            handleRadDimPerc90();
        return {_mainPerc90.first, _mainPerc90.second};
    }

    double GetAvgClCoeff(){
        if (_mainCompCount == 0)
            weakConnCalc();
        if (_clCoeff == -1.0)
            calcClCoeff();
        return _clCoeff;
    }

    double GetAssortCoeff(){
        if (_mainCompCount == 0)
            weakConnCalc();
        if(_assortCoeff == -1.0)
            calcAssortCoeff();
        return _assortCoeff;
    }
};

#endif
