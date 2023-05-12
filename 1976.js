var countPaths = function (n, roads) {
  let matrix = new Array(n).fill(null);
  for (let i = 0; i < n; i++) {
    matrix[i] = new Array();
  }
  for (let i = 0; i < roads.length; i++) {
    matrix[roads[i][0]].push([roads[i][1], roads[i][2]]);
    matrix[roads[i][1]].push([roads[i][0], roads[i][2]]);
  }

  const distance = new Array(n).fill(Infinity);
  const ways = new Array(n).fill(0);
  ways[n - 1] = 1;
  distance[n - 1] = 0;
  const heap = new MinPriorityQueue({ priority: (x) => x[1] });
  heap.enqueue([n - 1, 0]);
  while (heap.size()) {
    const [n, cost] = heap.dequeue().element;
    for (let [nextNode, w] of matrix[n]) {
      const total = cost + w;
      if (distance[nextNode] == total) {
        ways[nextNode] = (ways[nextNode] + ways[n]) % 1000000007;
      } else if (distance[nextNode] > total) {
        distance[nextNode] = total;
        ways[nextNode] = ways[n];
        heap.enqueue([nextNode, total]);
      }
    }
  }

  return ways[0];
};
