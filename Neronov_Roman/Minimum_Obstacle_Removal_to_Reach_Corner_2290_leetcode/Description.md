# Minimum Obstacle Removal to Reach Corner
(https://leetcode.com/problems/minimum-obstacle-removal-to-reach-corner/)

You are given a 0-indexed 2D integer array grid of size m x n. Each cell has one of two values:

* 0 represents an empty cell,
* 1 represents an obstacle that may be removed.

You can move up, down, left, or right from and to an empty cell.

Return the minimum number of obstacles to remove so you can move from the upper left corner (0, 0) to the lower right corner (m - 1, n - 1).

## Example 1:

![image](https://user-images.githubusercontent.com/94119476/235195862-ea4614fa-f6cf-438d-a185-f67ec92dd24c.png)

Input: grid = [[0,1,1],[1,1,0],[1,1,0]]

Output: 2

Explanation: We can remove the obstacles at (0, 1) and (0, 2) to create a path from (0, 0) to (2, 2).

It can be shown that we need to remove at least 2 obstacles, so we return 2.

Note that there may be other ways to remove 2 obstacles to create a path.

## Example 2:

![image](https://user-images.githubusercontent.com/94119476/235195976-d763d4a3-75a0-42fd-95a6-d9e74d29c7ee.png)

Input: grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]

Output: 0

Explanation: We can move from (0, 0) to (2, 4) without removing any obstacles, so we return 0.

## Constraints:

* m == grid.length
* n == grid[i].length
* 1 <= m, n <= 10^{5}
* 2 <= m * n <= 10^{5}
* grid[i][j] is either 0 or 1.
* grid[0][0] == grid[m - 1][n - 1] == 0
