class Solution {
public:
    double distance(double x1, double y1, double x2, double y2)
    {
        return sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2));
    }

    int DFS(int index, int x1, int y1, int r1,
        vector<vector<int>>& bombs, vector<int>& visited)
    {
        visited[index] = 1;
        int count = 1;
        for (int i = 0; i < bombs.size(); ++i)
        {
            if (visited[i]) continue;
            if (distance(x1, y1, bombs[i][0], bombs[i][1]) <= r1)
            {
                count += DFS(i, bombs[i][0], bombs[i][1], bombs[i][2], bombs, visited);
            }
        }

        return count;
    }

    int maximumDetonation(vector<vector<int>>& bombs)
    {
        int answer = 0;
        for (int i = 0; i < bombs.size(); ++i)
        {
            vector<int> visited(bombs.size(), 0);
            answer = max(answer, DFS(i, bombs[i][0], bombs[i][1], bombs[i][2], bombs, visited));
        }

        return answer;
    }
};