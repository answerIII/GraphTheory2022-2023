use pyo3::{prelude::*, types::PyDict};
use std::{
    cmp::{max, min, Reverse},
    collections::{BinaryHeap, HashMap, HashSet, VecDeque},
    fs::File,
    io::BufRead,
    io::BufReader,
};

fn dfs(root: &usize, graph: &HashMap<usize, HashSet<usize>>, visited: &mut HashSet<usize>) {
    let mut stack = VecDeque::new();
    visited.insert(*root);
    stack.push_back(*root);

    while !stack.is_empty() {
        let cur_el = stack.pop_back().unwrap();
        for i in graph.get(&cur_el).unwrap() {
            if !visited.contains(i) {
                visited.insert(*i);
                stack.push_back(*i)
            }
        }
    }
}

#[warn(dead_code)]
fn biggest_component_root_old(
    graph: &HashMap<usize, HashSet<usize>>,
    ans: &mut HashMap<usize, HashSet<usize>>,
) -> usize {
    let mut visited = HashSet::new();
    let ids = graph.keys();

    let mut old_len = 0;
    let (mut max_len, mut max_root) = (0, 0);
    for i in ids {
        if visited.contains(i) {
            continue;
        }

        dfs(i, graph, &mut visited);
        if visited.len() - old_len > max_len {
            max_len = visited.len() - old_len;
            max_root = *i;
        }
        old_len = visited.len();
    }
    max_root
}

fn biggest_component_root(
    graph: &HashMap<usize, HashSet<usize>>,
    ans: &mut HashMap<usize, HashSet<usize>>,
) -> usize {
    let mut visited = HashSet::new();
    let ids = graph.keys();
    let mut tmp_set: HashSet<usize> = HashSet::new();

    let (mut max_len, mut max_root) = (0, 0);
    for i in ids {
        if visited.contains(i) {
            continue;
        }

        dfs(i, graph, &mut tmp_set);
        if tmp_set.len() > max_len {
            max_len = tmp_set.len();
            max_root = *i;
        }
        for i in tmp_set.iter() {
            visited.insert(*i);
        }
        ans.insert(*i, tmp_set);
        tmp_set = HashSet::new();
    }
    max_root
}

fn dijkstra(root: &usize, graph: &HashMap<usize, HashSet<usize>>) -> HashMap<usize, i32> {
    let mut dist = HashMap::new();
    let mut heap = BinaryHeap::new();
    heap.push(Reverse((0, *root)));
    let mut visited = HashSet::new();
    while !heap.is_empty() {
        let (cur_len, cur_idx) = heap.pop().unwrap().0;
        if visited.contains(&cur_idx) {
            continue;
        }
        visited.insert(cur_idx);

        for i in graph.get(&cur_idx).unwrap() {
            let new_len = cur_len + 1;
            if *dist.entry(*i).or_insert(i32::MAX) > new_len {
                dist.entry(*i)
                    .and_modify(|el| *el = new_len)
                    .or_insert(new_len);
                heap.push(Reverse((new_len, *i)));
            }
        }
    }

    return dist;
}

fn drq_full(
    root: &usize,
    mnz: &HashMap<usize, HashSet<usize>>,
    graph: &HashMap<usize, HashSet<usize>>,
) -> (i32, i32, f64) {
    let mut diam = 0;
    let mut rad = i32::MAX;
    let mut dists: Vec<i32> = Vec::new();
    for i in mnz.get(&root).unwrap() {
        let ans = dijkstra(i, &graph);

        let ans = ans.values().collect::<Vec<_>>();
        let max_val = ans.iter().max().unwrap();
        let tmp = **max_val;
        diam = max(diam, tmp);
        rad = min(rad, tmp);

        dists.extend(ans);
    }

    let q = 0.9;
    let n = dists.len() as f64;
    dists.sort();
    let k = (q * n - 1.0).floor();
    let q = if k + 1.0 < q * n {
        dists[k as usize + 1] as f64
    } else if (k + 1.0 - q * n).abs() < 1.0 / n {
        (dists[k as usize] + dists[k as usize + 1]) as f64 / 2.0
    } else {
        dists[k as usize] as f64
    };
    (diam, rad, q)
}

#[pyfunction]
fn find_drq(
    py: Python<'_>,
    graph_path: String,
    big: Option<(i32, i32)>,
) -> PyResult<Vec<(i32, i32, f64)>> {
    let mut graph: HashMap<usize, HashSet<usize>> = HashMap::new();

    let reader = BufReader::new(File::open(graph_path)?);
    let lines = reader.lines();
    for line in lines {
        let line = line?;
        if line.starts_with("%") {
            continue;
        }

        let line = line.split_ascii_whitespace().collect::<Vec<_>>();
        let (from, to) = (line[0].parse()?, line[1].parse()?);
        graph.entry(from).or_insert(HashSet::new()).insert(to);
        graph.entry(to).or_insert(HashSet::new()).insert(from);
    }

    let mut mnz = HashMap::new();

    let root = biggest_component_root(&graph, &mut mnz);
    // let mut diam = 0;
    // let mut rad = i32::MAX;
    // let mut dists: Vec<i32> = Vec::new();
    // for i in mnz.get(&root).unwrap() {
    //     let ans = dijkstra(i, &graph);
    //     let ans = ans.values().collect::<Vec<_>>();
    //     let max_val = ans.iter().max().unwrap();
    //     let tmp = **max_val;
    //     diam = max(diam, tmp);
    //     rad = min(rad, tmp);

    //     dists.extend(ans);
    // }

    // let q = 0.9;
    // let N = dists.len() as f64;
    // dists.sort();
    // let k = (q * N - 1.0).floor();
    // let q = if k + 1.0 < q * N {
    //     dists[k as usize + 1] as f64
    // } else if (k + 1.0 - q * N).abs() < 1.0 / N {
    //     (dists[k as usize] + dists[k as usize + 1]) as f64 / 2.0
    // } else {
    //     dists[k as usize] as f64
    // };

    Ok(vec![drq_full(&root, &mnz, &graph)])
}

#[pyfunction]
fn test(py: Python<'_>, d: PyObject, key: PyObject) -> PyResult<String> {
    let nodes = d.downcast::<PyDict>(py)?;

    Ok(nodes.get_item(key).to_object(py).to_string())
}

#[pymodule]
fn drq(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(find_drq, m)?)?;
    m.add_function(wrap_pyfunction!(test, m)?)?;

    Ok(())
}
