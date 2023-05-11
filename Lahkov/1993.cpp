#include <vector>
#include <iostream>
using namespace std;

class LockingTree {
private:
    vector<int> parent, locked;
    vector<vector<int>> child;
public:
    LockingTree(vector<int>& _parent) :parent(_parent) {
        locked.resize(parent.size(), 0);
        child.resize(parent.size());
        for (int i = 1; i < parent.size(); i++) {
            child[parent[i]].push_back(i);
        }
    }

    bool lock(int _num, int _user) {
        if (locked[_num] == 0) {
            locked[_num] = _user;
            return true;
        }
        return false;
    }

    bool unlock(int _num, int _user) {
        if (locked[_num] == _user) {
            locked[_num] = 0;
            return true;
        }
        return false;
    }

    bool upgrade(int _num, int _user) {
        if (locked[_num] != 0)
            return false;
        if (goUp(_num) == false)
            return false;
        if (goDown(_num) == false)
            return false;
        locked[_num] = _user;
        return true;
    }
    bool goUp(int _num) {
        if (locked[_num] != 0) return false;
        if (parent[_num] == -1) return true;
        return goUp(parent[_num]);
    }

    bool goDown(int _num) {
        bool tmp = false;
        for (int i = 0; i < child[_num].size(); i++) {
            if (goDown(child[_num][i]) == true)
                tmp = true;
        }
        if (locked[_num] != 0) {
            locked[_num] = 0;
            return true;
        }
        return tmp;
    }
};