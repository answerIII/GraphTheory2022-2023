#ifndef TEMPORAL_GRAPH_CLASS
#define TEMPORAL_GRAPH_CLASS

#include <map>
#include <unordered_set>
#include <utility>
#include <vector>
#include <set>
#include <climits>
#include <algorithm>
//#include "mlpack.hpp"

class TemporalGraph
{
private:
    int _tMin = INT_MAX;
    int _tMax = 0;

    std::map<std::pair<int, int>, std::vector<int>> _temporalGraph;
    std::map<std::pair<int,int>, std::vector<std::vector<double>>> _featureGraph;
    std::vector<std::set<int>> _staticGraph;

public: 
    void Push(int x, int y, int t){
        if (x != y){
            _staticGraph[x].insert(y);
            _staticGraph[y].insert(x);

            if (t < _tMin)
                _tMin = t;
            if (t > _tMax)
                _tMax = t;
            std::pair<int, int> edge(x,y);
            _temporalGraph[edge].push_back(t);
            int i = _temporalGraph[edge].size() - 2;
            while(i > 0 && _temporalGraph[edge][i] > t){
                std::swap(_temporalGraph[edge][i], _temporalGraph[edge][i+1]);
                --i;
            }   
        }
    }

    void SetVertex(int n){
        _staticGraph.resize(n+1);
    }

    void CalcStaticFeatures(){
        double unionUV = 0, intersectUV = 0, nu = 0, nv = 0, aa;
        for (int u = 1; u < _staticGraph.size(); ++u){
            for (int v: _staticGraph[u]){
                std::pair uv(u,v);
                if (_featureGraph[uv].size() == 0){
                    aa = 0.0;
                    nu = _staticGraph[u].size();
                    nv = _staticGraph[v].size();
                    std::vector<int> intersect;
                    std::set_intersection(_staticGraph[u].begin(),
                                      _staticGraph[u].end(),
                                      _staticGraph[v].begin(),
                                      _staticGraph[v].end(),
                                      intersect.begin());
                    for (int i = 0; i < intersect.size(); ++i)
                        aa += 1.0 / log10(_staticGraph[intersect[i]].size());
                    intersectUV = intersect.size();
                    unionUV = nu + nv - intersectUV; 
                    std::vector<double> features;
                    features.push_back(intersectUV);
                    features.push_back(aa);
                    features.push_back(intersectUV / unionUV);
                    features.push_back(nu * nv);
                    _featureGraph[uv].push_back(features);
                }
            }
        }
    }

    void CalcTemporalFeatures(){
        double l = 0.2;
        const double e3m1 = 19.0855369232;
        for(const auto& [uv, timestamp]: _temporalGraph){ 
            for (int i = 0; i < timestamp.size(); ++i){
                double t = timestamp[i];
                double tminmax = (t - _tMin)/(_tMax - _tMin);
                std::vector<double> w;
                w.push_back(l + (1 - l)*tminmax);
                w.push_back(l + (1 - l)*(exp(3*tminmax-1)/e3m1));
                w.push_back(l + (1 - l)*sqrt(tminmax));
                _featureGraph[uv].push_back(w);
            }
        }
    }
};

#endif
