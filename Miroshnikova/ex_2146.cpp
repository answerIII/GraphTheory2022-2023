#include <vector>
#include <queue>

using namespace std;

struct Pair {
    int i;
    int j;
};

struct Item {
    Pair pricing;
    Pair position;
    int price;
    int distance;
};

class Item_ {
    int price;
    int distance;
    Pair position;

public:
    Item_(int price, int distance, Pair position) : price(price), distance(distance), position(position) {}
    Item_() {}

    bool operator < (const Item_& item) const {
        /*if (distance != item.distance) {
            return (distance < item.distance);
        }
        if (price != item.price) {
            return (price < item.price);
        }
        if (position.i != item.position.i) {
            return (position.i < item.position.i);
        }
        if (position.j != item.position.j) {
            return(position.j < item.position.j);
        }
        return true;*/
        if (distance == item.distance) {
            if (price == item.price) {
                if (position.i == item.position.i) {
                    return position.j > item.position.j;
                }
                return position.i > item.position.i;
            }
            return price > item.price;
        }
        return distance > item.distance;
    }
};



// ?? проверить правильность очереди: порядок + вне диапазона 
class CompareRank
{
public:

    bool operator() (Item a, Item b)
    {
        // товар вне рамок цены
    /*    if (((a.price > a.pricing.j) || (a.price < a.pricing.i)) && ((b.price >= b.pricing.i) || (b.price <= b.pricing.j)))
            return true;
        else if (((b.price > b.pricing.j) || (b.price < b.pricing.i)) && ((a.price >= a.pricing.i) || (a.price <= a.pricing.j)))
            return false;
        else if (((a.price > a.pricing.j) || (a.price < a.pricing.i)) && ((b.price > b.pricing.j) || (b.price < b.pricing.i)))
            return true;
    */

    // товар в рамках цены
        if (a.distance == b.distance) {
            if (a.price == b.price) {
                if (a.position.i == b.position.i) {
                    return a.position.j > b.position.j;
                }
                return a.position.i > b.position.i;
            }
            return a.price > b.price;
        }
        return a.distance > b.distance;
    }
};

const int FROM_UP = 1;
const int FROM_DOWN = 2;
const int FROM_LEFT = 3;
const int FROM_RIGHT = 4;
const int FROM_NONE = 5;
const int NOT_VISITED = 0;

const int WALL = 0;

