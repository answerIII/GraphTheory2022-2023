/**
 * @param {character[][]} grid
 * @return {boolean}
 */
let containsCycle = function (grid) {
  const m = grid.length;
  const n = grid[0].length;
  let visited = new Array(m).fill(0).map((_) => new Array(n));

  const dir = {
    left: { i: 0, j: -1 },
    right: { i: 0, j: 1 },
    up: { i: -1, j: 0 },
    down: { i: 1, j: 0 },
  };

  const dirPrev = {
    left: 'right',
    right: 'left',
    up: 'down',
    down: 'up',
  };

  function dfs(row, col, prev = '') {
    if (visited[row][col]) return true;

    visited[row][col] = true;

    for (let d in dir) {
      if (d === prev) continue;

      let i = row + dir[d].i;
      let j = col + dir[d].j;

      if (i > -1 && i < m && j > -1 && j < n) {
        if (grid[row][col] === grid[i][j] && dfs(i, j, dirPrev[d])) return true;
      }
    }

    visited[row][col] = false;
    return false;
  }

  for (let i = 0; i < m; ++i) {
    for (let j = 0; j < n; ++j) {
      if (visited[i][j] === false) continue;
      if (dfs(i, j)) return true;
    }
  }

  return false;
};
