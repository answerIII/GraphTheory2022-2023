/**
 * @param {number} n
 * @param {number[][]} edges
 * @param {number} distanceThreshold
 * @return {number}
 */
let findTheCity = function (n, edges, distanceThreshold) {
  const MAX = 1e4 + 1;
  let D = Array.from({ length: n }, (_) => new Uint16Array(n).fill(MAX));
  let children = n - 1;
  let result = 0;

  for (let [u, v, w] of edges) {
    D[u][v] = D[v][u] = w;
  }

  for (let i = 0; i < n; ++i) {
    for (let u = 0; u < n; ++u) {
      if (D[u][i] === MAX) continue;

      for (let v = 0; v < n; ++v) {
        if (u === v) continue;

        D[u][v] = Math.min(D[u][v], D[u][i] + D[i][v]);
      }
    }
  }

  for (let i = 0; i < n; ++i) {
    let currChildren = 0;

    for (let j = 0; j < n; ++j) {
      currChildren += D[i][j] <= distanceThreshold;
    }

    if (currChildren <= children) {
      children = currChildren;
      result = i;
    }
  }

  return result;
};
