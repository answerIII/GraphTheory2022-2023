int dx[8] = {0,  0, 1,  1, 1, -1, -1, -1};
int dy[8] = {1, -1, 0, -1, 1,  0, -1,  1};

class Solution {
public:
    int latestDayToCross(int row, int col, vector<vector<int>>& cells) {
        int n = row * col;
        bool** water = new bool*[row];
        int** numberOfComponent = new int*[row];
        int* isComponentReachesEndOfRow = new int[n];
        int countOfComponents = 0;
        for (int i = 0; i < n; ++i) {
            isComponentReachesEndOfRow[i] = false;
        }
        for (int i = 0; i < row; ++i) {
            water[i] = new bool[col];
            numberOfComponent[i] = new int[col];
            for (int j = 0; j < col; ++j) {
                water[i][j] = false;
                numberOfComponent[i][j] = 0;
            }
        }
        queue<pair<int, int> > q;
        for (int i = 0; i < n - row; ++i) {
            int x = cells[i][0] - 1, y = cells[i][1] - 1;
            water[x][y] = true; 
            for (int j = 0; j < 8; ++j) {
                int neighborX = x + dx[j];
                int neighborY = y + dy[j];
                if (!(neighborX < 0 || neighborX >= row || neighborY < 0 || neighborY >= col || !water[neighborX][neighborY])) {
                    if (numberOfComponent[x][y] != 0) {
                        int oldComponent = numberOfComponent[neighborX][neighborY];
                        int newComponent = numberOfComponent[x][y];
                        if (isComponentReachesEndOfRow[oldComponent] == true) {
                            isComponentReachesEndOfRow[newComponent] = true;
                        }
                        q.push(make_pair(neighborX, neighborY));
                        numberOfComponent[neighborX][neighborY] = newComponent;
                        while(!q.empty()) {
                            pair<int, int> v = q.front();
                            q.pop();
                            for (int k = 0; k < 8; ++k) {
                                int toX = v.first + dx[k];
                                int toY = v.second + dy[k];
                                if (!(toX < 0 || toX >= row || toY < 0 || toY >= col || !water[toX][toY] || numberOfComponent[toX][toY] == newComponent)) {
                                    numberOfComponent[toX][toY] = newComponent;
                                    q.push(make_pair(toX, toY));
                                }
                            }
                        }
                        
                    } else {
                        numberOfComponent[x][y] = numberOfComponent[neighborX][neighborY];
                        if (y == col - 1) {
                            isComponentReachesEndOfRow[numberOfComponent[x][y]] = true;
                        }
                    }
                }
            }
            if (numberOfComponent[x][y] == 0) {
                numberOfComponent[x][y] = ++countOfComponents;
                if (y == col - 1){
                    isComponentReachesEndOfRow[numberOfComponent[x][y]] = true;
                }
            }
            for (int j = 0; j < row; ++j) {
                if (isComponentReachesEndOfRow[numberOfComponent[j][0]]) {
                    return i;
                }
            }
        }
        return n - row;
    }
};