/**
 * @param {number[][]} bombs
 * @return {number}
 */
let maximumDetonation = function (bombs) {
  const N = bombs.length;
  let graph = Array.from({ length: N }, (_) => []);
  let visited = new Array(N).fill(false);
  let result = 0;

  for (let i = 0; i < N - 1; ++i) {
    for (let j = i; j < N; ++j) {
      let [x_i, y_i, r_i] = bombs[i];
      let [x_j, y_j, r_j] = bombs[j];

      let d = Math.sqrt((x_i - x_j) ** 2 + (y_i - y_j) ** 2);

      if (r_i >= d) graph[i].push(j);
      if (r_j >= d) graph[j].push(i);
    }
  }

  function dfs(idx, visited) {
    visited[idx] = true;
    let currCount = 1;

    for (let bomb of graph[idx]) {
      if (!visited[bomb]) currCount += dfs(bomb, visited);
    }

    return currCount;
  }

  for (let i = 0; i < N; ++i) {
    visited.fill(false);
    result = Math.max(result, dfs(i, visited));
  }

  return result;
};
