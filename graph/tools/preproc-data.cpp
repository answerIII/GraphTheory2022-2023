#include <iomanip>
#include <map>
#include <string>
#include <vector>
#include <set>
#include <filesystem>
#include <fstream>
#include <algorithm>
#include <iomanip>

std::vector<std::string> splitString(const std::string& str)
{
    std::vector<std::string> ans(1);
    for (const char& elem: str)
    {
        if (elem == ' ' || elem == '\t')
        {
            if (!ans.back().empty())
            {
                ans.emplace_back();
            }
            continue;
        }
        ans.back().push_back(elem);
    }
    if (ans.back().empty())
    {
        ans.pop_back();
    }
    return ans;
}

void preprocData_(std::string file_name)
{
    std::filesystem::path row_data_path("D:\\VScodeProjects\\graphTheory\\core2\\row-data\\" + file_name);
    std::filesystem::path data_path("D:\\VScodeProjects\\graphTheory\\core2\\data\\" + file_name);

    std::ifstream in(row_data_path);
    size_t num_vertices, num_edges;
    
    std::map<size_t, size_t> vertices_accord;
    size_t count = 0;
    std::vector<std::vector<size_t>> edges;
    std::string line;
    size_t l1 = 0, l2 = 0, l3 = 0;

    while (std::getline(in, line))
    {
        auto split_string = splitString(line);
        
        size_t v1, v2;
        size_t time;
        if (split_string.size() == 0)
        {
            continue;
        }
        if (split_string.size() < 3)
        {
            throw std::exception();
        }
        if (split_string.size() == 3)
        {
            v1 = std::stoull(split_string[0]);
            v2 = std::stoull(split_string[1]);
            time = std::stoull(split_string[2]);
        }
        else
        {
            v1 = std::stoull(split_string[0]);
            v2 = std::stoull(split_string[1]);
            time = std::stoull(split_string[3]);
        }
        if (time == 0. || v1 == v2)
        {
            continue;
        }
        if (vertices_accord.find(v1) == vertices_accord.end())
        {
            vertices_accord[v1] = count++;
        }
        if (vertices_accord.find(v2) == vertices_accord.end())
        {
            vertices_accord[v2] = count++;
        }
        if (vertices_accord[v1] > vertices_accord[v2])
        {
            std::swap(v1, v2);
        }
        l1 = std::max(l1, std::to_string(v1).size());
        l2 = std::max(l2, std::to_string(v2).size());
        l3 = std::max(l3, std::to_string(time).size());
        edges.push_back({vertices_accord[v1], vertices_accord[v2], time});
    }

    in.close();

    std::sort(edges.begin(), edges.end(), [](std::vector<size_t>& a, std::vector<size_t>& b)
    {
        if (a[0] == b[0])
        {
            if (a[1] == b[1])
            {
                return a[2] <= b[2];
            }
            return a[1] <= b[1];
        }
        return a[0] <= b[0];
    });

    std::ofstream out(data_path);
    out << std::fixed;

    for (auto& edge: edges)
    {
        out << edge[0] << std::setw(l2 + 4) << edge[1] << std::setw(l3 + 4) << edge[2] << '\n';
    }

    out.close();
}

int main(int argc, char* argv[])
{
    preprocData_(argv[1]);
}