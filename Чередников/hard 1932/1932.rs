use std::cell::RefCell;
use std::collections::{HashMap, VecDeque};
use std::rc::Rc;

const INF: i32 = 1_000_000;
impl Solution {
    pub fn can_merge(trees: Vec<Option<Rc<RefCell<TreeNode>>>>) -> Option<Rc<RefCell<TreeNode>>> {
        let mut roots = HashMap::new();
        let mut counts = HashMap::new();

        for i in &trees {
            let node = i.clone().unwrap();

            let node = Rc::clone(&node);
            let node2 = Rc::clone(&node);
            roots.insert(node.borrow().val, node2);

            if let Some(el) = &node.borrow().left {
                counts.insert(el.borrow().val, 1);
            };
            if let Some(el) = &node.borrow().right {
                counts.insert(el.borrow().val, 1);
            };
        }

        let mut root = None;

        for i in trees {
            let i = i.unwrap();
            if counts.get(&i.borrow().val).is_none() {
                match root {
                    None => root = Some(i),
                    Some(_) => {
                        println!("4");
                        return None;
                    }
                }
            }
        }

        if root.is_none() {
            return None;
        }

        let mut queue = VecDeque::new();
        queue.push_back((root.clone().unwrap(), -INF, INF));
        while queue.is_empty() == false {
            let (node, min, max) = queue.pop_front().unwrap();
            if !(min < node.borrow().val && node.borrow().val < max) {
                return None;
            }

            let mut node = node.borrow_mut();

            if let Some(el) = &node.left {
                let el = Rc::clone(el);
                if let Some(root) = roots.get(&el.borrow().val) {
                    node.left = Some(Rc::clone(root));
                    roots.remove(&el.borrow().val); // !!!!!!!!!!!!!!!!
                };
                queue.push_back((node.left.clone().unwrap(), min, node.val));
            };

            if let Some(el) = &node.right {
                let el = Rc::clone(el);
                if let Some(root) = roots.get(&el.borrow().val) {
                    node.right = Some(Rc::clone(root));
                    roots.remove(&el.borrow().val); // !!!!!!!!!!!!!!!!
                };
                queue.push_back((node.right.clone().unwrap(), node.val, max));
            };
        }

        if roots.len() == 1 {
            root
        } else {
            None
        }
    }
}