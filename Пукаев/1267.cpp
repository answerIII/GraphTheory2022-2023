class Solution {
public:
    int countServers(vector<vector<int>>& grid) {
        vector<int> rowCount(grid.size(),0);
        vector<int> columnCount(grid[0].size(), 0);
        int result = 0;
        for(int i = 0; i < grid.size(); i++){
            for(int j = 0; j < grid[0].size(); j++){
                rowCount[i] += grid[i][j];
                columnCount[j] += grid[i][j];
            }
        }

        for(int i = 0; i < grid.size(); i++){
            for(int j = 0; j < grid[0].size(); j++){
                if(grid[i][j] && (rowCount[i] > 1 || columnCount[j]>1))	
                    result++;
            }
        }
        return result;
    }
};