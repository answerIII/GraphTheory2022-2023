class Solution {
public:
    bool canMeasureWater(int jug1Capacity, int jug2Capacity, int targetCapacity) {
        if (jug1Capacity > jug2Capacity) {
            swap(jug1Capacity, jug2Capacity);
        }
        queue<pair<int, int> > q;
        map<pair<int, int>, bool > used;
        used[make_pair(0, 0)] = true;
        q.push(make_pair(0, 0));
        pair<int, int> coords;
        int difference, x, y;
        pair<int, int> newCoords;
        while (!q.empty()) {
            coords = q.front();
            x = coords.first;
            y = coords.second;
            if (x == targetCapacity || y == targetCapacity || x + y == targetCapacity) return true;
            q.pop();
            
            if (x + y - jug1Capacity > 0)
                difference = x + y - jug1Capacity;
            else difference = 0;

            newCoords = make_pair(x + y - difference, difference);
            
            if (used.find(newCoords) == used.end()) {
                used[newCoords] = true;
                q.push(newCoords);
            }

            if (x + y - jug2Capacity > 0)
                difference = x + y - jug2Capacity;
            else difference = 0;

            newCoords = make_pair(difference, y + x - difference);
            
            if (used.find(newCoords) == used.end()) {
                used[newCoords] = true;
                q.push(newCoords);
            }

            newCoords = make_pair(jug1Capacity, y);

            if (used.find(newCoords) == used.end()) {
                used[newCoords] = true;
                q.push(newCoords);
            }

            newCoords = make_pair(x, jug2Capacity);

            if (used.find(newCoords) == used.end()) {
                used[newCoords] = true;
                q.push(newCoords);
            }

            newCoords = make_pair(0, y);

            if (used.find(newCoords) == used.end()) {
                used[newCoords] = true;
                q.push(newCoords);
            }

            newCoords = make_pair(x, 0);

            if (used.find(newCoords) == used.end()) {
                used[newCoords] = true;
                q.push(newCoords);
            }
        }
        return false;
    }
};
