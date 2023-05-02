/**
 * @param {number} n
 * @param {number} m
 * @param {number[]} group
 * @param {number[][]} beforeItems
 * @return {number[]}
 */
let sortItems = function (n, m, group, beforeItems) {
  let graph = new Array(m).fill(0).map((_) => []);
  let visited = new Array(n).fill(0);
  let visitedGroups = new Array(m).fill(0);
  let result = [];

  for (let i = 0; i < n; ++i) {
    if (group[i] !== -1) graph[group[i]].push(i);
  }

  function dfs(item, groupId) {
    if (visited[item] === 1) return false;
    if (visited[item] === 2) return true;

    visited[item] = 1;

    for (let before of beforeItems[item]) {
      if (group[before] !== groupId) continue;
      if (!dfs(before, groupId)) return false;
    }

    visited[item] = 2;
    result.push(item);
    return true;
  }

  function sortGroup(groupId) {
    if (visitedGroups[groupId] === 1) return false;
    if (visitedGroups[groupId] === 2) return true;

    visitedGroups[groupId] = 1;

    for (let item of graph[groupId]) {
      for (let before of beforeItems[item]) {
        if (group[before] === -1 && !addNoGroup(before)) return false;
        if (group[before] > -1 && group[before] !== groupId && !sortGroup(group[before])) return false;
      }
    }

    for (let item of graph[groupId]) {
      if (!dfs(item, groupId)) return false;
    }

    visitedGroups[groupId] = 2;
    return true;
  }

  function addNoGroup(item) {
    if (visited[item] === 1) return false;
    if (visited[item] === 2) return true;

    visited[item] = 1;

    for (let before of beforeItems[item]) {
      if (group[before] === -1 && !addNoGroup(before)) return false;
      if (group[before] > -1 && !sortGroup(group[before])) return false;
    }

    visited[item] = 2;
    result.push(item);
    return true;
  }

  for (let i = 0; i < n; ++i) {
    if (group[i] !== -1 && !sortGroup(group[i])) return [];
    if (group[i] === -1 && !addNoGroup(i)) return [];
  }

  return result;
};
