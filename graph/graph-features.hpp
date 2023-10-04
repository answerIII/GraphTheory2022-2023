#pragma once

#include "graph.hpp"
#include <cmath>
#include <typeinfo>
#include <vector>
#include <exception>
#include <cmath>
#include <map>

namespace Graph
{

    namespace GraphFeatures
    {
        using FeatureData = double;
        using FeatureVector = std::vector<FeatureData>;

        template<typename ... Args>
        struct Feature
        {
            virtual FeatureData operator()(Args...) const = 0;

            virtual std::string getName() const = 0;
        };

        template<typename ... Args>
        struct GraphFeature: public Feature<Graph&, Args...>
        {
            virtual FeatureData operator()(Graph& graph, Args...) const override = 0;
        };

        template<typename ... Args>
        struct EdgeFeature: public GraphFeature<Edge, Args...>
        {
            virtual FeatureData operator()(Graph& graph, Edge edge, Args...) const override = 0;
        };

        template<typename ... Args>
        struct VertexFeature: public GraphFeature<Vertex, Args...>
        {
            virtual FeatureData operator()(Graph& graph, Vertex vertex, Args...) const override = 0;
        };


        struct CommonNeighbours: public EdgeFeature<>
        {
            FeatureData operator()(Graph& graph, Edge edge) const override
            {
                return graph.getCommonNeighbours(edge).size();
            }

            virtual std::string getName() const override
            {
                return "SCN";
            }
        };  

        struct AdamicAdar: public EdgeFeature<>
        {
            FeatureData operator()(Graph& graph, Edge edge) const override
            {
                FeatureData res = 0.;
                for (Vertex vertex: graph.getCommonNeighbours(edge))
                {
                    size_t neighbours = graph.getNeighborsSize(vertex);
                    if (neighbours < 2)
                    {
                        throw std::string("Edge: " + std::to_string(edge.first) + " " + std::to_string(edge.second));
                    }
                    res += 1. / std::log2(graph.getNeighborsSize(vertex));
                }
                return res;
            }

            virtual std::string getName() const override
            {
                return "SAA";
            }
        };

        struct JaccardCoefficient: public EdgeFeature<>
        {
            FeatureData operator()(Graph& graph, Edge edge) const override
            {
                size_t n_size = graph.getCommonNeighbours(edge).size();
                if (n_size == 0)
                {
                    return 1.;
                }
                return (double) n_size / graph.getUniqueNeighboursSize(edge);
            }

            virtual std::string getName() const override
            {
                return "SJC";
            }
        };

        struct PreferentialAttachment : public EdgeFeature<>
        {
            FeatureData operator()(Graph& graph, Edge edge) const override
            {
                return graph.getNeighborsSize(edge.first) * graph.getNeighborsSize(edge.second);
            }

            virtual std::string getName() const override
            {
                return "SPA";
            }
        };
    
        
        struct Aggregation
        {
            virtual double operator()(const std::vector<double>& weights) const = 0;
            virtual std::string getName() const = 0;
        };

        template<int quantile>
        struct QuantileAggregation: public Aggregation
        {
            virtual double operator()(const std::vector<double>& weights) const override
            {
                return weights[std::min(weights.size() - 1, size_t((double)quantile / 4 * weights.size()))];
            } 
            virtual std::string getName() const override
            {
                return "Q" + std::to_string(quantile);
            }
        };

        struct ZerothQuantileAggregation: public QuantileAggregation<0>{};

        struct FirstQuantileAggregation: public QuantileAggregation<1>{};

        struct SecondQuantileAggregation: public QuantileAggregation<2>{};

        struct ThirdQuantileAggregation: public QuantileAggregation<3>{};

        struct FourthQuantileAggregation: public QuantileAggregation<4>{};

        struct SumAggregation: public Aggregation
        {
            virtual double operator()(const std::vector<double>& weights) const override
            {
                double res = 0.;
                for (auto weight: weights)
                {
                    res += weight;
                }
                return res;
            }
            virtual std::string getName() const override
            {
                return "S";
            }
        };

        struct MeanAggregation: public SumAggregation
        {
            virtual double operator()(const std::vector<double>& weights) const override
            {
                return SumAggregation::operator()(weights) / weights.size();
            }
            virtual std::string getName() const override
            {
                return "M";
            }
        };

        struct VarianceAggregation: public MeanAggregation
        {
            virtual double operator()(const std::vector<double>& weights) const override
            {
                if (weights.size() == 1)
                {
                    return 1.;
                }
                double mean = MeanAggregation::operator()(weights);
                double res = 0.;
                for (double weight: weights)
                {
                    res += (weight - mean) * (weight - mean);
                }

                return res / (weights.size() - 1);
            }
            virtual std::string getName() const override
            {
                return "V";
            }
        };
    

        struct WeightEdge
        {
            virtual double operator()(size_t edge_time, size_t time_min, size_t time_max, double lower_bound) const = 0;
            virtual std::string getName() const = 0;

        protected:
            static double edgeTimeNorm_(size_t edge_time, size_t time_min, size_t time_max)
            {
                return (double)(edge_time - time_min) / (time_max - time_min);
            }
        };

        struct LinearWeightEdge: public WeightEdge
        {
            virtual double operator()(size_t edge_time, size_t time_min, size_t time_max, double lower_bound) const override
            {
                return lower_bound + (1. - lower_bound) * edgeTimeNorm_(edge_time, time_min, time_max);
            }
            virtual std::string getName() const override
            {
                return "LW";
            }
        };

