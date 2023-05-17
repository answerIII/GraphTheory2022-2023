use std::cmp::Ordering;
use std::cmp::Reverse;
use std::cmp::max;
use std::collections::BinaryHeap;

#[derive(Debug)]
struct Item {
    x: usize,
    y: usize,
    el: i32,
}
impl Ord for Item {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.el == other.el {
            Ordering::Equal
        } else if self.el < other.el {
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

fn get_neighbors(grid: &Vec<Vec<i32>>, x: usize, y: usize) -> Vec<(usize, usize)> {
    let mut ans = Vec::new();
    if x > 0 {
        ans.push((x - 1, y));
    }
    if x + 1 < grid.len() {
        ans.push((x + 1, y));
    }
    if y > 0 {
        ans.push((x, y - 1));
    }
    if  y + 1 < grid[0].len() {
        ans.push((x, y + 1));
    }
    ans
}

fn dijkstra(grid: &Vec<Vec<i32>>) -> i32 {
    let mut dist = Vec::with_capacity(grid.len());
    for i in 0..grid.len() {
        dist.push(Vec::with_capacity(grid[0].len()));
        for _ in 0..grid[0].len() {
            dist[i].push(-1);
        }
    }

    let mut heap = BinaryHeap::new();
    heap.push(Reverse(Item { x: 0, y: 0, el: 0 }));

    while heap.is_empty() == false {
        let cur_el: Item = heap.pop().unwrap().0;
        if cur_el.x == grid.len() - 1 && cur_el.y == grid[0].len() - 1 {
            return cur_el.el;
        }
        if dist[cur_el.x][cur_el.y] != -1 {
            continue;
        }

        let neighbors = get_neighbors(grid, cur_el.x, cur_el.y);
        for i in &neighbors {
            if dist[i.0][i.1] == -1 {
                heap.push(Reverse(Item {
                    x: i.0,
                    y: i.1,
                    el: max(
                        cur_el.el + 1,
                        grid[i.0][i.1] + ((grid[i.0][i.1] - cur_el.el) % 2==0) as i32,
                    ),
                }));
            }
        }
        dist[cur_el.x][cur_el.y] = cur_el.el;
    }

    dist[grid.len() - 1][grid[0].len() - 1]
}

impl Solution {
    pub fn minimum_time(grid: Vec<Vec<i32>>) -> i32 {   
        if grid[0][1] > 1 && grid[1][0] > 1 {
            return -1;
        }

        dijkstra(&grid)
    }
}