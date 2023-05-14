int DFS(unordered_map<int, vector<int>>& ls, int& head, vector<int>& informTime) {
	int depth = informTime[head];
	int sup = 0;
	auto ptr = ls.find(head);
	if (ptr != ls.end()) {
		for (auto x : ptr->second) {
			int supRes = DFS(ls, x, informTime);
			if (supRes > sup) {
				sup = supRes;
			}
		}
	}
	return depth + sup;
}
class Solution {
public:
	int numOfMinutes(int n, int headID, vector<int>& manager, vector<int>& informTime) {
		unordered_map<int, vector<int>> ls;
		for (int i = 0; i < manager.size(); ++i) {
			auto ins_ptr = ls.find(manager[i]);
			if (ins_ptr != ls.end()) {
				ins_ptr->second.push_back(i);
			}
			else {
				ls.insert({ manager[i], vector<int>(1, i) });
			}
		}
		return DFS(ls, headID, informTime);
	}
};
