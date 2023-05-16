package Hard._1368_;

import java.util.Arrays;
import java.util.LinkedList;

class Solution {
    LinkedList<int[]> workingQueue = new LinkedList<>();
    private int h, w;
    private boolean[][] visited;
    private int[][] dist, grid, directions = { {1, 0}, {-1, 0}, {0, 1}, {0, -1} };
    private boolean withinGrid(int x, int y) {
        return (x >= 0) && (y >= 0) && (x < w) && (y < h);
    }
    private boolean changeDirection(int x, int y, int nextX, int nextY) {
        int[] dir = directions[grid[y][x] - 1];
        int validX = x + dir[0], validY = y + dir[1];
        return (validX != nextX) || (validY != nextY);
    }
    private void init(int[][] grid) {
        this.grid = grid;
        this.h = grid.length;
        this.w = grid[0].length;
        this.visited = new boolean[h][w];
        this.dist = new int[h][w];
        for (int i = 0; i < h; i++)
            Arrays.fill(dist[i], Integer.MAX_VALUE);
    }
    private void findShortestPaths() {
        workingQueue.add(new int[]{ 0, 0 });
        dist[0][0] = 0;

        while(!workingQueue.isEmpty()) {
            int[] cell = workingQueue.poll();
            int x = cell[0], y = cell[1];

            for (int[] dir: directions) {
                int nextX = dir[0] + x;
                int nextY = dir[1] + y;

                if (withinGrid(nextX, nextY) && !visited[nextY][nextX]) {
                    int newDist = dist[y][x];
                    int queuePosition = 0;

                    if (changeDirection(x, y, nextX, nextY)) {
                        newDist += 1;
                        queuePosition = workingQueue.size();
                    }

                    workingQueue.add(queuePosition, new int[]{ nextX, nextY });
                    dist[nextY][nextX] = Math.min(dist[nextY][nextX], newDist);
                }
            }
            visited[y][x] = true;
        }

    }
    public int minCost(int[][] grid) {
        init(grid);
        findShortestPaths();
        return dist[h - 1][w - 1];
    }
    public static void main(String[] args) {
        int[][] grid = {{1,1,3},{3,2,2},{1,1,4}};
        Solution solution = new Solution();
        System.out.println(solution.minCost(grid));
    }
}
