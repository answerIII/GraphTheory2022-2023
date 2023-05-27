use pyo3::{exceptions, prelude::*, types::PyDict};
use std::{
    collections::{HashMap, HashSet, VecDeque},
    fs::File,
    io::BufRead,
    io::BufReader,
    slice,
    sync::{Arc, Mutex},
    thread,
    mem::swap
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

fn bfs(root: &usize, graph: &HashMap<usize, HashSet<usize>>) -> Vec<usize> {
    let mut dists = Vec::new();
    let mut q_old = Vec::new();
    let mut q_new = Vec::new();
    let mut visited = HashSet::new();
    
    q_old.push(*root);
    visited.insert(*root);
    
    while !q_old.is_empty() {
        dists.push(q_old.len());
        
        for cur_idx in q_old.iter() {
            
            for neighbor_id in graph.get(&cur_idx).unwrap() {
                if !visited.contains(neighbor_id) {
                    visited.insert(*neighbor_id);
                    q_new.push(*neighbor_id);
                }
            }
        }
        
        q_old.clear();
        swap(&mut q_new, &mut q_old);
    }

    return dists;
}

fn add_dists(base: &mut Vec<usize>, to_add: &mut Vec<usize>) {
    if base.len() < to_add.len() {
        swap(&mut *base, &mut *to_add);
    }
    for idx in 0..to_add.len() {
        base[idx] += to_add[idx];
    }
}

fn drq_full(
    root: &usize,
    mnz: &HashMap<usize, HashSet<usize>>,
    graph: Arc<HashMap<usize, HashSet<usize>>>,
    threads: usize,
) -> (usize, usize, usize) {
    let diam = Arc::new(Mutex::new(0 as usize));
    let rad = Arc::new(Mutex::new(usize::MAX));

    let tmp = mnz
        .get(&root)
        .unwrap()
        .into_iter()
        .map(|&el| el)
        .collect::<Vec<usize>>();

    let dists = Arc::new(Mutex::new(Vec::new()));

    
    let mut right = unsafe {
        let tmp = &tmp[..];
        let len = tmp.len();
        let ptr = tmp.as_ptr();
        slice::from_raw_parts(ptr, len)
    };
    let mut d_threads = Vec::with_capacity(16);

    let mut per_thread = right.len() / threads;
    if per_thread < threads{
        per_thread = right.len();
    }
    for _ in 1..threads + 1 {
        if right.len() == 0{
            break;
        }
        let (left, _r) = right.split_at(per_thread);
        right = _r;
        let cur_graph = Arc::clone(&graph);
        let global_dist = Arc::clone(&dists);
        let global_diam = Arc::clone(&diam);
        let global_rad = Arc::clone(&rad);

        d_threads.push(thread::spawn(move || {
            let mut cur_diam = 0;
            let mut cur_rad = usize::MAX;

            let mut cur_dists: Vec<usize> = Vec::new();
            for i in left {
                let mut ans = bfs(i, &cur_graph);
                let max_val = ans.len() - 1;
                cur_diam = cur_diam.max(max_val);
                cur_rad = cur_rad.min(max_val);
                
                add_dists(&mut cur_dists, &mut ans);
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
                add_dists(&mut dists, &mut cur_dists);
            };
        }));
    }

    for i in d_threads {
        i.join().unwrap();
    }

    let mut dists = dists.lock().unwrap().to_owned();

    let q: f64 = 0.9;
    dists[0] = 0;
    let n = dists.iter().sum::<usize>() as f64;

    let k = (q * n).floor() as usize;
    let mut q = diam.lock().unwrap().to_owned();
    let mut prev_len = 0;
    for (dist, size) in dists.iter().enumerate() {
        prev_len += size;
        if prev_len >= k {
            q = dist;
            break;
        }
    }
    
    let ans = (
        diam.lock().unwrap().to_owned(),
        rad.lock().unwrap().to_owned(),
        q,
    );
    
    return ans;
}

#[pyfunction]
fn find_drq(
    py: Python<'_>,
    graph_path: String,
    threads_count: Option<usize>,
) -> PyResult<(usize, usize, usize)> {
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
