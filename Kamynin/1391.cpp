class Solution {
public:
    bool hasValidPath(vector<vector<int>>& grid) {
	int m = grid.size(), n = grid[0].size();
    if (grid[0][0] == 5 || grid[m-1][n-1] == 4)
		return false;
	int i = 0, j = 0, d = -1, c = 0;
    int startDir = grid[0][0] == 4 ? 3 : -1;
    bool isCorrect = true;
	switch (grid[0][0])
	{
		case 1: d = 4; break;
		case 2: d = 1; break;
        case 3: d = 4; break;
		case 4: d = startDir; break;
		case 6: d = 1; break;
		default: return false;
	}
	while (true)
	{
        if (!isCorrect){
            if (startDir == 3)
                i = 0, j = 0, d = 2, c = 0, startDir = 2;
            else
                return false;
        }
        if (i == m - 1 && j == n - 1){
        	int v = grid[i][j];
            if (d == 1 && (v == 2 || v == 5 || v == 6) ||
                d == 2 && (v == 1 || v == 4 || v == 6) ||
                d == 3 && (v == 2 || v == 3 || v == 4) ||
                d == 4 && (v == 1 || v == 3 || v == 5))
                return true;
        }
		
		if ((c > m * n || i < 0 || j < 0 || i >= m || j >= n) && startDir == 3)
			i = 0, j = 0, d = 2, c = 0, startDir = 2;   
	    else if (i < 0 || j < 0 || i >= m || j >= n)
            break;
        else if (c > m * n)
			break;
        if (grid[i][j] == 1) {
            if (d == 2 || d == 4) d == 2 ? --j : ++j;
            else isCorrect = false; 
        }
        else if (grid[i][j] == 2) {
            if (d == 1 || d == 3) d == 1 ? ++i : --i;
            else isCorrect = false; 
        }
        else if (grid[i][j] == 3){
            if (d == 3 || d == 4) d == 3 ? (--j, d = 2) : (++i, d = 1);
            else isCorrect = false; 
        }
        else if (grid[i][j] == 4) {
            if (d == 2 || d == 3) d == 2 ? (++i, d = 1) : (++j, d = 4); 
            else isCorrect = false; 
        }
        else if (grid[i][j] == 5) {
            if (d == 1 || d == 4) d == 1 ? (--j, d = 2) : (--i, d = 3); 
            else isCorrect = false; 
        }
        else if (grid[i][j] == 6) {
            if (d == 1 || d == 2) d == 1 ? (++j, d = 4) : (--i, d = 3);
            else isCorrect = false;
        } 
        ++c; 
        
	}
	return false;
}
};
