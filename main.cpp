#include <iostream>
#include <fstream>

class StaticGraph
{
    public:
    void SetVertex(int n)
    {
        return;
    }
    void Push(int x, int y)
    {
        return;
    }
};

bool DataReader(std::string fileName, StaticGraph graph){
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
