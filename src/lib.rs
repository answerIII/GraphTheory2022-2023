use pyo3::{exceptions, prelude::*, types::PyDict};
use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashMap, HashSet, VecDeque},
    fs::File,
    io::BufRead,
    io::BufReader,
    slice,
    sync::{Arc, Mutex},
    thread,
};

mod sorting;

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
    graph: Arc<HashMap<usize, HashSet<usize>>>,
    threads: usize,
) -> (i32, i32, f64) {
    let diam = Arc::new(Mutex::new(0 as i32));
    let rad = Arc::new(Mutex::new(i32::MAX));
    let dists = Arc::new(Mutex::new(Vec::new()));

    let tmp = mnz
        .get(&root)
        .unwrap()
        .into_iter()
        .map(|&el| el)
        .collect::<Vec<usize>>();
    let mut right = unsafe {
        let tmp = &tmp[..];
        let len = tmp.len();
        let ptr = tmp.as_ptr();
        slice::from_raw_parts(ptr, len)
    };
    let mut d_threads = vec![];

    let per_thread = right.len() / threads;
    for _ in 1..threads + 1 {
        let (left, _r) = right.split_at(per_thread);
        right = _r;
        let cur_graph = Arc::clone(&graph);
        let global_dist = Arc::clone(&dists);
        let global_diam = Arc::clone(&diam);
        let global_rad = Arc::clone(&rad);

        d_threads.push(thread::spawn(move || {
            let mut cur_diam = 0;
            let mut cur_rad = i32::MAX;

            let mut cur_dists: Vec<i32> = vec![];
            for i in left {
                let ans = dijkstra(i, &cur_graph);
                let ans = ans.values().collect::<Vec<_>>();
                let max_val = ans.iter().max().unwrap();
                let tmp = **max_val;
                cur_diam = cur_diam.max(tmp);
                cur_rad = cur_rad.min(tmp);

                cur_dists.extend(ans);
            }

            {
                let mut global_diam = global_diam.lock().unwrap();
                *global_diam = global_diam.max(cur_diam);
            };
            {
                let mut global_rad = global_rad.lock().unwrap();
                *global_rad = global_rad.min(cur_rad);
            };

            {
                let mut dists = global_dist.lock().unwrap();
                dists.extend(cur_dists);
            };
        }));
    }

    for i in d_threads {
        i.join().unwrap();
    }

    let mut dists = dists.lock().unwrap().to_owned();

    let q = 0.9;
    let n = dists.len() as f64;

    sorting::quicksort_multi(&mut dists, threads);

    let k = (q * n - 1.0).floor();
    let q = if k + 1.0 < q * n {
        dists[k as usize + 1] as f64
    } else if (k + 1.0 - q * n).abs() < 1.0 / n {
        (dists[k as usize] + dists[k as usize + 1]) as f64 / 2.0
    } else {
        dists[k as usize] as f64
    };
    let ans = (
        diam.lock().unwrap().to_owned(),
        rad.lock().unwrap().to_owned(),
        q,
    );
    ans
}

// fn drq_full(
//     root: &usize,
//     mnz: &HashMap<usize, HashSet<usize>>,
//     graph: &HashMap<usize, HashSet<usize>>,
//     threads: usize,
// ) -> (i32, i32, f64) {
//     let mut diam = 0;
//     let mut rad = i32::MAX;
//     let mut dists: Vec<i32> = Vec::new();
//     for i in mnz.get(&root).unwrap() {
//         let ans = dijkstra(i, &graph);
//         let ans = ans.values().collect::<Vec<_>>();
//         let max_val = ans.iter().max().unwrap();
//         let tmp = **max_val;
//         diam = max(diam, tmp);
//         rad = min(rad, tmp);
//         dists.extend(ans);
//     }
//     let q = 0.9;
//     let n = dists.len() as f64;
//     sorting::quicksort_multi(&mut dists, threads);
//     let k = (q * n - 1.0).floor();
//     let q = if k + 1.0 < q * n {
//         dists[k as usize + 1] as f64
//     } else if (k + 1.0 - q * n).abs() < 1.0 / n {
//         (dists[k as usize] + dists[k as usize + 1]) as f64 / 2.0
//     } else {
//         dists[k as usize] as f64
//     };
//     (diam, rad, q)
// }

#[pyfunction]
fn find_drq(
    py: Python<'_>,
    graph_path: String,
    threads_count: Option<usize>,
) -> PyResult<(i32, i32, f64)> {
    let threads_count = match threads_count {
        Some(x) => {
            if x < 1 {
                return Err(exceptions::PyValueError::new_err(
                    "threads_count must be > 1",
                ));
            };
            x
        }
        None => 1,
    };

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
    let graph = Arc::new(graph);
    Ok(drq_full(
        &root,
        &mnz,
        Arc::clone(&graph),
        threads_count,
    ))
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
