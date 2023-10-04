#pragma once

#include "graph.hpp"
#include "fstream"
#include "tools/benchmark.hpp"
#include <filesystem>
#include <set>
#include <vector>
#include <functional>

namespace Graph
{
    class GraphReader
    {
    public:
        static GraphData readGraphData(std::filesystem::path file_path)
        {
            GraphData graph_data;
            unsigned int num_vertices = 0;

            std::function edge_invoke = [&graph_data, &num_vertices](Vertex v1, Vertex v2, size_t time)
            {
                graph_data.edges_.emplace_back(v1, v2, time);
                num_vertices = std::max(num_vertices, std::max(v1, v2));
            };
            readGraphData_(file_path, edge_invoke);

            for (unsigned int i = 0; i <= num_vertices; ++i)
            {
                graph_data.vertices_.emplace_back(i);
            }

            return graph_data;
        }

        // static Graph readGraph(std::filesystem::path file_path)
        // {
        //     return Graph(readGraphData(file_path));
        // }

        // static std::set<std::pair<unsigned int, unsigned int>> readEdgesSet(std::filesystem::path file_path, double time_init, double time_predict)
        // {
        //     std::set<std::pair<unsigned int, unsigned int>> edges;
        //     std::function edge_invoke = [&edges, &time_init, &time_predict](unsigned int v1, unsigned int v2, double, double time)
        //     {
        //         if ((time_init == -1. || time >= time_init) && (time_predict == -1. || time < time_predict))
        //         {
        //             edges.insert(Graph::keyPair_({v1, v2}));
        //         }
        //     };
        //     readGraphData_(file_path, edge_invoke);
        //     return edges;
        // }

        // static std::vector<std::pair<unsigned int, unsigned int>> readEdgesVector(std::filesystem::path file_path, double time_init, double time_predict)
        // {
        //     std::vector<std::pair<unsigned int, unsigned int>> edges;
        //     std::function edge_invoke = [&edges, &time_init, &time_predict](unsigned int v1, unsigned int v2, double, double time)
        //     {
        //         if ((time_init == -1. || time >= time_init) && (time_predict == -1. || time < time_predict))
        //         {
        //             edges.emplace_back(Graph::keyPair_({v1, v2}));
        //         }
        //     };
        //     readGraphData_(file_path, edge_invoke);
        //     return edges;
        // }

        // static std::vector<double> getAllTimes(std::filesystem::path file_path)
        // {
        //     std::vector<double> times;
        //     std::function edge_invoke = [&times](unsigned int, unsigned int, double, double time){times.emplace_back(time);};
        //     readGraphData_(file_path, edge_invoke);
        //     std::sort(times.begin(), times.end());
        //     return times;
        // }

    private:
        static void readGraphData_(std::filesystem::path file_path, 
            std::function<void(Vertex, Vertex, size_t)> edge_invoke)
        {
            std::ifstream in(file_path);

            if (!in.is_open())
            {
                throw std::string("file not found");
            }

            Vertex v1, v2;
            size_t time;

            while (in >> v1 >> v2 >> time)
            {
                edge_invoke(v1, v2, time);
            }
        }
    };
}