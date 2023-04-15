use std::cell::RefCell;
use std::rc::Rc;

fn dfs(node: &Option<Rc<RefCell<TreeNode>>>, depth: usize, sums: &mut Vec<i64>) {
    if let Some(x) = node {
        let x = x.borrow();

        if depth >= sums.len() {
            sums.push(0);
        }

        sums[depth] += x.val as i64;

        dfs(&x.left, depth + 1, sums);
        dfs(&x.right, depth + 1, sums);
    }
}

impl Solution {
    pub fn kth_largest_level_sum(root: Option<Rc<RefCell<TreeNode>>>, k: i32) -> i64 {
        let mut sums = Vec::new();

        dfs(&root, 0, &mut sums);

        sums.sort_unstable();
        let idx = sums.len() - k as usize;
        sums.into_iter().nth(idx).unwrap_or(-1)
    }
}
