use std::cmp::Ordering;
struct Item(f64, usize);
impl Ord for Item {
    fn cmp(&self, other: &Self) -> Ordering {
        if (self.0 - other.0) < 0.0000001 {
            Ordering::Equal
        } else if self.0 < other.0 {
            Ordering::Less
        } else {
            Ordering::Greater
        }
    }
}
impl PartialOrd for Item {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
impl PartialEq for Item {
    fn eq(&self, other: &Self) -> bool {
        if self.cmp(other) == Ordering::Equal {
            true
        } else {
            false
        }
    }
}
impl Eq for Item {}

impl Solution {
    pub fn max_probability(
        n: i32,
        edges: Vec<Vec<i32>>,
        succ_prob: Vec<f64>,
        start: i32,
        end: i32,
    ) -> f64 {
        let start = start as usize;
        let end = end as usize;
        let mut graph = Vec::with_capacity(n as usize);
        for _ in 0..n {
            graph.push(Vec::new())
        }

        for (nodes, ves) in edges.iter().zip(succ_prob) {
            let first_node = nodes[0] as usize;
            let second_node = nodes[1] as usize;
            graph[first_node].push((second_node, ves));
            graph[second_node].push((first_node, ves));
        }

        let mut dist = Vec::with_capacity(n as usize);
        for _ in 0..n {
            dist.push((0.0, false));
        }
        dist[start].0 = 1.0;

        let mut heap = std::collections::BinaryHeap::new();
        heap.push(Item(0.0, start));
        while heap.is_empty() == false {
            let cur_item = heap.pop().unwrap();
            if cur_item.1 == end {
                break;
            }
            for i in &graph[cur_item.1] {
                if dist[i.0].1 == false {
                    let tmp = dist[cur_item.1].0 * i.1;
                    let r = &mut dist[i.0].0;
                    if tmp >= *r {
                        *r = tmp;
                        heap.push(Item(*r, i.0));
                    }
                }
            }

            dist[cur_item.1].1 = true;
        }

        dist[end].0
    }
}
