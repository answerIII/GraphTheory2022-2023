use std::{cell::RefCell, rc::Rc, vec};
#[derive(Debug)]
struct LockingTree {
    locks: Vec<i32>,
    children: Vec<Vec<i32>>,
    parents: Vec<i32>,
}

impl LockingTree {
    fn new(parent: Vec<i32>) -> Self {
        let mut ans = LockingTree {
            locks: Vec::with_capacity(parent.len()),
            children: Vec::with_capacity(parent.len()),
            parents: Vec::with_capacity(parent.len()),
        };
        let mut iter = parent.iter().enumerate();
        iter.next();
        for i in 0..parent.len(){
            ans.locks.push(0);
            ans.parents.push(-1);
            x
        }
        for (idx, i) in iter {
            ans.children[*i as usize].push(idx as i32);
            ans.parents[idx] = *i;
            ans.locks[idx] = 0;
        }

        ans
    }

    fn lock(&mut self, num: i32, user: i32) -> bool {
        let num = num as usize;
        if self.locks[num] == 0 {
            self.locks[num] = user;
            true
        } else {
            false
        }
    }

    fn unlock(&mut self, num: i32, user: i32) -> bool {
        let num = num as usize;
        if self.locks[num] == user {
            self.locks[num] = 0;
            true
        } else {
            false
        }
    }

    fn upgrade(&mut self, num: i32, user: i32) -> bool {
        let num = num as usize;
        if self.locks[num] != 0 {
            return false;
        }
        if self.dfs_parent_check(num as i32) == false {
            return false;
        }
        if self.dfs_children_check(num as i32) == false {
            return false;
        }
        self.dfs_children_unlock(num as i32);
        self.locks[num] = user;
        true
    }
    fn dfs_parent_check(&self, num: i32) -> bool {
        let num = num as usize;

        if num as i32 == -1 {
            true
        } else if self.locks[num] != 0 {
            false
        } else {
            self.dfs_parent_check(self.parents[num])
        }
    }

    fn dfs_children_check(&self, num: i32) -> bool {
        let num = num as usize;
        if self.locks[num] != 0 {
            return true;
        }
        self.children[num]
            .iter()
            .map(|el| self.dfs_children_check(*el))
            .any(|el| el == true)
    }

    fn dfs_children_unlock(&mut self, num: i32) {
        let num = num as usize;
        self.locks[num] = 0;
        for i in 0..self.children[num].len() {
            self.dfs_children_unlock(self.children[num][i]);
        }
    }
}