        struct ExponentialWeightEdge: public WeightEdge
        {
            virtual double operator()(size_t edge_time, size_t time_min, size_t time_max, double lower_bound) const override
            {
                return lower_bound + (1. - lower_bound) * (std::exp(3. * edgeTimeNorm_(edge_time, time_min, time_max)) - 1.) / (std::exp(3.) - 1.);
            }
            virtual std::string getName() const override
            {
                return "EW";
            }
        };

        struct SqrtWeightEdge: public WeightEdge
        {
            virtual double operator()(size_t edge_time, size_t time_min, size_t time_max, double lower_bound) const override
            {
                return lower_bound + (1. - lower_bound) * std::sqrt(edgeTimeNorm_(edge_time, time_min, time_max));
            }
            virtual std::string getName() const override
            {
                return "SW";
            }
        };


        template<typename ... Args>
        struct WeightedEdgeFeatures: public EdgeFeature<const std::map<Edge, std::vector<double>>&, size_t, Args ...>
        {
            virtual FeatureData operator()(
                Graph& graph, 
                Edge edge,
                const std::map<Edge, std::vector<double>>& weights,
                size_t weight_index,
                Args ...) const override = 0;

        protected:
            static double getWeight_(const std::map<Edge, std::vector<double>>& weights, Edge edge, size_t weight_index)
            {
                return weights.at(edge)[weight_index];
            }

            static Edge getKeyEdge_(Edge edge)
            {
                return {std::min(edge.first, edge.second), std::max(edge.first, edge.second)};
            }
        };

        struct TemporalCommonNeighbours: public WeightedEdgeFeatures<>
        {
            std::string getName() const override
            {
                return "TCC";
            }

            virtual FeatureData operator()(
                Graph& graph, 
                Edge edge,
                const std::map<Edge, std::vector<double>>& weights,
                size_t weight_index) const override
            {
                edge = getKeyEdge_(edge);
                FeatureData feature_data = 0;

                for (Vertex vertex: graph.getCommonNeighbours(edge))
                {
                    feature_data += 
                        getWeight_(weights, getKeyEdge_({edge.first, vertex}), weight_index) + 
                        getWeight_(weights, getKeyEdge_({edge.second, vertex}), weight_index);
                }
                
                return feature_data;
            }
        };

        struct TemporalAdamicAdar: public WeightedEdgeFeatures<>
        {
            std::string getName() const override
            {
                return "TAA";
            }

            virtual FeatureData operator()(
                Graph& graph, 
                Edge edge,
                const std::map<Edge, std::vector<double>>& weights,
                size_t weight_index) const override
            {
                edge = getKeyEdge_(edge);
                FeatureData feature_data = 0;

                for (Vertex vertex: graph.getCommonNeighbours(edge))
                {
                    double tmp_res = 1.;
                    for (Vertex vertex1: graph.getNeighbors(vertex))
                    {
                        tmp_res += getWeight_(weights, getKeyEdge_({vertex, vertex1}), weight_index);
                    }
                    if (tmp_res == 1.)
                    {
                        feature_data += 1.;
                        continue;
                    }
                    feature_data += 
                        (getWeight_(weights, getKeyEdge_({edge.first, vertex}), weight_index) + 
                        getWeight_(weights, getKeyEdge_({edge.second, vertex}), weight_index)) / std::log2(tmp_res); 
                }

                return feature_data;
            }
        };

        struct TemporalJaccardCoefficient: public WeightedEdgeFeatures<>
        {
            std::string getName() const override
            {
                return "TJC";
            }

            virtual FeatureData operator()(
                Graph& graph, 
                Edge edge,
                const std::map<Edge, std::vector<double>>& weights,
                size_t weight_index) const override
            {
                edge = getKeyEdge_(edge);
                FeatureData feature_data = 0;

                for (Vertex vertex: graph.getCommonNeighbours(edge))
                {
                    double tmp_res = 0.;
                    for (Vertex vertex1: graph.getNeighbors(edge.first))
                    {
                        tmp_res += getWeight_(weights, getKeyEdge_({edge.first, vertex1}), weight_index);
                    }
                    for (Vertex vertex1: graph.getNeighbors(edge.second))
                    {
                        tmp_res += getWeight_(weights, getKeyEdge_({edge.second, vertex1}), weight_index);
                    }
                    if (tmp_res == 0.)
                    {
                        feature_data += 1.;
                        continue;
                    }
                    feature_data += 
                        (getWeight_(weights, getKeyEdge_({edge.first, vertex}), weight_index) + 
                        getWeight_(weights, getKeyEdge_({edge.second, vertex}), weight_index)) / tmp_res;
                }

                return feature_data;
            }
        };

        struct TemporalPreferentialAttachment: public WeightedEdgeFeatures<>
        {
            std::string getName() const override
            {
                return "TPA";
            }

            virtual FeatureData operator()(
                Graph& graph, 
                Edge edge,
                const std::map<Edge, std::vector<double>>& weights,
                size_t weight_index) const override
            {
                edge = getKeyEdge_(edge);
                double tmp_res1 = 0., tmp_res2 = 0.;

                for (Vertex vertex: graph.getNeighbors(edge.first))
                {
                    tmp_res1 += getWeight_(weights, getKeyEdge_({edge.first, vertex}), weight_index);
                }
                for (Vertex vertex: graph.getNeighbors(edge.second))
                {
                    tmp_res2 += getWeight_(weights, getKeyEdge_({edge.second, vertex}), weight_index);
                }

                return tmp_res1 * tmp_res2;
            }
        };
    }
}