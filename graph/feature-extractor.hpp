#pragma once

#include "graph-features.hpp"
#include "graph.hpp"
#include "graph-reader.hpp"
#include "tools/benchmark.hpp"
#include <vector>
#include <random>
#include <filesystem>
#include <typeinfo>
#include <sstream>
#include <map>
#include <set>
#include <map>
#include <iomanip>


namespace Graph::GraphFeatures
{

    template<typename ... Args>
    class FeatureExtractor
    {
    public:
        FeatureExtractor(std::filesystem::path graph_path, std::vector<EdgeFeature<Args...>*> features): 
            features_(features),
            graph_data_(GraphReader::readGraphData(graph_path)),
            graph_(graph_data_) {}

        virtual std::vector<FeatureVector> operator()(
            size_t time_init,
            size_t time_predict,
            size_t max_edges) = 0;

        virtual std::vector<FeatureVector> operator()(
            double part_time,
            size_t max_edges) = 0;

        virtual std::vector<std::string> getFeatureNames() const
        {
            std::vector<std::string> ans(features_.size());
            for (size_t i = 0; i < ans.size(); ++i)
            {
                ans[i] = features_[i]->getName();
            }
            return ans;
        }

        virtual ~FeatureExtractor()
        {
            for (size_t i = 0; i < features_.size(); ++i)
            {
                delete features_[i];
            }
        }

    protected:
        virtual std::vector<FeatureVector> extractFeatures_(const std::vector<Edge>& edges, Args ... args)
        {
            std::vector<FeatureVector> res;
            LoopProgress progress(edges.size(), "Extracting...", true);
            Benchmark bench;
            std::map<std::string, std::chrono::nanoseconds> times;
            std::stringstream ss;

            for (auto& edge: edges)
            {
                res.emplace_back();
                for (const EdgeFeature<Args...>* feature: features_)
                {
                    bench.startTimer();
                    res.back().emplace_back((*feature)(graph_, edge, args...));
                    times[feature->getName()] += bench.getPassedTime();
                    ss << "|" << feature->getName() << ": " <<
                        std::setw(3) << std::chrono::duration_cast<std::chrono::seconds>(times[feature->getName()]).count() << "s.| ";
                }

                progress.update(ss.str());
                ss.str("");
            }

            return res;
        }

        std::set<Edge> extractNotAppearEdges_(const std::vector<Vertex>& vertices, const std::set<Edge>& appear_edges)
        {
            std::random_device rd;
            std::mt19937 gen(rd());

            std::set<Edge> edges;
            LoopProgress progress(vertices.size(), "Extract near edges");

            for (Vertex vertex: vertices)
            {
                std::vector<Vertex> suspects = graph_.getVerticesInDistance2(vertex);
                if (suspects.size() > vertices.size())
                {
                    std::shuffle(suspects.begin(), suspects.end(), gen);
                    suspects.resize(vertices.size());
                }
                for (Vertex suspect: suspects)
                {
                    Edge edge = {std::min(vertex, suspect), std::max(vertex, suspect)};
                    if (appear_edges.find(edge) == appear_edges.end())
                    {
                        edges.insert(edge);
                    }
                }
                progress.update(std::string("---- Num near edges: ") + std::to_string(edges.size()));
            }

            return edges;
        }

        void normalisation_(std::vector<FeatureVector>& features)
        {
            std::vector<std::pair<FeatureData, FeatureData>> bounds(features[0].size());
            for (size_t i = 0; i < features[0].size(); ++i)
            {
                bounds[i] = {features[0][i], features[0][i]};
            }
            for (size_t i = 1; i < features.size(); ++i)
            {
                for (size_t j = 0; j < features[i].size(); ++j)
                {
                    bounds[j].first = std::min(bounds[j].first, features[i][j]);
                    bounds[j].second = std::max(bounds[j].second, features[i][j]);
                }
            }
            for (size_t i = 0; i < features.size(); ++i)
            {
                for (size_t j = 0; j < features[i].size(); ++j)
                {
                    features[i][j] = (features[i][j] - bounds[j].first);
                    if (bounds[j].second - bounds[j].first > 1e-6)
                    {
                        features[i][j] /= (bounds[j].second - bounds[j].first);
                    }
                }
            }
        }

