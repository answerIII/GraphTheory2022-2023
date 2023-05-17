class Solution {
public:
    bool dfs(set<pair<int, int>>& blocks, pair<int, int> source, pair<int, int> target) {
        set<pair<int, int>> connS;
        stack<pair<int, int>> inwork;
        connS.insert(source);
        inwork.push(source);
        while (!inwork.empty() && connS.size() <= 19900) {
            auto[x, y] = inwork.top(); inwork.pop();
            if (y + 1 < 1'000'000 &&
                connS.find({x, y+1}) == connS.end() &&
                blocks.find({x, y+1}) == blocks.end()
            ) {
                if (x == target.first && y+1 == target.second) {return true;}
                connS.insert({x, y+1});
                inwork.push({x, y+1});
            }
            if (x + 1 < 1'000'000 &&
                connS.find({x+1, y}) == connS.end() &&
                blocks.find({x+1, y}) == blocks.end()
            ) {
                if (x+1 == target.first && y == target.second) {return true;}
                connS.insert({x+1, y});
                inwork.push({x+1, y});
            }
            if (y - 1 >= 0 &&
                connS.find({x, y-1}) == connS.end() &&
                blocks.find({x, y-1}) == blocks.end()
            ) {
                if (x == target.first && y-1 == target.second) {return true;}
                connS.insert({x, y-1});
                inwork.push({x, y-1});
            }
            if (x - 1 >= 0 &&
                connS.find({x-1, y}) == connS.end() &&
                blocks.find({x-1, y}) == blocks.end()
            ) {
                if (x-1 == target.first && y == target.second) {return true;}
                connS.insert({x-1, y});
                inwork.push({x-1, y});
            }
        }
        if (connS.size() > 19900) {return true;}
        return false;
    }
    bool isEscapePossible(vector<vector<int>>& blocked, vector<int>& source, vector<int>& target) {
        set<pair<int, int>> blocks;
        for (int i = 0; i < blocked.size(); ++i) {blocks.insert({blocked[i][0], blocked[i][1]});}
        return (dfs(blocks, {source[0], source[1]}, {target[0], target[1]}) &&
            dfs(blocks, {target[0], target[1]}, {source[0], source[1]}));

    }
};
