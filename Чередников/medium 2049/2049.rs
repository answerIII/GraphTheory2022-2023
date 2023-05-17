fn dfs(
    graph: &Vec<Vec<usize>>,
    node: &usize,
    max_score: &mut usize,
    max_count: &mut usize,
    all: usize,
) -> usize {
    let mut count: [usize; 2] = [0; 2];
    for (idx, i) in graph[*node].iter().enumerate() {
        count[idx] = dfs(graph, i, max_score, max_count, all);
    }
    let ans = count[0] + count[1] + 1;
    let other = all - ans;

    count[0] = if count[0] == 0 { 1 } else { count[0] };
    count[1] = if count[1] == 0 { 1 } else { count[1] };
    let other = if other == 0 { 1 } else { other };

    if count[0] * count[1] * other > *max_score {
        *max_score = count[0] * count[1] * other;
        *max_count = 1;
    } else if count[0] * count[1] * other == *max_score {
        *max_count += 1;
    }
    return ans;
}

impl Solution {
    pub fn count_highest_score_nodes(parents: Vec<i32>) -> i32 {
        let mut graph = Vec::with_capacity(parents.len());
        for _ in 0..parents.len() {
            graph.push(Vec::with_capacity(2));
        }
        for (idx, el) in parents[1..].iter().enumerate() {
            let el = *el as usize;
            graph[el].push(idx+1)
        }

        let mut tmp = 0;
        let mut ans = 0;
        dfs(&graph, &0, &mut tmp, &mut ans, parents.len());
        ans as i32
    }
}