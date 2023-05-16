package Hard._2290_;

import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

class Solution {
    private PriorityQueue<int[]> workingQueue = new PriorityQueue<>(Comparator.comparingInt(element -> element[0]));
    private int h, w;
    private int[][] dist, grid, directions = { {1, 0}, {-1, 0}, {0, 1}, {0, -1} };
    private boolean withinGrid(int x, int y) {
        return (x >= 0) && (y >= 0) && (x < w) && (y < h);
    }
    private boolean breakCell(int nextX, int nextY) {
        return grid[nextY][nextX] == 1;
    }
    private void init(int[][] grid) {
        this.grid = grid;
        this.h = grid.length;
        this.w = grid[0].length;
        this.dist = new int[h][w];
        for (int i = 0; i < h; i++)
            Arrays.fill(dist[i], Integer.MAX_VALUE);
    }
    private void findShortestPaths() {
        dist[0][0] = grid[0][0];
        workingQueue.add(new int[]{ dist[0][0], 0, 0 });

        while(!workingQueue.isEmpty()) {
            int[] cell = workingQueue.poll();
            int x = cell[1], y = cell[2];

            for (int[] dir: directions) {
                int nextX = dir[0] + x;
                int nextY = dir[1] + y;

                if (withinGrid(nextX, nextY)) {
                    int newDist = breakCell(nextX, nextY) ? dist[y][x] + 1 : dist[y][x];
                    if (newDist < dist[nextY][nextX]) {
                        dist[nextY][nextX] = newDist;
                        workingQueue.add(new int[]{ newDist, nextX, nextY} );
                    }
                }
            }
        }

    }
    public int minimumObstacles(int[][] grid) {
        init(grid);
        findShortestPaths();
        return dist[h - 1][w - 1];
    }
    public static void main(String[] args) {
        int[][] grid = {{0,1,1},{1,1,0},{1,1,0}};
        Solution solution = new Solution();
        System.out.println(solution.minimumObstacles(grid));
    }
}

