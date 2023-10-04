// #define DEBUG

#include "graph.hpp"
#include "graph-reader.hpp"
#include "tools/csv.hpp"
#include <filesystem>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>


int main(int argc, char* argv[])
{
    std::string str_graph_path;
    std::string str_out_path;
    std::ofstream out;

    #ifdef DEBUG
        str_graph_path = "../data/radoslaw_email_email.txt";
        str_out_path = "DEBUG_log.csv";
    #else
        str_graph_path = argv[1];
        str_out_path = argv[2];
    #endif

    out.open(str_out_path);

    std::vector<std::vector<double>> res(1);
    std::vector<std::string> column_names;

    std::filesystem::path graph_path(str_graph_path);

    Graph::Graph graph(Graph::GraphReader::readGraphData(graph_path));
    graph.setTime(ULLONG_MAX);

    res[0].emplace_back(graph.getNumVertices());
    res[0].emplace_back(graph.getNumEdges());
    res[0].emplace_back(graph.getDensity());

    column_names.emplace_back("NumVerts");
    column_names.emplace_back("NumEdges");
    column_names.emplace_back("GrDens");

    std::vector<std::vector<Graph::Vertex>> components = graph.getWeakComponents();
    size_t max_graph_id = 0;
    for (size_t i = 1; i < components.size(); ++i)
    {
        if (components[i].size() > components[max_graph_id].size())
        {
            max_graph_id = i;
        }
    }

    Graph::Graph max_component = graph.extractSubgraph(components[max_graph_id]);
    
    res[0].emplace_back(components.size());
    res[0].emplace_back((double)max_component.getNumVertices() / graph.getNumVertices());
    res[0].emplace_back(max_component.getNumVertices());
    res[0].emplace_back(max_component.getNumEdges());
    res[0].emplace_back(max_component.getDensity());

    column_names.emplace_back("NumComp");
    column_names.emplace_back("MC_ShareVerts");
    column_names.emplace_back("MC_NumVerts");
    column_names.emplace_back("MC_NumEdges");
    column_names.emplace_back("MC_GrDens");
    
    std::vector<Graph::Vertex> random_subgraph = max_component.getRandomSubgraph(500);
    std::vector<Graph::Vertex> snowball_subgraph = max_component.getSnowballSubgraph(500);

    std::vector<size_t> static_data_rand = max_component.getStaticData(random_subgraph);
    std::vector<size_t> static_data_snow = max_component.getStaticData(snowball_subgraph);
    
    if (max_component.getNumVertices() < 4000 && max_component.getNumEdges() * max_component.getNumVertices() < 10'000'000)
    {
        res[0].emplace_back(max_component.getRadius());
    }
    else
    {
        res[0].emplace_back(-1.);
    }
    res[0].emplace_back(static_data_rand[0]);
    res[0].emplace_back(static_data_snow[0]);

    column_names.emplace_back("MC_Rad");
    column_names.emplace_back("MC_RS_Rad");
    column_names.emplace_back("MC_SS_Rad");
    
    if (max_component.getNumVertices() < 4000 && max_component.getNumEdges() * max_component.getNumVertices() < 10'000'000)
    {
        res[0].emplace_back(max_component.getDiameter());
    }
    else
    {
        res[0].emplace_back(-1.);
    }
    res[0].emplace_back(static_data_rand[1]);
    res[0].emplace_back(static_data_snow[1]);

    column_names.emplace_back("MC_Diam");
    column_names.emplace_back("MC_RS_Diam");
    column_names.emplace_back("MC_SS_Diam");

    if (max_component.getNumVertices() < 4000 && max_component.getNumEdges() * max_component.getNumVertices() < 10'000'000)
    {
       res[0].emplace_back(max_component.getPercentile(90));
    }
    else
    {
        res[0].emplace_back(-1.);
    }
    res[0].emplace_back(static_data_rand[2]);
    res[0].emplace_back(static_data_snow[2]);

    column_names.emplace_back("MC_90P");
    column_names.emplace_back("MC_RS_90P");
    column_names.emplace_back("MC_SS_90P");
    
    if (max_component.getR2() < 10'000'000)
    {
        res[0].emplace_back(max_component.getClusteringCoefficient());
    }
    else
    {
        res[0].emplace_back(-1.);
    }
    res[0].emplace_back(max_component.getClusteringCoefficient(random_subgraph));
    res[0].emplace_back(max_component.getClusteringCoefficient(snowball_subgraph));

    column_names.emplace_back("MC_CC");
    column_names.emplace_back("MC_RS_CC");
    column_names.emplace_back("MC_SS_CC");

    res[0].emplace_back(max_component.getPearsonsCoefficient());
    column_names.emplace_back("MC_PC");

    toCSV(column_names, res, out);
}