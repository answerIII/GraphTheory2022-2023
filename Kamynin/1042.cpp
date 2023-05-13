class Solution {
public:
    void colorDFS(int start, vector<vector<int>>& adj, vector<int>& colors)
{
    stack<int> s;
    s.push(start);
    while(!s.empty()){
        int cur = s.top();
        s.pop();
        for (int i = 1; i < 5; ++i){
            for (int j = 2; j < 5; ++j){
                int v = adj[cur-1][j];
                if (v != 0 && colors[v-1] == i)
                    break;
                if (v == 0 || j == 4)
                    colors[cur-1] = i;
            }
            if (colors[cur-1] != 0)
                break;
        }
        adj[cur-1][0] = 1;
        int i = 2;
        while(i < 5 && adj[cur-1][i] != 0){
            int v = adj[cur-1][i];
            if (adj[v-1][0] == 0){
                s.push(v);
                adj[v-1][0] = 1;
            }
            ++i;
        }
    }
}

vector<int> gardenNoAdj(int n, vector<vector<int>>& paths) {
    vector<vector<int>> adj(n);
    vector<int> colors(n);
    for (int i = 0; i < adj.size(); ++i)
        adj[i] = {0,1,0,0,0};
    
    for (auto path : paths){
        int v = path[0]-1;
        ++adj[v][1];
        adj[v][adj[v][1]] = path[1];
    }

    for (auto path : paths){
        int v = path[1]-1;
        ++adj[v][1];
        adj[v][adj[v][1]] = path[0];
    }

    bool done = false;
    while (!done) {
        for (int i = 0; i < colors.size(); ++i){
            if (colors[i] == 0)
                colorDFS(i+1, adj, colors);
            else if (i == colors.size() - 1)
                done=true;
        }
    }

    return colors;
}
};
