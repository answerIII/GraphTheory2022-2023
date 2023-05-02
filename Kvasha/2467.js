/**
 * @param {number[][]} edges
 * @param {number} bob
 * @param {number[]} amount
 * @return {number}
 */
let mostProfitablePath = function (edges, bob, amount) {
  const N = amount.length;
  let graph = Array.from({ length: N }, (_) => []);
  let visitedBob = new Array(N).fill(Infinity);

  for (let [a, b] of edges) {
    graph[a].push(b);
    graph[b].push(a);
  }

  function dfsBob(idx, prev) {
    if (idx === bob) return [idx, 0];

    for (let next of graph[idx]) {
      if (next !== prev) {
        let [bobNode, bobTime] = dfsBob(next, idx);

        if (bobNode !== null) {
          visitedBob[bobNode] = bobTime;

          return [idx, bobTime + 1];
        }
      }
    }

    return [null, null];
  }

  function dfs(idx, prev, time) {
    let income = -Infinity;
    let bobTime = visitedBob[idx];

    for (let next of graph[idx]) {
      if (next !== prev) {
        income = Math.max(income, dfs(next, idx, time + 1));
      }
    }

    if (income === -Infinity) income = 0;

    if (bobTime > time) {
      return income + amount[idx];
    } else if (bobTime < time) {
      return income;
    } else {
      return income + amount[idx] / 2;
    }
  }

  visitedBob[0] = dfsBob(0, -1)[1];
  return dfs(0, -1, 0);
};
