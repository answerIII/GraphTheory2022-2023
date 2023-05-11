#include <vector>
#include <queue>

using namespace std;

class Solution {
public:
    int minimumJumps(vector<int>& forbidden, int a, int b, int x) 
    {
        vector<int> d(4000001, -1);
        for (auto i : forbidden)
        {
            d[i] = INT_MAX;
        }
        d[0] = 0;
        queue<int> q, w;
        q.push(0);
        while(!q.empty() || !w.empty()){
            int t;
            if (w.empty())
            {
                t = q.front();
                q.pop();
            } 
            else if (q.empty())
            {
                t = w.front();
                w.pop();
            } 
            else if (d[w.front()] <= d[q.front()])
            {
                t = w.front();
                w.pop();
            }
            else
            {
                t = q.front();
                q.pop();
            }
            if (t + a < 4000001 && d[t + a] == -1)
            {
                if (t + a == x)
                {
                    return d[t] + 1;
                }
                d[t + a] = d[t] + 1;
                q.push(t + a);
            }
            if (t - b > 0 && d[t - b] == -1)
            {
                if (t - b == x)
                {
                    return d[t] + 1;
                }
                if (t - b + a < 4000001 && d[t - b + a] == -1)
                {
                    if (t - b + a == x)
                    {
                        return d[t] + 2;
                    }
                    d[t - b + a] = d[t] + 2;
                    w.push(t - b + a);
                }
            }
        }
        return d[x];
    }
};