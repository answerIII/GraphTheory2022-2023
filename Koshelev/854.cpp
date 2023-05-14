class Solution {
public:
    vector<string> permutations(string& s, string& s2, unordered_set<string>& set) {
        vector<string> variants;
        int ind = 0;
        for (int i = 0; i < s2.size(); i++)
        {    
            if (s[i] != s2[i])
                break;
            ind++;
        }
        for (int i = 0; i < s.size(); i++) {
            if (s[i] == s2[ind]) {
                string newString = s;
                char symbol = newString[i];
                newString[i] = newString[ind];
                newString[ind] = symbol;
                if (set.find(newString) == set.end()) {
                    variants.push_back(newString);
                    set.insert(newString);
                }
            }
        }
        return variants;
    }
    int kSimilarity(string s1, string s2) {
        unordered_set<string> set;
        if (s1 == s2)
            return 0;
        else
        {
            queue<string> q;
            q.push(s1);
            int k = 1;
            string s;
            while (!q.empty()) {
                int size = q.size();
                while (size--) {
                    s = q.front();
                    q.pop();
                    vector<string> variants = permutations(s, s2, set);
                    for (int i = 0; i < variants.size(); i++)
                    {
                        if (variants[i] == s2)
                            return k;
                        q.push(variants[i]);
                    }
                }
                k++;
            }
            return -1;
        }
        
    }
};