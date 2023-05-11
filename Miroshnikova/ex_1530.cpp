#include <vector>
#include <iostream>

using namespace std;


struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* left, TreeNode* right) : val(x), left(left), right(right) {}
};


bool isLeaf(TreeNode* node) {
    return ((node->left == NULL) && (node->right == NULL));
}

int count_pairs_in_two_arrays(vector<int>& leftNodes, vector<int>& rightNodes, int dist) {
    if ((leftNodes.size() == 0) || (rightNodes.size() == 0))
        return 0;

    int left = 0;
    int right = rightNodes.size() - 1;

    int count = 0;
    while ((left < leftNodes.size()) && (right >= 0)) {
        int current_left = leftNodes[left];

        while ((leftNodes[left] + rightNodes[right] > dist) && (right >= 0)) {
            --right;
            if (right < 0)
                return count;
        }
        count += right + 1;
        ++left;

        while ((left < leftNodes.size()) && (current_left == leftNodes[left])) {
            count += right + 1;
            ++left;
        }
    }
    return count;
}

void merge_arrays(vector<int>& leftNodes, vector<int>& rightNodes, int dist, vector<int>* result) {
    int left = 0;
    int right = 0;

    while (true) {
        if ((left >= leftNodes.size()) || (leftNodes[left] > dist)) {
            while ((right < rightNodes.size()) && (rightNodes[right] <= dist)) {
                result->push_back(rightNodes[right]);
                ++right;
            }
            break;
        }
        else if ((right >= rightNodes.size()) || (rightNodes[right] > dist)) {
            while ((left < leftNodes.size()) && (leftNodes[left] <= dist)) {
                result->push_back(leftNodes[left]);
                ++left;
            }
            break;
        }
        if (leftNodes[left] < rightNodes[right]) {
            result->push_back(leftNodes[left]);
            ++left;
        }
        else {
            result->push_back(rightNodes[right]);
            ++right;
        }
    }

}

struct Result {
    vector<int> nodes_distances;
    int count_pairs;
};

Result countDistance(TreeNode* node, int dist) {
    if (node == NULL)
        return { vector<int>({ }), 0 };

    if (isLeaf(node))
        return { vector<int>({ 1 }), 0 };

    Result leftResult = countDistance(node->left, dist);
    Result rightResult = countDistance(node->right, dist);
    vector<int>& leftNodes = leftResult.nodes_distances;
    vector<int>& rightNodes = rightResult.nodes_distances;

    // считаем количество пар, которые можно образовать с помощью левого и правого поддеревьев
    int count = count_pairs_in_two_arrays(leftNodes, rightNodes, dist);

    // сливаем массивы
    vector<int> result;
    merge_arrays(leftNodes, rightNodes, dist, &result);

    // добавляем ребро до следующей вершины
    for (int i = 0; i < result.size(); ++i) {
        result[i] += 1;

    }
    return { result, leftResult.count_pairs + rightResult.count_pairs + count };
}


class Solution {
public:
    int countPairs(TreeNode* root, int distance) {
        return countDistance(root, distance).count_pairs;
    }
};

#include <queue>

const int LEFT = 0;
const int RIGHT = 1;

void addNode(TreeNode* parent, int side, int value, queue<TreeNode*>& queue) {
    if ((value == 0) || (parent == NULL)) {
        queue.push(NULL);
        return;
    }
    TreeNode* node = new TreeNode(value);
    queue.push(node);
    if (side == LEFT)
        parent->left = node;
    else
        parent->right = node;
}

TreeNode* parser(vector<int>& tree) {
    queue<TreeNode*> queue;
    TreeNode* root = new TreeNode(tree[0]);
    queue.push(root);
    int i = 1;
    while (i < tree.size()) {
        TreeNode* current = queue.front();
        queue.pop();
        addNode(current, LEFT, tree[i], queue);
        ++i;
        if (i >= tree.size())
            break;
        addNode(current, RIGHT, tree[i], queue);
        ++i;
    }
    return root;
}

void test_count() {

}

void test_merge() {
    vector<vector<int>> lefts({ {}, {2}, {1}, {2}, {1, 2}, {1, 4}, {3}, {1}, {1, 2, 3}, {4, 5}, {1, 2, 6, 7} });
    vector<vector<int>> rights({ {1}, {}, {2}, {1}, {0, 3}, {2}, {1, 2}, {2, 3}, {1, 2, 3, 4, 5}, {1, 2, 3}, {4, 5, 8, 9} });
    int dist = 6;
    for (int i = 0; i < lefts.size(); ++i) {
        vector<int> result;
        merge_arrays(lefts[i], rights[i], dist, &result);
        for (int j = 0; j < result.size(); ++j)
            cout << result[j] << " ";
        cout << endl;
    }

}

/*int main() {
    test_merge();

    vector<int> tree({ 7,1,4,6,0,5,3,0,0,0,0,0,2 });
    TreeNode* root = parser(tree);

    int dist = 3;

    Solution sol;
    int result = sol.countPairs(root, dist);

    return 0;
}*/

// 1530