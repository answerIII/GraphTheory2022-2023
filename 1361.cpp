#include <vector>
#include <stack>

using namespace std;

class Solution {
public:
    bool validateBinaryTreeNodes(int n, vector<int>& leftChild, vector<int>& rightChild) 
    {
        vector<int> v(n);
        for (int i = 0; i < n; ++i)
        {
            if (leftChild[i] != -1) ++v[leftChild[i]];
            if (rightChild[i] != -1) ++v[rightChild[i]];
        }
        int root = -1;
        for (int i = 0; i < n; ++i)
        {
            if (v[i] == 0 && root != -1) return false;
            if (v[i] == 0) root = i;
        }
        if (root == -1) return false;

        stack<int> st;
        st.push(root);
        vector<bool> vis(n);
        vis[root] = true;

        while(!st.empty())
        {
            int nd = st.top();
            st.pop();
            if (leftChild[nd] != -1)
            {
                if (vis[leftChild[nd]]) return false;
                vis[leftChild[nd]] = true;
                st.push(leftChild[nd]);
            }
            if (rightChild[nd] != -1)
            {
                if (vis[rightChild[nd]]) return false;
                vis[rightChild[nd]] = true;
                st.push(rightChild[nd]);
            }
        }

        for (int i = 0; i < n; ++i)
        {
            if (!vis[i]) return false;
        }
        return true;
    }
};