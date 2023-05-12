let testCases = [
  {
    source: [1, 2, 3, 4],
    target: [2, 1, 4, 5],
    allowedSwaps: [
      [0, 1],
      [2, 3],
    ],
  },
];

class Union {
  constructor(n) {
    this.parent = new Array(n);
    for (let i = 0; i < n; i++) {
      this.parent[i] = i;
    }
  }

  findParent(v) {
    return (this.parent[v] =
      this.parent[v] == v ? v : this.findParent(this.parent[v]));
  }

  union(v, u) {
    let pv = this.findParent(v);
    let pu = this.findParent(u);
    if (pv != pu) this.parent[pv] = pu;
  }
}
class Multiset {
  _backing = new Map();
  add(value) {
    if (this._backing.has(value)) {
      this._backing.set(value, 1 + this._backing.get(value));
    } else {
      this._backing.set(value, 1);
    }
  }

  delete(value) {
    if (this._backing.get(value) > 0) {
      this._backing.set(value, this._backing.get(value) - 1);
    } else {
    }
  }

  get(value) {
    if (this._backing.get(value) > 0) {
      return this._backing.get(value);
    } else {
      return 0;
    }
  }
}

var minimumHammingDistance = function (source, target, allowedSwaps) {
  let un = new Union(source.length);
  let result = 0;
  let map = new Map();
  allowedSwaps.forEach((item) => un.union(item[0], item[1]));
  for (let i = 0; i < source.length; i++) {
    map.set(un.findParent(i), new Multiset());
  }
  for (let i = 0; i < source.length; i++) {
    map.get(un.findParent(i)).add(source[i]);
  }
  for (let i = 0; i < source.length; i++) {
    if (!map.get(un.findParent(i)).get(target[i])) result++;
    else map.get(un.findParent(i)).delete(target[i]);
  }
  return result;
};

for (let i = 0; i < 1; i++) {
  console.log(
    minimumHammingDistance(
      testCases[i].source,
      testCases[i].target,
      testCases[i].allowedSwaps
    )
  );
}
