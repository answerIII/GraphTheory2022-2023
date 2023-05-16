package Medium._2192_;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.TreeSet;

class Solution {
    private LinkedList<Integer>[] graph;
    private TreeSet<Integer>[] achievable;
    private boolean[] done;

    private void dfs(int start) {
        for (int adj : graph[start]) {
            if (!done[adj])
                dfs(adj);
            achievable[start].addAll(achievable[adj]);
            achievable[start].add(adj);
        }
       done[start] = true;
    }
    private void init(int n) {
        graph = new LinkedList[n];
        achievable = new TreeSet[n];
        done = new boolean[n];
        for (int i = 0; i < n; i++) {
            graph[i] = new LinkedList<>();
            achievable[i] = new TreeSet<>();
        }
    }
    private List<List<Integer>> allAchievable(int n) {
        List<List<Integer>> result = new ArrayList<>(n);
        for (int v = 0; v < n; v++) {
            if (!done[v])
                dfs(v);
            achievable[v].remove(v);
            result.add(new LinkedList<>());
            result.get(v).addAll(achievable[v]);
        }
        return result;
    }
    public List<List<Integer>> getAncestors(int n, int[][] edges) {
        init(n);

        for (int[] edge : edges) {
            int from = edge[0];
            int to = edge[1];
            graph[to].add(from);    //reversed graph
        }

        return allAchievable(n);
    }
}

