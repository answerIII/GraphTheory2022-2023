#pragma once

#include <vector>
#include <string>
#include <fstream>
#include <iomanip>


void toCSV(const std::vector<std::string>& columns_name, const std::vector<std::vector<double>>& data, std::ofstream& out)
{
    if (data.size() == 0 || columns_name.size() != data[0].size())
    {
        throw std::exception();
    }

    out << std::fixed << std::setprecision(5);

    for (size_t i = 0; i < columns_name.size() - 1; ++i)
    {
        out << columns_name[i] << ",";
    }
    out << columns_name.back() << '\n';

    for (size_t i = 0; i < data.size(); ++i)
    {
        for (size_t j = 0; j < data[i].size() - 1; ++j)
        {
            out << data[i][j] << ",";
        }
        out << data[i].back() << '\n';
    }
}