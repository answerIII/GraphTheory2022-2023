/**
 * @param {number[][]} grid
 * @return {number}
 */
let minimumObstacles = function (grid) {
  const m = grid.length;
  const n = grid[0].length;

  const dir = [
    [0, 1],
    [0, -1],
    [-1, 0],
    [1, 0],
  ];

  const visited = Array.from({ length: m }, () => new Array(n).fill(false));
  visited[0][0] = true;

  let queue = new MinPriorityQueue({ priority: (x) => x[2] });
  queue.enqueue([0, 0, 0]);

  while (!queue.isEmpty()) {
    let [x, y, blocks] = queue.dequeue().element;

    if (x === m - 1 && y === n - 1) return blocks;

    for (let [i, j] of dir) {
      nextX = x + i;
      nextY = y + j;

      if (nextX >= 0 && nextX < m && nextY >= 0 && nextY < n && !visited[nextX][nextY]) {
        visited[nextX][nextY] = true;
        newBlocks = blocks + grid[nextX][nextY];
        queue.enqueue([nextX, nextY, newBlocks]);
      }
    }
  }
};
