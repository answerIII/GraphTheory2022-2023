#ifndef HANDLER_CLASS
#define HANDLER_CLASS

#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include "StaticGraph.h"
#include "TemporalGraph.h"

class Handler
{
private:
    std::string _dataFilePath;
    
    bool dataReader(std::string fileName, StaticGraph& graph){
        std::ifstream inFile(fileName);
        if(!inFile)
            return 0;

        int vertexCount, x, y, l, t;
        inFile >> vertexCount;
        graph.SetVertex(vertexCount);
    
        while(true){
            inFile >> x >> y >> t >> l;
            if(inFile.eof())
                break;
            graph.Push(x, y);
        }

        inFile.close();
        return 1;
    }

    bool dataReader(std::string fileName, TemporalGraph& graph){
        std::ifstream inFile(fileName);
        if(!inFile)
            return 0;

        int vertexCount, x, y, l, t;
        inFile >> vertexCount;
        graph.SetVertex(vertexCount);
    
        while(true){
            inFile >> x >> y >> l >> t;
            if(inFile.eof())
                break;
            graph.Push(x, y, t);
        }

        inFile.close();
        return 1;
    }

    void staticTaskPrint(StaticGraph& graph, std::string datasetName){
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " |";
        int space = (37 - datasetName.size()) / 2;
        for(int i = 0; i < space + !(datasetName.size() % 2); ++i)
            std::cout << ' ';
        std::cout << datasetName;
        for(int i = 0; i < space; ++i)
            std::cout << ' ';
        std::cout << " |";
        std::cout << '\n';
        std::cout << std::setprecision(3) << std::fixed;
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " |  Vertex count            |  ";
        int vertexCount = graph.GetVertexCount();
        std::cout << vertexCount;
        for(int i = 0; i < 8 - std::log10(vertexCount); ++i)
            std::cout << ' ';
        std::cout << '|' << '\n';
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " |  Edge count              |  ";
        int edgeCount = graph.GetEdgeCount();
        std::cout << edgeCount;
        for(int i = 0; i < 8 - std::log10(edgeCount); ++i)
            std::cout << ' ';
        std::cout << '|' << '\n';
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " |  Density                 |  ";
        std::cout << graph.GetDensity() << "    |" << '\n';
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " |  Weak comp. count        |  ";
        int weakConnCount = graph.GetWeakConnCount();
        std::cout << weakConnCount;
        for(int i = 0; i < 8 - std::log10(weakConnCount); ++i)
            std::cout << ' ';
        std::cout << '|' << '\n';
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " |  Main comp. to graph     |  ";
        std::cout << graph.GetMainCompToFull() << "    |"<< '\n';
        std::cout << " ----------------------------------------" << '\n';

        std::cout << " |  Main component radius   |  ";
        if(graph.GetRadius().second == 0){
            int rad = graph.GetRadius().first;
            std::cout << rad;
            for(int i = 0; i < 8 - std::log10(rad); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " ----------------------------------------" << '\n';
        }
        else{
            std::cout << "Rand: ";
            int rand = graph.GetRadius().first;
            std::cout << rand;
            for(int i = 0; i < 2 - std::log10(rand); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " |  Main component radius   |  ";
            std::cout << "Snow: ";
            int snow = graph.GetRadius().second;
            std::cout << snow;
            for(int i = 0; i < 2 - std::log10(snow); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " ----------------------------------------" << '\n';
        }

        std::cout << " |  Main component diameter |  ";
        if(graph.GetDiameter().second == 0){
            int diam = graph.GetDiameter().first;
            std::cout << diam;
            for(int i = 0; i < 8 - std::log10(diam); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " ----------------------------------------" << '\n';
        }
        else{
            std::cout << "Rand: ";
            int rand = graph.GetDiameter().first;
            std::cout << rand;
            for(int i = 0; i < 2 - std::log10(rand); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " |  Main component diameter |  ";
            std::cout << "Snow: ";
            int snow = graph.GetDiameter().second;
            std::cout << snow;
            for(int i = 0; i < 2 - std::log10(snow); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " ----------------------------------------" << '\n';
        }
        
        std::cout << " |  Main component 90%      |  ";
        if(graph.GetPerc90().second == 0){
            int perc = graph.GetPerc90().first;
            std::cout << perc;
            for(int i = 0; i < 8 - std::log10(perc); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " ----------------------------------------" << '\n';
        }
        else{
            std::cout << "Rand: ";
            int rand = graph.GetPerc90().first;
            std::cout << rand;
            for(int i = 0; i < 2 - std::log10(rand); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " |  Main component 90%      |  ";
            std::cout << "Snow: ";
            int snow = graph.GetPerc90().second;
            std::cout << snow;
            for(int i = 0; i < 2 - std::log10(snow); ++i)
                std::cout << ' ';
            std::cout << '|' << '\n';
            std::cout << " ----------------------------------------" << '\n';
        }

        std::cout << " | Cl koef                  |  ";
        std::cout << graph.GetAvgClCoeff() << "    |"<< '\n';
        std::cout << " ----------------------------------------" << '\n';
        std::cout << " | Assort koef              |  ";
        double assCoeff = graph.GetAssortCoeff();
        std::cout << assCoeff;
        if(assCoeff >= 0)
            std::cout << "    |" << '\n';
        else
            std::cout << "   |" << '\n';
        std::cout << " ----------------------------------------" << '\n';
    }

    void temporalGraphPrint(TemporalGraph& graph){
        graph.GenerateGraphSlice();
        graph.GenerateTrainPairs();
        //graph.CalcStaticFeatures();
        graph.CalcTemporalWeights();
        graph.Aggregate();
        graph.Combine();
        graph.LogisticRegression();
        std::cout << "Static graph features calculated" << '\n';
    }

    void taskMenuPrint(std::string datasetName){
        system("clear");
        std::cout << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << " |";
        int space = (21 - datasetName.size()) / 2;
        for(int i = 0; i < space + !(datasetName.size() % 2); ++i)
            std::cout << ' ';
        std::cout << datasetName;
        for(int i = 0; i < space; ++i)
            std::cout << ' ';
        std::cout << "|" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << " | 1 |   Static task   |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << " | 2 |  Temporal task  |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << '\n'; 
        std::cout << " -----------------------" << '\n';
        std::cout << " | 3 | Go to datasets  |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << " | 0 |  Exit program   |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << "\n Input number: ";
    }

    void datasetNamePrint(std::vector<std::string> datasetName){
        system("clear");
        std::cout << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << " | № |     Dataset     |" << '\n';
        std::cout << " -----------------------" << '\n';
        for(int i = 1; i <= datasetName.size(); ++i){
            std::cout << " | "<< i << " | ";
            std::cout << datasetName[i - 1];
            for(int j = 0; j < 16 - datasetName[i - 1].size(); ++j)
                std::cout << ' ';
            std::cout << "|" << '\n'; 
            std::cout << " -----------------------" << '\n';
        }
        std::cout << '\n'; 
        std::cout << " -----------------------" << '\n';
        std::cout << " | 0 |  exit program   |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << '\n';
        std::cout << " Input number: ";
    }

    void taskExitList(){
        std::cout << '\n'; 
        std::cout << " -----------------------" << '\n';
        std::cout << " | 1 |  go task list   |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << " | 0 |  exit program   |" << '\n';
        std::cout << " -----------------------" << '\n';
        std::cout << '\n';
        std::cout << " Input number: ";
    }

public:
    Handler(std::string filePath) : _dataFilePath(filePath) {}

    int ConsoleHandlerStart(){
        std::ifstream inFile(_dataFilePath);
        if(!inFile)
            return 0;

        std::vector<std::string> datasetPath;
        std::vector<std::string> datasetName;
        std::string str;
        while(true){
            inFile >> str;
            if(inFile.eof())
                break;
            datasetPath.push_back(str);
            inFile >> str;
            datasetName.push_back(str);
        }
        inFile.close();

        char control;
        while(true){
            datasetNamePrint(datasetName);
            std::cin >> control; 
            if(control == '0'){
                system("clear");
                return -1;
            }
            if(control < '0' || control > datasetName.size() + '0')
                continue;

            int controlNum = control - '0' - 1;
            while(true){
                taskMenuPrint(datasetName[controlNum]);
                std::cin >> control; 
                system("clear");
                if(control == '1'){
                    StaticGraph graph;
                    if(!dataReader(datasetPath[controlNum], graph))
                        return 1;
                    staticTaskPrint(graph, datasetName[controlNum]);
                }
                if(control == '2'){
                    TemporalGraph graph;
                    if(!dataReader(datasetPath[controlNum], graph))
                        return 1;
                    std::cout << datasetName[controlNum] << '\n';
                    temporalGraphPrint(graph);
                }
                if(control == '3')
                    break;
                if(control == '0'){
                    system("clear");
                    return -1;
                }
                if(control < '0' || control > '3')
                    continue;

                taskExitList();
                std::cin >> control;
                if(control == '0'){
                    system("clear");
                    return -1;
                }
            }
        }
        return -1;
    }
};

#endif
