// #define DEBUG

#include "feature-extractor.hpp"
#include "graph.hpp"
#include "tools/csv.hpp"
#include <string>
#include <filesystem>
#include <fstream>
#include <exception>
#include <iomanip>

int main(int argc, char* argv[])
/*
    graph path (path),
    max edges (size_t),
    part edges (double [0, 1]),
    out (path)
*/
{
    try
    {
        #ifdef DEBUG

            std::cout << "## DEBUG ## \n\n";

            argc = 5;
            std::filesystem::path graph_path("D:\\VScodeProjects\\graphTheory\\core2\\data\\dnc-corecipient.txt");
            size_t max_edges = std::stoull("20000");
            double part_edges = std::stod("0.666");
            std::ofstream out("D:\\VScodeProjects\\graphTheory\\core2\\features\\TEST.csv");
        #else
            if (argc != 5)
            {
                return 1;
            }
            
            std::filesystem::path graph_path(argv[1]);
            size_t max_edges = std::stoull(argv[2]);
            double part_edges = std::stod(argv[3]);
            std::ofstream out(argv[4]);
        #endif

            if (!out.is_open())
            {
                throw std::string("out is not open");
            }

            Graph::GraphFeatures::StaticTopologicalFeaturesExtractor extractor(graph_path);

            auto data = extractor(part_edges, max_edges);
            auto columns_name = extractor.getFeatureNames();
            columns_name.emplace_back("predict");
            
            std::cout.flush();

            toCSV(columns_name, data, out);

            return 0;
    }
    catch(std::string str)
    {
        std::cout << str << '\n';
        return 2;
    }
    catch(std::exception& ex)
    {
        std::cout << ex.what() << '\n';
        return 3;
    }
    catch(...)
    {
        std::cout << "error 4";
        return 4;
    }
}