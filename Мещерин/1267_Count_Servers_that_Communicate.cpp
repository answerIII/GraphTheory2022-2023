/*
3 компонента очереди:
    0: 2 направления поиска
    1: поиск по горизонтали
    2: поиск по вертикали
*/

class Solution {
private:
    unsigned foo(vector<vector<int>>& grid, const unsigned& x, const unsigned& y)
    {
        queue<array<unsigned, 3>> q;
        q.push({ x, y, 0 });
        grid[x][y] = 0;
        unsigned countOfServers = 1;
        while (!q.empty())
        {
            array<unsigned, 3> sup = q.front();
            switch (sup[2])
            {
            case 0:
            {
                for (unsigned i = 0; i < grid[0].size(); ++i)
                {
                    if (grid[sup[0]][i] == 1) {
                        q.push({sup[0], i, 2 });
                        grid[sup[0]][i] = 0;
                        countOfServers += 1;
                    }
                }
                for (unsigned i = 0; i < grid.size(); ++i)
                {
                    if (grid[i][sup[1]] == 1) {
                        q.push({ i, sup[1], 1 });
                        grid[i][sup[1]] = 0;
                        countOfServers += 1;
                    }
                }
                break;
            }
            case 1:
            {
                for (unsigned i = 0; i < grid[0].size(); ++i)
                {
                    if (grid[sup[0]][i] == 1) {
                        q.push({sup[0], i, 2});
                        grid[sup[0]][i] = 0;
                        countOfServers += 1;
                    }
                }
                break;
            }
            case 2:
            {
                for (unsigned i = 0; i < grid.size(); ++i)
                {
                    if (grid[i][sup[1]] == 1) {
                        q.push({ i, sup[1], 1});
                        grid[i][sup[1]] = 0;
                        countOfServers += 1;
                    }
                }
                break;
            }
            }
            q.pop();
        }
        return (countOfServers == 1) ? 0 : countOfServers;
    }
public:
    int countServers(vector<vector<int>>& grid) {
        int result = 0;
        for(unsigned i = 0; i < grid.size(); ++i)
        {
            for(unsigned j = 0; j < grid[0].size(); ++j)
            {
                if(grid[i][j])
                {
                result += foo(grid, i, j);
                if (i < grid.size() - 1)
                    {
                        j = 0;
                        ++i;
                    }
                    else {
                        return result;
                    }
                }
            }
        }
        return result;
    }
};
