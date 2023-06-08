#include <iostream>
#include "include/Handler.h"

int main()
{
    std::string dataFilePath = "datafile.txt";

    Handler mainHandler(dataFilePath);

    int status = mainHandler.ConsoleHandlerStart();

    if(status == 0)
        std::cout << "Wrong file with datasets info!" << '\n';

    if(status == 1)
        std::cout << "Error reading dataset file!" << '\n';

    return 0;
}
