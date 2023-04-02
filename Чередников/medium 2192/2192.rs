use std::collections::HashSet;

fn dfs(input_edges: &Vec<Vec<usize>>, vertex: usize, store: &mut Vec<HashSet<i32>>) {
    if store[vertex].is_empty() == false {
        return;
    }

    if input_edges[vertex].len() == 0 {
        return;
    }
    for i in &input_edges[vertex] {
        store[vertex].insert(*i as i32);
        dfs(input_edges, *i, store);
        store[vertex] = store[vertex].union(&store[*i]).map(|&el| el).collect()
    }
}

impl Solution {
    pub fn get_ancestors(n: i32, edges: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
        let n = n as usize;
        let mut graph = vec![vec![]; n];
        for edge in &edges {
            let out = edge[0] as usize;
            let input = edge[1] as usize;
            graph[input].push(out);
        }

        let mut store: Vec<HashSet<i32>> = Vec::new();
        for _ in 0..n {
            store.push(HashSet::new())
        }
        for i in 0..n {
            dfs(&graph, i, &mut store)
        }

        let ans = store
            .iter()
            .map(|el| {
                let mut tmp = el.iter().map(|&n| n).collect::<Vec<_>>();
                tmp.sort();
                tmp
            })
            .collect::<Vec<_>>();

        return ans;
    }
}
