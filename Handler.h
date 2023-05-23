#ifndef HANDLER
#define HANDLER

#include <iostream>
#include <fstream>
#include "StaticGraph.h"

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

    void staticTaskPrint(StaticGraph graph)
    {
        std::cout << "Vertex count: ";
        std::cout << graph.GetVertexCount() << '\n';
        std::cout << "Edge count: ";
        std::cout << graph.GetEdgeCount() << '\n';
        std::cout << "Density: ";
        std::cout << graph.GetDensity() << '\n';
        std::cout << "Weak count: ";
        std::cout << graph.GetWeakConnCount() << '\n';
        std::cout << "Main comp to full graph: ";
        std::cout << graph.GetMainCompToFull() << '\n';

        std::cout << "Main component radius: ";
        if(graph.GetRadius().second == 0) 
            std::cout << graph.GetRadius().first << '\n';
        else{
            std::cout << '\n' << '\t' << "Random: " << graph.GetRadius().first << '\n';
            std::cout << '\t' << "Snowball: " << graph.GetRadius().second << '\n';
        }

        std::cout << "Main component diameter: ";
        if(graph.GetDiameter().second == 0) 
            std::cout << graph.GetDiameter().first << '\n';
        else{
            std::cout << '\n' << '\t' << "Random: " << graph.GetDiameter().first << '\n';
            std::cout << '\t' << "Snowball: " << graph.GetDiameter().second << '\n';
        }
        
        std::cout << "Main component perc90: ";
        if(graph.GetPerc90().second == 0) 
            std::cout << graph.GetPerc90().first << '\n';
        else{
            std::cout << '\n' << '\t' << "Random: " << graph.GetPerc90().first << '\n';
            std::cout << '\t' << "Snowball: " << graph.GetPerc90().second << '\n';
        }

        std::cout << "Cl koef: ";
        std::cout << graph.GetAvgClCoeff() << '\n';
        std::cout << "Assort koef: ";
        std::cout << graph.GetAssortCoeff() << '\n';
    }

    void taskMenuPrint(std::string datasetName)
    {
        system("clear");
        std::cout << datasetName << '\n';
        std::cout << "1) Static task" << '\n';
        std::cout << "2) Temporal task" << '\n';
        std::cout << '\n' << "3) go to dataset list" << '\n';
        std::cout << "4) exit program" << '\n';
        std::cout << "Input number: ";
    }

    void datasetNamePrint(std::vector<std::string> datasetName)
    {
        system("clear");
        std::cout << "Choose dataset:" << '\n';
        for(int i = 1; i <= datasetName.size(); ++i)
            std::cout << i << ") " << datasetName[i - 1] << '\n';
        std::cout << '\n' << "0) exit program" << '\n';
        std::cout << "Input number: ";
    }

    void taskExitList()
    {
        std::cout << '\n' << "1) go task list" << '\n';
        std::cout << "2) exit program" << '\n';
        std::cout << "Input number: ";
    }

public:
    Handler(std::string filePath) : _dataFilePath(filePath) {}

    int ConsoleHandlerStart()
    {
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
                    std::cout << datasetName[controlNum] << '\n';
                    staticTaskPrint(graph);
                }
                if(control == '2'){
                    std::cout << "no stuff here yet :)" << '\n';
                }
                if(control == '3')
                    break;
                if(control == '4'){
                    system("clear");
                    return -1;
                }
                if(control < '0' || control > '4')
                    continue;

                taskExitList();
                std::cin >> control;
                if(control == '2'){
                    system("clear");
                    return -1;
                }
            }
        }
        return -1;
    }
};

#endif