        std::pair<std::vector<Edge>, std::vector<Edge>> extractEdges_(size_t time_init, size_t time_predict, size_t max_edges)
        {
            std::random_device rd;
            std::mt19937 gen(rd());

            std::vector<Edge> appear_edges_v;
            std::set<Edge> appear_edges_s;

            for (auto& edge: graph_data_.edges_)
            {
                if (edge.time_ > time_init && edge.time_ <= time_predict)
                {
                    Edge edge1 = {std::min(edge.vertex1_, edge.vertex2_), std::max(edge.vertex1_, edge.vertex2_)};
                    appear_edges_s.insert(edge1);
                }
            }

            LoopProgress apear_edges_progress(appear_edges_s.size(), "Appear edges search");

            for (auto& edge: appear_edges_s)
            {
                if (graph_.getCommonNeighbours(edge).size() > 0 && !graph_.isExist(edge))
                {
                    appear_edges_v.emplace_back(edge);
                }
                apear_edges_progress.update("---- Appear edges size: " + std::to_string(appear_edges_v.size()));
            }

            std::vector<Vertex> random_subgraph = graph_.getRandomSubgraph((size_t)std::sqrt(max_edges) * 10ULL);
            std::set<Edge> near_edges = extractNotAppearEdges_(random_subgraph, appear_edges_s);
            LoopProgress not_appear_edges_progress(appear_edges_v.size(), "Not appear edges search");

            for (auto& edge: appear_edges_v)
            {
                if (near_edges.find(edge) != near_edges.end())
                {
                    near_edges.erase(near_edges.find(edge));
                }
                not_appear_edges_progress.update("---- Not appear edges size: " +  std::to_string(near_edges.size()));
            }

            std::vector<Edge> not_appear_edges_v(near_edges.begin(), near_edges.end());
            max_edges = std::min(max_edges, std::min(appear_edges_v.size(), not_appear_edges_v.size()));

            if (appear_edges_v.size() > max_edges)
            {
                std::shuffle(appear_edges_v.begin(), appear_edges_v.end(), gen);
                appear_edges_v.resize(max_edges);
            }

            if (not_appear_edges_v.size() > max_edges)
            {
                std::shuffle(not_appear_edges_v.begin(), not_appear_edges_v.end(), gen);
                not_appear_edges_v.resize(max_edges);
            }

            return {appear_edges_v, not_appear_edges_v};
        }

        std::vector<EdgeFeature<Args ...>*> features_;
        GraphData graph_data_;
        Graph graph_;
    };


    class StaticTopologicalFeaturesExtractor: public FeatureExtractor<>
    {
    public:

        StaticTopologicalFeaturesExtractor(std::filesystem::path graph_path): 
            FeatureExtractor(graph_path, 
            {
                new CommonNeighbours(),
                new AdamicAdar(),
                new JaccardCoefficient(),
                new PreferentialAttachment()
            }) {}

        virtual std::vector<FeatureVector> operator()(size_t time_init, size_t time_predict, size_t max_edges) override
        {
            graph_.setTime(time_init);

            auto[appear_edges, not_appear_edges] = extractEdges_(time_init, time_predict, max_edges);
            
            std::vector<FeatureVector> appear_edge_features = extractFeatures_(appear_edges);
            std::vector<FeatureVector> not_appear_edges_features = extractFeatures_(not_appear_edges);

            std::vector<FeatureVector> features(appear_edge_features.begin(), appear_edge_features.end());
            for (auto& vec: not_appear_edges_features)
            {
                features.emplace_back(vec);
            }

            normalisation_(features);

            for (size_t i = 0; i < appear_edge_features.size(); ++i)
            {
                features[i].emplace_back(1.);
            }
            for (size_t i = appear_edge_features.size(); i < features.size(); ++i)
            {
                features[i].emplace_back(0.);
            }

            return features;
        }

        virtual std::vector<FeatureVector> operator()(double part_time, size_t max_edges) override
        {
            graph_data_.timeSort();
            size_t time_init = graph_data_.edges_[(size_t)(graph_data_.edges_.size()*part_time)].time_;
            size_t time_predict = graph_data_.edges_.back().time_ + 1ULL;

            return (*this)(time_init, time_predict, max_edges);
        }
    };


    class TemporalTopologicalFeaturesExtractor: public FeatureExtractor<const std::map<Edge, std::vector<double>>&, size_t>
    {
    public:
        TemporalTopologicalFeaturesExtractor(std::filesystem::path graph_path): 
            FeatureExtractor(graph_path,
            {
                new TemporalAdamicAdar(),
                new TemporalCommonNeighbours(),
                new TemporalJaccardCoefficient(),
                new TemporalPreferentialAttachment()
            }) {}

        virtual std::vector<std::string> getFeatureNames() const override
        {
            std::vector<std::string> res;
            for (size_t j = 0; j < weighting_.size(); ++j)
            {
                for (size_t k = 0; k < aggregating_.size(); ++k)
                {
                    for (size_t i = 0; i < features_.size(); ++i)
                    {
                        res.emplace_back(features_[i]->getName() + "/" + weighting_[j]->getName() + "/" + aggregating_[k]->getName());
                    }
                }
            }
            return res;
        }

