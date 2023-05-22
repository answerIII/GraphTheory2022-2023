#include <iostream>
#include <fstream>
#include <unordered_set>

class StaticGraph
{
private: 
    std::vector<std::unordered_set<int>> _staticGraph;
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
};

bool DataReader(std::string fileName, StaticGraph& graph){
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

int main()
{
    std::string fileName = "datasets/radoslaw_email.tsv";
    StaticGraph graph;
    DataReader(fileName, graph); 
    return 0;
}
