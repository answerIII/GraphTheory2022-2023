/**
 * @param {string} bottom
 * @param {string[]} allowed
 * @return {boolean}
 */
let pyramidTransition = function (bottom, allowed) {
  let blocks = {};

  for (let item of allowed) {
    let [i, j, k] = item;
    blocks[i + j] ? blocks[i + j].push(k) : (blocks[i + j] = [k]);
  }

  function dfs(row, top, idx) {
    if (row.length === 1) return true;
    if (idx === row.length - 1) return dfs(top, '', 0);

    let [i, j] = [row[idx], row[idx + 1]];
    let possible = blocks[i + j];

    if (!possible) return false;

    for (let block of possible) {
      if (dfs(row, top + block, idx + 1)) return true;
    }

    return false;
  }

  return dfs(bottom, '', 0);
};