vector<vector<int>> BFS(vector<vector<int>>& grid, vector<int>& pricing, vector<int>& start, int k) {
    priority_queue<Item, vector<Item>, CompareRank> bfs_queue;

    Pair pricing_ = Pair({ pricing[0], pricing[1] });
    Pair position = Pair({ start[0], start[1] });
    bfs_queue.push(Item({ pricing_, position, grid[start[0]][start[1]], 0 }));
    int m = grid.size();
    int n = grid[0].size();

    // таблица с флагом посещенности вершин, хранит НАПРАВЛЕНИЕ
    vector<vector<int>> visited;
    for (int i = 0; i < m; ++i) {
        visited.push_back(vector<int>());
        for (int j = 0; j < n; ++j) {
            visited[i].push_back(NOT_VISITED);
        }
    }
    visited[start[0]][start[1]] = FROM_NONE;

    // заготовка для ответа;
    vector<vector<int>> result;

    // расстояние для BFS
    int next_distance = 1;
    int current_distance = 0;
    Item node;

    while (!bfs_queue.empty()) {
        node = bfs_queue.top();
        bfs_queue.pop();

        // уже перешли на новый уровень
        if (node.distance != current_distance) {
            current_distance = node.distance;
            next_distance++;
        }

        int idx = node.position.i;
        int jdx = node.position.j;

        // это в диапазоне или нет, если да - добавить к ответу, чекнуть заполнение
        if ((node.price >= pricing[0]) && (node.price <= pricing[1])) {
            result.push_back(vector<int>({ idx, jdx }));
            if (result.size() == k)
                return result;
        }

        // всех соседей добавить в очередь
        int side = visited[idx][jdx];

        if (side == FROM_UP) {
            if ((idx < m - 1) && (grid[idx + 1][jdx] != WALL) && (visited[idx + 1][jdx] == NOT_VISITED)) {
                visited[idx + 1][jdx] = FROM_UP;
                bfs_queue.push(Item({ pricing_, Pair({idx + 1, jdx}), grid[idx + 1][jdx], next_distance }));
            }
            if ((jdx < n - 1) && (grid[idx][jdx + 1] != WALL) && (visited[idx][jdx + 1] == NOT_VISITED)) {
                visited[idx][jdx + 1] = FROM_LEFT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx + 1}), grid[idx][jdx + 1], next_distance }));
            }
            if ((jdx > 0) && (grid[idx][jdx - 1] != WALL) && (visited[idx][jdx - 1] == NOT_VISITED)) {
                visited[idx][jdx - 1] = FROM_RIGHT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx - 1}), grid[idx][jdx - 1], next_distance }));
            }
        }
        else if (side == FROM_DOWN) {
            if ((jdx < n - 1) && (grid[idx][jdx + 1] != WALL) && (visited[idx][jdx + 1] == NOT_VISITED)) {
                visited[idx][jdx + 1] = FROM_LEFT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx + 1}), grid[idx][jdx + 1], next_distance }));
            }
            if ((idx > 0) && (grid[idx - 1][jdx] != WALL) && (visited[idx - 1][jdx] == NOT_VISITED)) {
                visited[idx - 1][jdx] = FROM_DOWN;
                bfs_queue.push(Item({ pricing_, Pair({idx - 1, jdx}), grid[idx - 1][jdx], next_distance }));
            }
            if ((jdx > 0) && (grid[idx][jdx - 1] != WALL) && (visited[idx][jdx - 1] == NOT_VISITED)) {
                visited[idx][jdx - 1] = FROM_RIGHT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx - 1}), grid[idx][jdx - 1], next_distance }));
            }
        }
        else if (side == FROM_LEFT) {
            if ((idx < m - 1) && (grid[idx + 1][jdx] != WALL) && (visited[idx + 1][jdx] == NOT_VISITED)) {
                visited[idx + 1][jdx] = FROM_UP;
                bfs_queue.push(Item({ pricing_, Pair({idx + 1, jdx}), grid[idx + 1][jdx], next_distance }));
            }
            if ((jdx < n - 1) && (grid[idx][jdx + 1] != WALL) && (visited[idx][jdx + 1] == NOT_VISITED)) {
                visited[idx][jdx + 1] = FROM_LEFT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx + 1}), grid[idx][jdx + 1], next_distance }));
            }
            if ((idx > 0) && (grid[idx - 1][jdx] != WALL) && (visited[idx - 1][jdx] == NOT_VISITED)) {
                visited[idx - 1][jdx] = FROM_DOWN;
                bfs_queue.push(Item({ pricing_, Pair({idx - 1, jdx}), grid[idx - 1][jdx], next_distance }));
            }
        }
        else if (side == FROM_RIGHT) {
            if ((idx < m - 1) && (grid[idx + 1][jdx] != WALL) && (visited[idx + 1][jdx] == NOT_VISITED)) {
                visited[idx + 1][jdx] = FROM_UP;
                bfs_queue.push(Item({ pricing_, Pair({idx + 1, jdx}), grid[idx + 1][jdx], next_distance }));
            }
            if ((idx > 0) && (grid[idx - 1][jdx] != WALL) && (visited[idx - 1][jdx] == NOT_VISITED)) {
                visited[idx - 1][jdx] = FROM_DOWN;
                bfs_queue.push(Item({ pricing_, Pair({idx - 1, jdx}), grid[idx - 1][jdx], next_distance }));
            }
            if ((jdx > 0) && (grid[idx][jdx - 1] != WALL) && (visited[idx][jdx - 1] == NOT_VISITED)) {
                visited[idx][jdx - 1] = FROM_RIGHT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx - 1}), grid[idx][jdx - 1], next_distance }));
            }
        }
        else if (side == FROM_NONE) {
            if ((jdx < n - 1) && (grid[idx][jdx + 1] != WALL) && (visited[idx][jdx + 1] == NOT_VISITED)) {
                visited[idx][jdx + 1] = FROM_LEFT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx + 1}), grid[idx][jdx + 1], next_distance }));
            }
            if ((idx < m - 1) && (grid[idx + 1][jdx] != WALL) && (visited[idx + 1][jdx] == NOT_VISITED)) {
                visited[idx + 1][jdx] = FROM_UP;
                bfs_queue.push(Item({ pricing_, Pair({idx + 1, jdx}), grid[idx + 1][jdx], next_distance }));
            }
            if ((idx > 0) && (grid[idx - 1][jdx] != WALL) && (visited[idx - 1][jdx] == NOT_VISITED)) {
                visited[idx - 1][jdx] = FROM_DOWN;
                bfs_queue.push(Item({ pricing_, Pair({idx - 1, jdx}), grid[idx - 1][jdx], next_distance }));
            }
            if ((jdx > 0) && (grid[idx][jdx - 1] != WALL) && (visited[idx][jdx - 1] == NOT_VISITED)) {
                visited[idx][jdx - 1] = FROM_RIGHT;
                bfs_queue.push(Item({ pricing_, Pair({idx, jdx - 1}), grid[idx][jdx - 1], next_distance }));
            }
        }
    }

    return result;
}


class Solution {
public:
    vector<vector<int>> highestRankedKItems(vector<vector<int>>& grid, vector<int>& pricing, vector<int>& start, int k) {
        return BFS(grid, pricing, start, k);
    }
};

void test_queue() {
    priority_queue<Item, vector<Item>, CompareRank> bfs_queue;
    //priority_queue<Item_> bfs_queue;

    Pair pricing({ 2, 3 });
    vector<vector<int>> coord({ {0, 1}, {}, {}, {} });
    Pair coords({ 0, 0 });
    vector<int> prices({ 3, 2, 2, 5 });
    vector<int> distances({ 2, 2, 2, 1 });
    vector<Item> items;
    //   vector<Item_> items;
    for (int i = 0; i < distances.size(); ++i) {
        items.push_back(Item({ pricing, coords, prices[i], distances[i] }));
        //items.push_back(Item_({ prices[i], distances[i], coords}));
    }

    for (auto& item : items) {
        bfs_queue.push(item);
    }
    for (auto& item : items) {
        bfs_queue.pop();
    }
}

/*int main() {

   // test_queue();

    vector<vector<int>> grid({ {0, 2, 0}});
    vector<int> pricing({2, 2});
    int k = 1;
    vector<int> start({0, 1});

    Solution sol;
    auto result = sol.highestRankedKItems(grid, pricing, start, k);

    return 0;
}*/

//2146

// не работает очередь - убрать компаратор + переопределить ноду.... отдельно от кода еще
// почему можно две разные очереди??
// или не ноду, а вектор
// ВСЁ РАБОТАЕТ! 

/*
Your code is correct. But I think you have a misunderstanding here. Because priority_queue is implemented using data structure heap. As we know, heap is not sorted. It only has the property that the maximum element is at the front. Every time, you insert an element into a heap, heap will use O(lgN) time to push the maximum into the front. And every time you pop an element, the largest element will be obtained. But heap is not sorted at all.
*/