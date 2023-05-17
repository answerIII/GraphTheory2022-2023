use std::cell::RefCell;
use std::cmp::max;
use std::collections::HashMap;
use std::rc::Rc;

fn init_bfs(root: &Rc<RefCell<TreeNode>>, graph: &mut HashMap<usize, Vec<usize>>) {
    graph
        .entry(root.borrow().val as usize)
        .or_insert(Vec::new());
    if let Some(el) = &root.borrow().left {
        graph.get_mut(&(root.borrow().val as usize)).unwrap().push(el.borrow().val as usize);
        graph
            .entry(el.borrow().val as usize)
            .or_insert(Vec::new())
            .push(root.borrow().val as usize);
        init_bfs(el, graph)
    };
    if let Some(el) = &root.borrow().right {
        graph.get_mut(&(root.borrow().val as usize)).unwrap().push(el.borrow().val as usize);
        graph
            .entry(el.borrow().val as usize)
            .or_insert(Vec::new())
            .push(root.borrow().val as usize);
        init_bfs(el, graph)
    };
}

fn bfs_infection(
    root: &usize,
    graph: &HashMap<usize, Vec<usize>>,
    visited: &mut HashMap<usize, bool>,
    level: i32,
) -> i32 {
    let mut ans = level;
    visited.insert(*root, true);
    for i in graph.get(root).unwrap() {
        if *visited.get(i).unwrap_or(&false) == false {
            ans = max(ans, bfs_infection(i, graph, visited, level + 1));
        }
    }

    ans
}

impl Solution {
    pub fn amount_of_time(root: Option<Rc<RefCell<TreeNode>>>, start: i32) -> i32 {
        let root = root.unwrap();
        let mut graph = HashMap::new();
        init_bfs(&root, &mut graph);
        let mut visited = HashMap::new();
        let x = bfs_infection(&(start as usize), &graph, &mut visited, 0);
        x
    }
}