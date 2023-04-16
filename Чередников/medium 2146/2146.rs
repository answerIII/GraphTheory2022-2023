use std::cmp::Ordering;
use std::cmp::max;
use std::collections::{BinaryHeap, VecDeque};

struct Item {
    x: usize,
    y: usize,
    price: i32,
    distanse: usize,
}

impl Ord for Item {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.distanse == other.distanse {
            if self.price == other.price {
                if self.x == other.x {
                    if self.y == other.y {
                        Ordering::Equal
                    } else if self.y < other.y {
                        Ordering::Greater
                    } else {
                        Ordering::Less
                    }
                } else if self.x < other.x {
                    Ordering::Greater
                } else {
                    Ordering::Less
                }
            } else if self.price < other.price {
                Ordering::Greater
            } else {
                Ordering::Less
            }
        } else if self.distanse < other.distanse {
            Ordering::Greater
        } else {
            Ordering::Less
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

fn bfs(
    grid: &mut Vec<Vec<i32>>,
    start: (usize, usize),
    min_cost: i32,
    max_cost: i32,
    k: i32,
) -> Vec<Vec<i32>> {
    let mut queue = VecDeque::new();
    let mut heap = BinaryHeap::new();

    queue.push_back(Item {
        x: start.0,
        y: start.1,
        price: grid[start.0][start.1],
        distanse: 0,
    });
    grid[start.0][start.1] = -1;
    while queue.is_empty() == false {
        let cur_el = queue.pop_front().unwrap();
        if cur_el.x > 0 {
            if grid[cur_el.x - 1][cur_el.y] > 0 {
                queue.push_back(Item {
                    x: cur_el.x - 1,
                    y: cur_el.y,
                    price: grid[cur_el.x - 1][cur_el.y],
                    distanse: cur_el.distanse + 1,
                });
                grid[cur_el.x - 1][cur_el.y] = -1;
            }
        }
        if cur_el.x < grid.len() - 1 {
            if grid[cur_el.x + 1][cur_el.y] > 0 {
                queue.push_back(Item {
                    x: cur_el.x + 1,
                    y: cur_el.y,
                    price: grid[cur_el.x + 1][cur_el.y],
                    distanse: cur_el.distanse + 1,
                });
                grid[cur_el.x + 1][cur_el.y] = -1;
            }
        }
        if cur_el.y > 0 {
            if grid[cur_el.x][cur_el.y - 1] > 0 {
                queue.push_back(Item {
                    x: cur_el.x,
                    y: cur_el.y - 1,
                    price: grid[cur_el.x][cur_el.y - 1],
                    distanse: cur_el.distanse + 1,
                });
                grid[cur_el.x][cur_el.y - 1] = -1;
            }
        }
        if cur_el.y < grid[0].len() - 1 {
            if grid[cur_el.x][cur_el.y + 1] > 0 {
                queue.push_back(Item {
                    x: cur_el.x,
                    y: cur_el.y + 1,
                    price: grid[cur_el.x][cur_el.y + 1],
                    distanse: cur_el.distanse + 1,
                });
                grid[cur_el.x][cur_el.y + 1] = -1;
            }
        }
        if cur_el.price <= max_cost && cur_el.price >= min_cost {
            heap.push(cur_el);
        }
    }

    let a = heap.into_sorted_vec();
    a.iter()
        .skip(max(0, a.len() as i32 - k) as usize)
        .rev()
        .map(|el| {
            let mut tmp = Vec::new();
            tmp.push(el.x as i32);
            tmp.push(el.y as i32);
            tmp
        })
        .collect::<Vec<_>>()
}


impl Solution {
    pub fn highest_ranked_k_items(
        grid: Vec<Vec<i32>>,
        pricing: Vec<i32>,
        start: Vec<i32>,
        k: i32,
    ) -> Vec<Vec<i32>> {
        let start_x = start[0] as usize;
        let start_y = start[1] as usize;
        let mut grid = grid;
        bfs(&mut grid, (start_x, start_y), pricing[0], pricing[1], k)
    }
}