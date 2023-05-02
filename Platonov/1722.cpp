class Solution {
public:

    int minimumHammingDistance(vector<int>& source, vector<int>& target, vector<vector<int>>& allowedSwaps) {
        int n = source.size();
        vector<vector<int> > edges(n);
        for (int i = 0; i < allowedSwaps.size(); ++i) {
            edges[allowedSwaps[i][0]].push_back(allowedSwaps[i][1]);
            edges[allowedSwaps[i][1]].push_back(allowedSwaps[i][0]);
        }
        int* numberOfComponent = new int[n];
        vector<int> component;
        vector<int> sourceCopy;
        vector<int> targetCopy;
        int countOfComponents = 0;
        for (int i = 0; i < n; ++i) numberOfComponent[i] = 0;
        int result = n;
        for (int i = 0; i < n; ++i) {
            if (numberOfComponent[i] == 0) {
                ++countOfComponents;
                dfs(numberOfComponent, edges, component, i, countOfComponents);
                for (int j = 0; j < component.size(); ++j) {
                    sourceCopy.push_back(source[component[j]]);
                    targetCopy.push_back(target[component[j]]);
                }
                sort(sourceCopy.begin(), sourceCopy.end());
                sort(targetCopy.begin(), targetCopy.end());
                for (int j = 0, k = 0; j < component.size() && k < component.size(); ++j) {
                    k = lower_bound(sourceCopy.begin() + k, sourceCopy.end(), targetCopy[j]) - sourceCopy.begin();
                    if (k < sourceCopy.size() && sourceCopy[k] == targetCopy[j]) {
                        --result;
                        ++k;
                    }
                }
                sourceCopy.clear();
                targetCopy.clear();
                component.clear();
            }
        }
        return result;
    }

    void dfs(int* numberOfComponent, vector<vector<int> >& edges, vector<int>& component, int v, int countOfComponents) {
        numberOfComponent[v] = countOfComponents;
        component.push_back(v);
        for (int i = 0; i < edges[v].size(); ++i) {
            if (numberOfComponent[edges[v][i]] == 0) {
                dfs(numberOfComponent, edges, component, edges[v][i], countOfComponents);
            }
        }
    }
};