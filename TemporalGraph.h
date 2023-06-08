#ifndef TEMPORAL_GRAPH_CLASS
#define TEMPORAL_GRAPH_CLASS

#include <cmath>
#include <cstdlib>
#include <iterator>
#include <map>
#include <unordered_set>
#include <utility>
#include <vector>
#include <set>
#include <climits>
#include <algorithm>
#include <iostream>
#include <mlpack.hpp>

typedef double (*comb)(double, double);
typedef double (*agg)(std::vector<double>&);

class TemporalGraph
{
private:
    const int PAIR_NUM = 10000;
    const double L = 0.2;
    const double E3M1 = 19.0855369232;
    int _tMin = INT_MAX;
    int _tMax = 0;

    std::vector<std::set<int>> _staticGraph;
    std::map<std::pair<int, int>, std::set<int>> _temporalGraph;
    
    std::map<std::pair<int,int>, std::vector<int>> _staticFeatures; 
 
    std::map<std::pair<int,int>, std::set<int>> _trainingGraph;
    std::vector<std::set<int>> _trainingStaticGraph;

    std::vector<std::pair<int,int>> _trainPairs;
    std::map<std::pair<int, int>, int> _yTrainPairs; // 75% and 25%
    std::map<std::pair<int,int>, int> _yTestPairs;

    //for training pairs
    std::map<std::pair<int,int>, std::vector<std::vector<double>>> _weightedEgde;
    std::map<int, std::vector<double>> _aggregatedVertex;
    std::map<std::pair<int,int>, std::vector<double>> _combinedEdge;

    static double q0(std::vector<double>& vec){
        return vec[0];
    }

    static double q1(std::vector<double>& vec){
        return vec[std::floor(vec.size() * 1/4.)];
    }

    static double q2(std::vector<double>& vec){
        return vec[std::floor(vec.size() * 2/4.)];
    }

    static double q3(std::vector<double>& vec){
        return vec[std::floor(vec.size() * 3/4.)];
    }

    static double q4(std::vector<double>& vec){
        return vec[vec.size() - 1];
    }

    static double sum(std::vector<double>& vec){
        double sum = 0.0;
        for (int i = 0; i < vec.size(); ++i)
            sum += vec[i];
        return sum;
    }

    static double mean(std::vector<double>& vec){
        return sum(vec) / vec.size(); 
    }

    static double dsum(double x, double y){
        return x + y;
    }

    static double abs_diff(double x, double y){
        return fabs(x - y);
    } 

    static double dmax(double x, double y){
        return std::max(x,y);
    }

