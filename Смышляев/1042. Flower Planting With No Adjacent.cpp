class Solution {
    struct TreeNode {
        int num;
        int c;
        vector<TreeNode*> adj;
        TreeNode(int n) : num(n), c(0), adj() {}
        TreeNode(int n, int x) : num(n), c(x), adj() {}
      };
public:
    vector<int> colorize(vector<TreeNode*>& gardens, vector<int>& ans) {
        stack<TreeNode*> s;
        vector<bool> availableColors(4, true);
        bool flag;
        while (true) {
            flag = true;
            for (int i = 1; i < gardens.size(); ++i) {
                if (gardens[i]->c == 0) {
                    s.push(gardens[i]);
                    flag = false;
                    break;
                }
            }
            if (flag) {break;}
            while(!s.empty()) {
                availableColors.assign(4, true);
                TreeNode* cur = s.top();
                s.pop();
                for (int i = 0; i < cur->adj.size(); ++i) {
                    if (cur->adj[i]->c == 0) {
                        s.push(cur->adj[i]);
                    } else {
                        availableColors[cur->adj[i]->c-1] = false;
                    }
                }
                if (availableColors[0]) {cur->c = 1; ans[cur->num-1] = 1; continue;}
                if (availableColors[1]) {cur->c = 2; ans[cur->num-1] = 2; continue;}
                if (availableColors[2]) {cur->c = 3; ans[cur->num-1] = 3; continue;}
                if (availableColors[3]) {cur->c = 4; ans[cur->num-1] = 4; continue;}
            }
        }
        return ans;
    }
    vector<int> gardenNoAdj(int n, vector<vector<int>>& paths) {
        vector<int> ans(n, 0);
        vector<TreeNode*> gardens(n+1, nullptr);
        for (int i = 1; i <= n; ++i) {
            gardens[i] = new TreeNode(i);
        }
        for (int i = 0; i < paths.size(); ++i) {
            gardens[paths[i][0]]->adj.push_back(gardens[paths[i][1]]);
            gardens[paths[i][1]]->adj.push_back(gardens[paths[i][0]]);
        }
        // for (int i = 1; i <= n; ++i) {
        //     cout << gardens[i]->adj.size() << ' ';
        // }
        ans = colorize(gardens, ans);
        return ans;
    }
};
