#include <iostream>
#include <vector>
#include <stack>

using namespace std;

class Solution {
public:
    double frogPosition(int n, vector<vector<int>>& edges, int t, int target) 
    {
        vector<vector<int>> gr(n);
        for (int i = 0; i < n - 1; ++i)
        {
            gr[edges[i][0] - 1].emplace_back(edges[i][1] - 1);
            gr[edges[i][1] - 1].emplace_back(edges[i][0] - 1);
        }
        vector<double> v(n, -1);
        v[0] = 1;
        stack<pair<int, int>> st;
        st.push({0, 0});
        while(!st.empty())
        {
            auto[num, time] = st.top();
            st.pop();
            vector<int> tmp;
            for (int i = 0; i < gr[num].size(); ++i)
            {
                if (v[gr[num][i]] == -1)
                {
                    tmp.emplace_back(gr[num][i]);
                }
            }
            if (tmp.size() == 0)
            {
                if (num == target - 1)
                {
                    if (t >= time)
                    {
                        return v[num];
                    }
                    return 0;
                }
            }
            for (int i = 0; i < tmp.size(); ++i)
            {
                v[tmp[i]] = v[num] / tmp.size();
                st.push({tmp[i], time + 1});
                if (target - 1 == tmp[i] && time + 1 == t)
                {
                    return v[tmp[i]];
                }
            }
        }
        return 0;
    }
};