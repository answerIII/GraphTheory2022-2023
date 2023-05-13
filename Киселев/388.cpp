class Solution {
private:
    int max_path;

    vector<string> string_decomposition(string s) {
        vector<string> data;
        int end = s.find('\n'); 
        while (end != -1) {
            cout << s.substr(0, end) << endl;
            data.push_back(s.substr(0, end));
            s.erase(s.begin(), s.begin() + end + 1);
            end = s.find('\n');
        }
        cout << s.substr(0, end);
        data.push_back(s.substr(0, end));
        return data;
    }

    void get_max_path(vector<string> data) {
        map<int, int> len;
        for(string node: data) {
            int num_tabs  = 0; 
                
            while (node[num_tabs] == '\t') 
                ++num_tabs;
            
            if (num_tabs)
                len[num_tabs] = len[num_tabs - 1] + 1 + node.substr(num_tabs).size(); 
            else
                len[num_tabs] = node.size(); 
            
            if (node.find('.') != string :: npos)
                max_path = max(max_path, len[num_tabs]);
        }
    }

public:
    Solution(): max_path(0) {}

    int lengthLongestPath(string input) {
        get_max_path(string_decomposition(input));
        return max_path;
    }
};
