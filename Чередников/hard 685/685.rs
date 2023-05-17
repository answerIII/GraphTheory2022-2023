fn dfs(parent: &Vec<usize>, node: usize, to: usize, visited: &mut Vec<bool>) -> bool {
    if node == to {
        return true;
    }
    let ans: bool;
    if visited[node] == true {
        return false;
    };
    
    visited[node] = true;
    if parent[node] == 0 {
        ans = false;
    } else {
        if visited[parent[node]] == false {
            
            ans = dfs(parent, parent[node], to, visited);
        } else {
            ans = false;
        }
    }

    visited[node] = false;
    ans
}


impl Solution {
    pub fn find_redundant_directed_connection(edges: Vec<Vec<i32>>) -> Vec<i32> {
        let mut parent: Vec<usize> = vec![0; edges.len() + 1];
        let mut visited: Vec<bool> = vec![false; edges.len() + 1];

        let mut cand1: usize = 0;
        let mut cand2: usize = 0;

        for i in &edges {
            let p = i[0] as usize;
            let c = i[1] as usize;
            if parent[c] != 0 {
                cand1 = c;
                cand2 = p;
                continue;
            }
            parent[c] = p;
        }

        if cand1 != 0 {
            let c = cand1;
            let p = cand2;
            let ans1 = dfs(&parent, p, c, &mut visited);
            let ans2 = dfs(&parent, parent[c], c, &mut visited);
            if ans1 || !ans1 && !ans2 {
                return vec![p as i32, c as i32];
            }
            if ans2 {
                return vec![parent[c] as i32, c as i32];
            }
        }

        for i in edges.iter().rev() {
            if dfs(&parent, i[0] as usize, i[1] as usize, &mut visited) {
                return vec![i[0], i[1]];
            }
        }

        vec![]
    }
}