    static double dmin(double x, double y){
        return std::min(x,y);
    } 

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
            _temporalGraph[edge].insert(t);   
        }
    }

    void SetVertex(int n){
        _staticGraph.resize(n+1);
        _trainingStaticGraph.resize(n+1);
    }

    void GenerateGraphSlice(){
        int tmax = 2/3. * _tMax + 1/3. * _tMin;
        for(const auto& [uv, timestamps]: _temporalGraph){
            for(auto time: timestamps){
                if (time < tmax){
                    _trainingGraph[uv].insert(time);
                    _trainingStaticGraph[uv.first].insert(uv.second);
                }
                else 
                    break;
            } 
        } 
    }

    void GenerateTrainPairs(){
        int t = PAIR_NUM, f = PAIR_NUM;
        srand(time(NULL));
        while(true){
            if (t < 1 && f < 1)
                break;
            int randVertex = rand() % (_trainingStaticGraph.size() - 1) + 1;
            for (int v1: _trainingStaticGraph[randVertex]){
                if (t < 1 && f < 1)
                    break;
                for(int v2: _trainingStaticGraph[randVertex]){
                    if (t < 1 && f < 1)
                        break;
                    if (v2 > v1){
                        if (!_trainingStaticGraph[v1].contains(v2)){
                            _trainPairs.push_back({v1,v2});
                            if (_staticGraph[v1].contains(v2)){
                                if (t > 0){
                                    std::pair<int,int> uv(v1,v2);
                                    _yTrainPairs[uv] = 1;
                                    --t;
                                }
                            }
                            else{
                                if (f > 0){
                                    std::pair<int, int> uv(v1,v2);
                                    _yTrainPairs[uv] = 0;
                                    --f;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    /*void CalcStaticFeatures(){
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
                                      std::back_inserter(intersect));
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
    }*/

    void CalcTemporalWeights(){ 
        for (const auto& [uv, timestamps]: _temporalGraph){
            for (auto t: timestamps){
                double tminmax = (t - _tMin)/(double)(_tMax - _tMin);
                std::vector<double> w;
                w.push_back(L + (1 - L)*tminmax);
                w.push_back(L + (1 - L)*(exp(3*tminmax-1)/E3M1));
                w.push_back(L + (1 - L)*sqrt(tminmax));
                _weightedEgde[uv].push_back(w);
            }
        }
    }

    void Aggregate(){
        std::vector<agg> funcs = {q0, q1, q2, q3, q4, sum, mean};
        for(int u = 1; u < _trainingStaticGraph.size(); ++u){
            if (_trainingStaticGraph[u].size() > 0){
                std::vector<double> w1,w2,w3;
                for(auto v: _trainingStaticGraph[u]){
                    std::pair<int, int> uv(u,v);
                    for (int i = 0; i < _weightedEgde[uv].size(); ++i){
                        w1.push_back(_weightedEgde[uv][i][0]);
                        w2.push_back(_weightedEgde[uv][i][1]);
                        w3.push_back(_weightedEgde[uv][i][2]);
                    }
                }
                std::vector<std::vector<double>> w = {w1,w2,w3};
                _aggregatedVertex[u].resize(21);
                for (int j = 0; j < 7; ++j)
                    for (int k = 0; k < 3; ++k)
                        _aggregatedVertex[u][3 * j + k] = funcs[j](w[k]);  
            }
        }
    }

    void Combine(){
        std::vector<comb> funcs = {dsum, abs_diff, dmin, dmax};
        for (int u = 1; u < _trainingStaticGraph.size()-1; ++u){
            for (int v = u + 1; v < _trainingStaticGraph.size(); ++v){
                if (_aggregatedVertex[u].size() > 0 && 
                    _aggregatedVertex[v].size() > 0){
                    std::pair<int, int> uv(u,v);
                    _combinedEdge[uv].resize(84);
                    for(int i = 0; i < 21; ++i)
                        for(int j = 0; j < 4; ++j)
                            _combinedEdge[uv][4 * i + j] = funcs[j](_aggregatedVertex[u][i],
                                                                _aggregatedVertex[v][i]);
                            
                }
            }
        }
    }

    void MakeTestPairs(){
        // divide yTrainPairs to yTrainPairs and yTestPairs
        int c = _yTrainPairs.size() / 4;
        srand(time(NULL));
        for (const auto& [uv, tf]: _yTrainPairs){
            if (c < 0)
                break;
            if (rand() % 4 == 0) {
                _yTestPairs[uv] = tf;
                --c;
            }
        }
        for (const auto& [uv, _]: _yTestPairs){
            _yTrainPairs.erase(uv);
        }
    }

    void LogisticRegression(){
        arma::mat X(84, _yTrainPairs.size());
        arma::Row<size_t> y(_yTrainPairs.size());
        int counter = 1;

        for (const auto& [uv, tf]: _yTrainPairs){
            if (_combinedEdge[uv].size() == 84){
                arma::vec xi(_combinedEdge[uv]); // +15 social credits
                X.insert_cols(counter, xi);
                y.insert_cols(counter, tf);
                ++counter;
            }
        }
        X.resize(84, counter);
        y.resize(counter);

        mlpack::regression::LogisticRegression logReg;
        logReg.Train(X, y);
    }
};

#endif
