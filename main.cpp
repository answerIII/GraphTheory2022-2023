#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_set>
#include <queue>

class StaticGraph
{
private:
    int _vertexCount = 0;
    int _edgeCount = 0;
    int _mainCompCount = 0;
    std::vector<std::unordered_set<int>> _staticGraph;
    std::vector<std::vector<int>> _weakComponents;
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

    int GetVertexCount(){
        return _staticGraph.size() - 1;
    }

    int GetEdgeCount(){
        if (_edgeCount == 0){
            for (auto v: _staticGraph)
                _edgeCount += v.size();
        }
        return _edgeCount / 2;
    }

    double GetDensity(){
        return (double)GetEdgeCount() / ((GetVertexCount() * (GetVertexCount() - 1)) / 2);
    }

    int GetWeakConnCount(){
        int n = GetVertexCount();
        std::vector<bool> visited(n+1);
        std::queue<int> bfs;
        int comp = 0;
        for(int i = 1; i <= n; ++i){
            if (!visited[i]){
                bfs.push(i);
                _weakComponents.push_back({i});
                visited[i] = true;
                while(!bfs.empty()){
                    int front = bfs.front();
                    bfs.pop();
                    for (auto v: _staticGraph[front]){
                        if (!visited[v]){
                            bfs.push(v);
                            _weakComponents[comp].push_back(v);
                            visited[v] = true;
                        }
                    }
                }
                ++comp;
            }
        }
        return comp;
    }

    double GetMainCompToFull(){
        int max = 0;
        for (int i = 0; i < _weakComponents.size(); ++i)
            if (_weakComponents[i].size() > max)
                max = _weakComponents[i].size();
        return (double)max / GetVertexCount();
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

void StaticTaskPrint(StaticGraph graph)
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
}

void TaskMenuPrint()
{
    std::cout << "1) Static task" << '\n';
    std::cout << "2) Temporal task" << '\n';
    std::cout << '\n' << "0) go back" << '\n';
    std::cout << "Input number: ";
}

void DatasetNamePrint(std::vector<std::string> datasetName)
{
    std::cout << "Choose dataset:" << '\n';
    for(int i = 1; i <= datasetName.size(); ++i)
        std::cout << i << ") " << datasetName[i - 1] << '\n';
    std::cout << '\n' << "0) exit program" << '\n';
    std::cout << "Input number: ";
}

int Handler(std::string dataFile)
{
    std::ifstream inFile(dataFile);
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
        system("clear");
        DatasetNamePrint(datasetName);
        std::cin >> control; 

        if(control == '0')
            return 1;
        if(control < '0' || control > '9')
            continue;

        int controlNum = control - '0' - 1;
        while(true)
        {
            system("clear");
            std::cout << datasetName[controlNum] << '\n';
            TaskMenuPrint();
            std::cin >> control; 
            system("clear");

            if(control == '0')
                break;
            if(control < '0' || control > '2')
                continue;

            if(control == '1'){
                StaticGraph graph;
                if(!DataReader(datasetPath[controlNum], graph))
                    return 2;
                std::cout << datasetName[controlNum] << '\n';
                StaticTaskPrint(graph);
            }

            if(control == '2'){
                std::cout << "no stuff here yet :)" << '\n';
            }

            std::cout << '\n' << "0) go back" << '\n';
            std::cout << "Input number: ";
            std::cin >> control;
        }
    }

    return 1;
}

int main()
{
    std::string dataFile = "datafile.txt";

    int status = Handler(dataFile);

    if(status == 0)
        std::cout << "Wrong file with datasets info!" << '\n';

    if(status == 2)
        std::cout << "Error reading dataset file!" << '\n';

    return 0;
}
