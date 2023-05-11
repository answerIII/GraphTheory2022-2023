#include <vector>
#include <deque>
#include <iostream>
using namespace std;

class Solution {
public:
    int minCost(vector<vector<int>>& grid) {
        deque<pair<int, int>> deq;
        vector < vector <int> > min_dist(grid.size(), vector <int>(grid[0].size(), 10000));
        deq.push_back({ 0,0 });
        min_dist[0][0] = 0;
        while (!deq.empty()) {
            pair<int, int> tmp = deq.front();
            deq.pop_front();
            if (tmp.first == grid.size() - 1 && tmp.second == grid[0].size() - 1) {
                return min_dist[tmp.first][tmp.second];
            }

            if (tmp.second + 1 < grid[0].size()) {  // Право
                int ooone = 1;
                if (grid[tmp.first][tmp.second] == 1)
                    ooone = 0;
                if (min_dist[tmp.first][tmp.second + 1] > min_dist[tmp.first][tmp.second] + ooone) {
                    min_dist[tmp.first][tmp.second + 1] = min_dist[tmp.first][tmp.second] + ooone;
                    if (ooone == 0)
                        deq.push_front({ tmp.first ,tmp.second + 1 });
                    else
                        deq.push_back({ tmp.first ,tmp.second + 1 });
                }
            }

            if (tmp.second - 1 < grid[0].size()) { // Лево
                int ooone = 1;
                if (grid[tmp.first][tmp.second] == 2)
                    ooone = 0;
                if (min_dist[tmp.first][tmp.second - 1] > min_dist[tmp.first][tmp.second] + ooone) {
                    min_dist[tmp.first][tmp.second - 1] = min_dist[tmp.first][tmp.second] + ooone;
                    if (ooone == 0)
                        deq.push_front({ tmp.first ,tmp.second - 1 });
                    else
                        deq.push_back({ tmp.first ,tmp.second - 1 });
                }
            }

            if (tmp.first + 1 < grid.size()) { // Низ
                int ooone = 1;
                if (grid[tmp.first][tmp.second] == 3)
                    ooone = 0;
                if (min_dist[tmp.first + 1][tmp.second] > min_dist[tmp.first][tmp.second] + ooone) {
                    min_dist[tmp.first + 1][tmp.second] = min_dist[tmp.first][tmp.second] + ooone;
                    if (ooone == 0)
                        deq.push_front({ tmp.first + 1 ,tmp.second });
                    else
                        deq.push_back({ tmp.first + 1 ,tmp.second });
                }
            }

            if (tmp.first - 1 < grid.size()) { // Низ
                int ooone = 1;
                if (grid[tmp.first][tmp.second] == 4)
                    ooone = 0;
                if (min_dist[tmp.first - 1][tmp.second] > min_dist[tmp.first][tmp.second] + ooone) {
                    min_dist[tmp.first - 1][tmp.second] = min_dist[tmp.first][tmp.second] + ooone;
                    if (ooone == 0)
                        deq.push_front({ tmp.first - 1 ,tmp.second });
                    else
                        deq.push_back({ tmp.first - 1 ,tmp.second });
                }
            }
        }
        return 0;
    }
};