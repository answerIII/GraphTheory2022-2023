#include <vector>
#include <string>
#include <stack>

using namespace std;

class NestedInteger {
  public:
    // Constructor initializes an empty nested list.
    NestedInteger();

    // Constructor initializes a single integer.
    NestedInteger(int value);

    // Return true if this NestedInteger holds a single integer, rather than a nested list.
    bool isInteger() const;

    // Return the single integer that this NestedInteger holds, if it holds a single integer
    // The result is undefined if this NestedInteger holds a nested list
    int getInteger() const;

    // Set this NestedInteger to hold a single integer.
    void setInteger(int value);

    // Set this NestedInteger to hold a nested list and adds a nested integer to it.
    void add(const NestedInteger &ni);

    // Return the nested list that this NestedInteger holds, if it holds a nested list
    // The result is undefined if this NestedInteger holds a single integer
    const vector<NestedInteger> &getList() const;
};
class Solution {
public:
    NestedInteger deserialize(string s) 
    {
        if (s[0] == '[') return deserialize(s, 1).first;
        return deserialize(s, 0).first;
    }
    pair<NestedInteger, int> deserialize(string s, int i) 
    {
        NestedInteger ans;
        int num = 0;
        int sign = 0;
        for (i; i < s.size(); ++i)
        {
            if (s[i] == '-') sign = 2;
            else if (s[i] >= '0' && s[i] <= '9')
            {
                if (sign == 0) sign = 1;
                if (sign == 1) num = num * 10 + (s[i] - '0');
                else num = num * 10 - (s[i] - '0');
            }
            else if (s[i] == ',') 
            {
                if (sign != 0) ans.add(NestedInteger(num));
                sign = 0;
                num = 0;
            }
            else if (s[i] == '[')
            {
                pair<NestedInteger, int> res = deserialize(s, i + 1);
                ans.add(res.first);
                i = res.second;
                sign = 0;
                num = 0;
            }
            else
            {
                if (sign != 0) ans.add(NestedInteger(num));
                sign = 0;
                num = 0;
                return {ans, i};
            }
        }
        if (sign != 0)
        {
            if (ans.isInteger() || ans.getList().size() > 0) ans.add(NestedInteger(num));
            else ans.setInteger(num);
        }
        sign = 0;
        num = 0;
        return {ans, s.size()};
    }
};