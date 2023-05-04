# Check Knight Tour Configuration
(https://leetcode.com/problems/check-knight-tour-configuration/)

There is a knight on an n x n chessboard. In a valid configuration, the knight starts at the top-left cell of the board and visits every cell on the board exactly once.

You are given an n x n integer matrix grid consisting of distinct integers from the range [0, n * n - 1] where grid[row][col] indicates that the cell (row, col) is the grid[row][col]th cell that the knight visited. The moves are 0-indexed.

Return true if grid represents a valid configuration of the knight's movements or false otherwise.

Note that a valid knight move consists of moving two squares vertically and one square horizontally, or two squares horizontally and one square vertically. The figure below illustrates all the possible eight moves of a knight from some cell.

![image](https://user-images.githubusercontent.com/94119476/235186922-cbc3eee6-14ce-4bc5-8417-b9398a9f39c2.png)

## Example 1:

![image](https://user-images.githubusercontent.com/94119476/235186941-5c612864-fc66-432f-adf0-175cdc2a4eed.png)

Input: grid = [[0,11,16,5,20],[17,4,19,10,15],[12,1,8,21,6],[3,18,23,14,9],[24,13,2,7,22]]

Output: true

Explanation: The above diagram represents the grid. It can be shown that it is a valid configuration.

## Example 2:

![image](https://user-images.githubusercontent.com/94119476/235186959-375c6ef1-3069-4da6-b444-1773356dc7e0.png)

Input: grid = [[0,3,6],[5,8,1],[2,7,4]]

Output: false

Explanation: The above diagram represents the grid. The 8th move of the knight is not valid considering its position after the 7th move.
 
## Constraints:

* n == grid.length == grid[i].length
* 3 <= n <= 7
* 0 <= grid[row][col] < n * n
* All integers in grid are unique.
