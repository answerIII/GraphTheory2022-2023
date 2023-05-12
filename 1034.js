let testCases = [
  {
    grid: [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
    ],
    row: 1,
    col: 1,
    color: 2,
  },
];

var colorBorder = function (grid, row, col, color) {
  let currentColor = grid[row][col];
  hash = new Set();
  let queue = [];
  let neighbors = [];
  queue.push([row, col]);
  while (queue.length > 0) {
    let v = queue.shift();
    neighbors = [
      [v[0], v[1] - 1],
      [v[0], v[1] + 1],
      [v[0] + 1, v[1]],
      [v[0] - 1, v[1]],
    ];
    for (let neighbor of neighbors) {
      if (
        !hash.has(neighbor) &&
        grid[neighbor[0]]?.[neighbor[1]] !== currentColor
      ) {
        console.log(neighbor);
        grid[v[0]][v[1]] = color;
      } else if (
        !hash.has(neighbor) &&
        grid[neighbor[0]]?.[neighbor[1]] === currentColor
      ) {
        queue.push(neighbor);
      }
    }
    hash.add(v);
  }
  return grid;
};

for (let i = 0; i < 1; i++) {
  console.log(
    colorBorder(
      testCases[i].grid,
      testCases[i].row,
      testCases[i].col,
      testCases[i].color
    )
  );
}
