package Medium._2385_;

import java.util.*;

class Solution {
    TreeMap<Integer, List<Integer>> graph = new TreeMap<>();
    HashSet<Integer> visited = new HashSet<>();

    private void addEdges(int v1, int v2) {
        if (!graph.containsKey(v1)) graph.put(v1, new LinkedList<>());
        if (!graph.containsKey(v2)) graph.put(v2, new LinkedList<>());

        graph.get(v1).add(v2);
        graph.get(v2).add(v1);
    }
    private void makeGraph(TreeNode root) {
        if (root == null)
            return;
        if (root.left != null) {
            addEdges(root.val, root.left.val);
            makeGraph(root.left);
        }
        if (root.right != null) {
            addEdges(root.val, root.right.val);
            makeGraph(root.right);
        }
    }
    private int bfs(int start, int level) {
        if (visited.contains(start))
            return level - 1;

        visited.add(start);
        int maxLevel = 0;

        for (int next : graph.get(start)) {
            int depth = bfs(next, level + 1);
            if (maxLevel < depth)
                maxLevel = depth;
        }

        return maxLevel;
    }
    public int amountOfTime(TreeNode root, int start) {
       makeGraph(root);
       if (graph.get(start) == null)
           return 0;
       return bfs(start, 0);
    }
}
