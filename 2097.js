/**
 * @param {number[][]} pairs
 * @return {number[][]}
 */
var validArrangement = function (pairs) {
  let out = new Map();
  let count = new Map();
  let matrix = new Array();
  for ([left, right] of pairs) {
    if (matrix[left]) {
      matrix[left].push(right);
    } else {
      matrix[left] = [right];
    }
    count.set(left, (count.get(left) || 0) + 1);
    out.set(left, (out.get(left) || 0) + 1);
    out.set(right, (out.get(right) || 0) - 1);
  }
  const curr_path = [];
  const circuit = [];
  let start = pairs[0][0];
  for (const k of out.keys()) {
    if (out.get(k) === 1) {
      start = k;
      break;
    }
  }
  curr_path.push(start);
  let curr_v = start;
  while (curr_path.length) {
    if (count.get(curr_v)) {
      curr_path.push(curr_v);
      const next_v = matrix[curr_v][matrix[curr_v].length - 1];
      count.set(curr_v, count.get(curr_v) - 1);
      matrix[curr_v].pop();
      curr_v = next_v;
    } else {
      circuit.push(curr_v);
      curr_v = curr_path[curr_path.length - 1];
      curr_path.pop();
    }
  }
  let ans = [];
  console.log(circuit);
  for (let i = circuit.length - 1; i > 0; i--) {
    ans.push([circuit[i], circuit[i - 1]]);
  }
  return ans;
};
