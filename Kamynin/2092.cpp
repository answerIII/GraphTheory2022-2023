class Solution {
public:
    
class DSU{
public:
    int* p;
    DSU(int n){
        p = new int[n];
    }

    void makeSet(int x){
        p[x] = x;
    }

    int find(int x){
        if (p[x] == x)
            return x;
        return p[x] = find(p[x]);
    }

    void join(int x, int y){ 
        x = find(x), y = find(y);
        srand((unsigned)time(NULL));
        if (rand() % 2 == 0)
            std::swap(x,y);
        p[x] = y;  
    }

    int get(int x){
        return p[x];
    }

    void unset(int x){
        p[x] = x;
    }

};

std::vector<int> findAllPeople(int n, std::vector<std::vector<int>>& meetings, int firstPerson) {
    std::sort(meetings.begin(), meetings.end(),
          [](const std::vector<int>& a, const std::vector<int>& b) { return a[2] < b[2]; });
    std::vector<int> result;
    DSU s(n);
    for (int i = 0; i < n; ++i)
        s.makeSet(i);
    s.join(0, firstPerson);
    int root = s.find(0);
    int time = 0;
    std::vector<int> v;
    for (auto m: meetings){
        if (m[2] != time){
            for (auto node: v)
                if (s.find(node) != root)
                    s.unset(node);
            v.clear();
            time = m[2];
        }
        v.push_back(m[0]);
        v.push_back(m[1]);
        s.join(m[0], m[1]);
        root = s.find(0);
    }
    for(int i = 0; i < n; ++i)
        if (s.find(i) == root)
            result.push_back(i);
    return result;
}
};
