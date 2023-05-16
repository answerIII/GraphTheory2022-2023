package Medium._1786_;

import java.util.*;
class Solution {
    private Map<Integer, Map<Integer, Integer>> G = new HashMap<>();
    private PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> (a[1] - b[1]));
    private int[] distTo, numberOfRestrictedPaths;
    private int numberOfVertices, MOD = 1_000_000_007;

    private void init(int n, int[][] edges) {
        numberOfVertices = n;
        distTo = new int[numberOfVertices + 1];
        numberOfRestrictedPaths = new int[numberOfVertices + 1];

        Arrays.fill(numberOfRestrictedPaths, -1);

        for (int[] e : edges) {
            int from = e[0];
            int to = e[1];
            int weight = e[2];

            G.putIfAbsent(from, new HashMap<>());
            G.putIfAbsent(to, new HashMap<>());

            G.get(from).put(to, weight);
            G.get(to).put(from, weight);
        }
    }
    private void findShortestPaths() {
        pq.offer(new int[]{ numberOfVertices, 0 });

        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int vertexFrom = current[0];
            int distanceFrom = current[1];

            for (Map.Entry<Integer, Integer> edge : G.get(vertexFrom).entrySet()) {
                int vertexTo = edge.getKey();
                int weight = edge.getValue();

                if (vertexTo == numberOfVertices)
                    continue;

                int newDistTo = distanceFrom + weight;
                if (distTo[vertexTo] == 0 || newDistTo < distTo[vertexTo]) {
                    distTo[vertexTo] = newDistTo;
                    pq.offer(new int[]{ vertexTo, newDistTo });
                }
            }
        }
    }
    public int countRestrictedPaths(int n, int[][] edges) {
        init(n, edges);
        findShortestPaths();
        return dfs(1, n);
    }

    private int dfs(int vertexFrom, int finalVertex) {
        if (vertexFrom == finalVertex)
            return 1;

        if (numberOfRestrictedPaths[vertexFrom] != -1)
            return numberOfRestrictedPaths[vertexFrom];

        int sum = 0;
        for (Map.Entry<Integer, Integer> edge : G.get(vertexFrom).entrySet()) {
            int vertexTo = edge.getKey();
            if (distTo[vertexFrom] > distTo[vertexTo])
                sum = (sum + dfs(vertexTo, finalVertex)) % MOD;
        }

        return numberOfRestrictedPaths[vertexFrom] = sum;
    }
}


