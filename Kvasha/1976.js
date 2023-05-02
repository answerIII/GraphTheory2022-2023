/**
 * @param {number} n
 * @param {number[][]} roads
 * @return {number}
 */
let countPaths = function (n, roads) {
  const MAX = Number.MAX_SAFE_INTEGER;
  const MOD = 1e9 + 7;
  let graph = Array.from({ length: n }, (_) => []);

  for (let [u, v, time] of roads) {
    graph[u].push([v, time]);
    graph[v].push([u, time]);
  }

  function dijkstraWithCount(src, to) {
    let dist = new Array(n).fill(MAX);
    let paths = new Array(n).fill(0);
    let queue = new MinPriorityQueue({ priority: (x) => x[0] });

    dist[src] = 0;
    paths[src] = 1;
    queue.enqueue([0, src]);

    while (!queue.isEmpty()) {
      let [d, u] = queue.dequeue().element;

      if (dist[u] !== d) continue;

      for (let [v, time] of graph[u]) {
        let newTime = d + time;

        if (newTime === dist[v]) {
          paths[v] = (paths[v] + paths[u]) % MOD;
        } else if (newTime < dist[v]) {
          dist[v] = newTime;
          paths[v] = paths[u];
          queue.enqueue([dist[v], v]);
        }
      }
    }

    return paths[to];
  }

  return dijkstraWithCount(0, n - 1);
};
