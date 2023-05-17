class Solution {
public:
    unordered_map<int,unordered_map<int,bool>>block;
    int max_area;

    bool isValid(int x, int y) {
        if (x < 0 || y < 0 || x >= 1000000 || y >= 1000000)
            return false;
        return !block[x][y];
    }

    bool isPossible(vector<int>& source, vector<int>& target) {
        unordered_map<int, unordered_map<int, bool>> visited;
        visited[source[0]][source[1]] = true;
        
        queue<pair<int, int>> q;
        q.push(make_pair(source[0], source[1]));
        int t = 1;
        
        while (!q.empty()) {
            int x = q.front().first;
            int y = q.front().second;
            q.pop();
          
            if ((x == target[0] && y == target[1]) || (t > max_area))
                return true;
            if (isValid(x - 1, y) && !visited[x - 1][y]) {
                ++t;
                visited[x-1][y]=true;
                q.push(make_pair(x - 1, y));
            }
            if (isValid(x + 1, y) && !visited[x + 1][y]) {
                ++t;
                visited[x + 1][y] = true;
                q.push(make_pair(x + 1, y));   
            }
            if (isValid(x, y - 1) && !visited[x][y - 1]) {
                ++t;
                visited[x][y - 1] = true;
                q.push(make_pair(x, y - 1));
            }
            if (isValid(x, y + 1) && !visited[x][y + 1]) {
                ++t;
                visited[x][y + 1] = true;
                q.push(make_pair(x, y + 1));
            }
        }
        return false;
    }
    
    bool isEscapePossible(vector<vector<int>>& blocked, vector<int>& source, vector<int>& target) {
        int cnt = 0;
        
        for(int i = 0; i < blocked.size(); ++i) {
            ++cnt;
            block[blocked[i][0]][blocked[i][1]] = true;
        }
        max_area = (cnt * (cnt - 1)) / 2;
        return isPossible(source, target) && isPossible(target, source);
    }
};
