#include <string>
#include <vector>
#include <iostream>

using namespace std;

class Solution {
public:
    bool pyramidTransition(string bottom, vector<string> allowed) 
    {
        vector<vector<vector<char>>> all(26, vector<vector<char>>(26));
        for (int i = 0; i < allowed.size(); ++i)
        {
            all[allowed[i][0] - 'A'][allowed[i][1] - 'A'].emplace_back(allowed[i][2]);
        }
        return fun(bottom, all, "");
    }

    bool fun(string bottom, vector<vector<vector<char>>>& all, string str)
    {
        if (bottom.size() == 1)
        {
            return true;
        }
        if (str.size() == bottom.size() - 1)
        {
            return fun(str, all, "");
        }
        for (int i = 0; i < all[bottom[str.size()] - 'A'][bottom[str.size() + 1] - 'A'].size(); ++i)
        {
            if (fun(bottom, all, str + all[bottom[str.size()] - 'A'][bottom[str.size() + 1] - 'A'][i]))
            {
                return true;
            }
        }
        return false;
    } 
};