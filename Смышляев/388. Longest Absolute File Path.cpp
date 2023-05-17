class Solution {
    struct TreeNode {
        int len;
        bool isFile;
        vector<TreeNode*> children;
        TreeNode() : len(0), isFile(false), children() {}
        TreeNode(int n) : len(n), isFile(false), children() {}
        TreeNode(int n, bool f) : len(n), isFile(f), children() {}
    };
public:
    vector<string> split(string s) {
        vector<string> ans;
        string cur = "";
        for (int i = 0; i < s.size(); ++i) {
            if (s[i] == '\n') {
                ans.push_back(cur);
                cur = "";
                continue;
            }
            cur += s[i];
        }
        ans.push_back(cur);
        return ans;
    }

    vector<pair<int, string>> countLevels(vector<string> v) {
        vector<pair<int, string>> ans;
        int counter = 0;
        for (int i = 0; i < v.size(); ++i) {
            for (int j = 0; v[i][j] == '\t'; ++j) {++counter;}
            if (counter != 0) {ans.push_back({counter, v[i].substr(counter)});}
            else {ans.push_back({counter, v[i]});}
            counter = 0;
        }
        return ans;
    }

    int findAns(TreeNode* root, long prev, long m) {
        if (root->children.empty()) {
            if (root->isFile) {
                return max(root->len+prev, m);
            } else {
                return m;
            }
        }
        int tmp = 0;
        for (int i = 0; i < root->children.size(); ++i) {
            tmp = findAns(root->children[i], prev+1+root->len, m);
            if (tmp > m) {m = tmp;}
        }
        return m;
    }

    int lengthLongestPath(string input) {
        TreeNode* root = new TreeNode();
        vector<string> s = split(input);
        vector<pair<int, string>> v = countLevels(s);

        int level = -1;
        stack<TreeNode*> prev;
        prev.push(root);
        for (int i = 0; i < v.size(); ++i) {
            if (v[i].first <= level) {
                for (int j = 0; j <= level - v[i].first; ++j) {prev.pop();}
                level = v[i].first;
            }
            if (v[i].first > level) {
                ++level;
            }
            TreeNode* tmp = new TreeNode(v[i].second.size());
            if (v[i].second.find('.') != string::npos) {tmp->isFile = true;}
            prev.top()->children.push_back(tmp);
            prev.push(tmp);
        }
        return max(findAns(root, 0, 0) - 1, 0);
    }
};
