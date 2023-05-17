class Solution {
public:
	vector<int> findAllPeople(int n, vector<vector<int>>& meetings, int firstPerson) {
        vector<int> result;
        vector<bool> visited(n, false);
		vector<vector<pair<int, int>>> graph(n);

		for (int i = 0; i < meetings.size(); ++i) {
			graph[meetings[i][0]].push_back({meetings[i][1],meetings[i][2]});
            graph[meetings[i][1]].push_back({meetings[i][0],meetings[i][2]});
		}

		priority_queue<pair<int, int> , vector<pair<int, int>> , greater<pair<int, int>>> q;
        q.push({0, firstPerson});
        q.push({0, 0});

        while (!q.empty()) {
            pair<int, int> curr = q.top();
            q.pop();

            int person = curr.second;
            int time = curr.first;

            if(visited[person])
                continue;

            visited[person] = true;
            result.push_back(person);

            for (auto i : graph[person]) {
                if (!visited[i.first] && time <= i.second) {
                    q.push({i.second, i.first});
                }
            }
        }
		return result;
	}
};