        virtual std::vector<FeatureVector> operator()(size_t time_init, size_t time_predict, size_t max_edges) override
        {
            graph_.setTime(time_init);
            graph_data_.timeSort();
            auto[appear_edges, not_appear_edges] = extractEdges_(time_init, time_predict, max_edges);
            
            size_t time_min = graph_data_.edges_[0].time_;
            size_t time_max = time_init;
            double lower_bound = 0.2;
            std::vector<std::pair<Edge, size_t>> edges;

            for (EdgeTime edge: graph_data_.edges_)
            {
                if (edge.time_ <= time_init)
                {
                    edges.push_back({{std::min(edge.vertex1_, edge.vertex2_), std::max(edge.vertex1_, edge.vertex2_)}, edge.time_});
                }
            }

            std::vector<FeatureVector> appear_edge_features(appear_edges.size());
            std::vector<FeatureVector> not_appear_edges_features(not_appear_edges.size());

            std::map<Edge, std::vector<double>> weights = getWeights_(edges, time_min, time_max, lower_bound);
            LoopProgress progress(weighting_.size() * aggregating_.size(), "Feature extracting");

            for (size_t k = 0; k < weighting_.size() * aggregating_.size(); ++k)
            {
                auto appear_temp = extractFeatures_(appear_edges, weights, k);
                auto not_appear_temp = extractFeatures_(not_appear_edges, weights, k);
                for (size_t i = 0; i < appear_temp.size(); ++i)
                {
                    for (size_t j = 0; j < features_.size(); ++j)
                    {
                        appear_edge_features[i].emplace_back(appear_temp[i][j]);
                        not_appear_edges_features[i].emplace_back(not_appear_temp[i][j]);
                    }
                }
                progress.update();
            }

            std::vector<FeatureVector> features(appear_edge_features);
            for (auto& vec: not_appear_edges_features)
            {
                features.emplace_back(vec);
            }

            normalisation_(features);

            for (size_t i = 0; i < appear_edge_features.size(); ++i)
            {
                features[i].emplace_back(1.);
            }
            for (size_t i = appear_edge_features.size(); i < features.size(); ++i)
            {
                features[i].emplace_back(0.);
            }

            return features;
        }

        virtual std::vector<FeatureVector> operator()(double part_time, size_t max_edges) override
        {
            graph_data_.timeSort();
            size_t time_init = graph_data_.edges_[(size_t)(graph_data_.edges_.size()*part_time)].time_;
            size_t time_predict = graph_data_.edges_.back().time_ + 1ULL;

            return (*this)(time_init, time_predict, max_edges);
        }

        ~TemporalTopologicalFeaturesExtractor()
        {
            for (size_t i = 0; i < weighting_.size(); ++i)
            {
                delete weighting_[i];
            }
            for (size_t i = 0; i < aggregating_.size(); ++i)
            {
                delete aggregating_[i];
            }
        }

    protected:
        std::map<Edge, std::vector<double>> getWeights_(
            const std::vector<std::pair<Edge, size_t>>& edges,
            size_t time_min,
            size_t time_max,
            double lower_bound)
        {
            std::map<Edge, std::vector<std::vector<double>>> tmp;
            LoopProgress weighting(edges.size(), "Weighting");

            for (auto[edge, time]: edges)
            {
                if (tmp.find(edge) == tmp.end())
                {
                    tmp[edge] = std::vector<std::vector<double>>(weighting_.size());
                }
                std::vector<std::vector<double>>& weights = tmp[edge];
                for (size_t i = 0; i < weighting_.size(); ++i)
                {
                    weights[i].emplace_back((*weighting_[i])(time, time_min, time_max, lower_bound));
                }
                weighting.update();
            }
            std::map<Edge, std::vector<double>> res;
            LoopProgress aggregating(tmp.size(), "Aggregating");

            for (auto[edge, data]: tmp)
            {
                std::vector<double>& weights = res[edge] = {};
                for (size_t i = 0; i < weighting_.size(); ++i)
                {
                    for (size_t j = 0; j < aggregating_.size(); ++j)
                    {
                        weights.emplace_back((*aggregating_[j])(data[i]));
                    }
                }
                aggregating.update();
            }

            return res;
        }


        std::vector<WeightEdge*> weighting_ = 
        {
            new LinearWeightEdge(), 
            new ExponentialWeightEdge(), 
            new SqrtWeightEdge()
        };

        std::vector<Aggregation*> aggregating_ = 
        {
            new ZerothQuantileAggregation(), 
            new FirstQuantileAggregation(),
            new SecondQuantileAggregation(),
            new ThirdQuantileAggregation(),
            new FourthQuantileAggregation(),
            new SumAggregation(),
            new MeanAggregation(),
            new VarianceAggregation()
        };
    };
}