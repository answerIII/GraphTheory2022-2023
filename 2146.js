class Queue1 {
  constructor() {
    this._oldestIndex = 1;
    this._newestIndex = 1;
    this._storage = {};
  }
  size() {
    return this._newestIndex - this._oldestIndex;
  }
  enqueue(data) {
    this._storage[this._newestIndex] = data;
    this._newestIndex++;
  }
  dequeue() {
    var oldestIndex = this._oldestIndex,
      newestIndex = this._newestIndex,
      deletedData;
    if (oldestIndex !== newestIndex) {
      deletedData = this._storage[oldestIndex];
      delete this._storage[oldestIndex];
      this._oldestIndex++;
      return deletedData;
    }
  }
}

var highestRankedKItems = function (grid, pricing, start, k) {
  let res = [];

  const sdvig = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
  ];
  let m = grid.length;
  let n = grid[0].length;
  let arr = [];
  let queue = new Queue1();
  queue.enqueue({
    steps: 0,
    i: start[0],
    j: start[1],
    price: grid[start[0]][start[1]],
  });

  const notOutOfRange = (arr, i, j) => {
    return i >= 0 && j >= 0 && i < arr.length && j < arr[0].length;
  };

  while (queue.size()) {
    let temp = queue.dequeue();

    let { steps, i, j, price } = temp;

    if (price >= pricing[0] && price <= pricing[1]) {
      arr.push(temp);
    }
    grid[i][j] = 0;

    for (let item of sdvig) {
      let nextX = i + item[0],
        nextY = j + item[1];

      if (!notOutOfRange(grid, nextX, nextY) || grid[nextX][nextY] === 0)
        continue;

      queue.enqueue({
        steps: steps + 1,
        i: nextX,
        j: nextY,
        price: grid[nextX][nextY],
      });
      grid[nextX][nextY] = 0;
    }
  }

  arr.sort(function (a, b) {
    if (a.price === b.price && a.steps === b.steps && a.i === b.i) {
      return a.j - b.j;
    }
    if (a.price === b.price && a.steps === b.steps) {
      return a.i - b.i;
    }
    if (a.steps === b.steps) {
      return a.price - b.price;
    }
    return a.steps - b.steps;
  });

  for (let i = 0; i < k; i++) {
    if (arr[i]) res.push([arr[i].i, arr[i].j]);
  }

  return res;
};
