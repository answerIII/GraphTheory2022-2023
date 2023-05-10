class Solution:
    def mostProfitablePath(self, edges: List[List[int]], bob: int, amount: List[int]) -> int:
        N = len(edges) + 1
        parent = [-1] * N  # info about parental node
        atime = [-1] * N  # entry time info for each vertex (Alice)

        adj = [[] for i in range(N)]  # adjacency list initialization
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        def dfs_time(current, par, t):
            parent[current] = par  # mark vertex as discovered
            atime[current] = t  # rewrite entry time

            for v in adj[current]:
                if v != parent[current]:
                    dfs_time(v, current, t + 1)

        dfs_time(0, -1, 0)  # run dfs to count entry time for each node (Alice)

        tmp = bob
        btime = [-1] * N  # entry time info for each vertex (Bob)
        t = 0

        while tmp != 0:  # recalculate possible incomes, starting from Bob
            btime[tmp] = t

            if btime[tmp] < atime[tmp]:  # bridge has been opened by Bob already
                amount[tmp] = 0
            elif btime[tmp] == atime[tmp]:  # simultaneous arrival
                amount[tmp] //= 2

            tmp = parent[tmp]
            t += 1

        maxincome = - 10 ** 10

        def dfs_income(current, par, income):
            down = 0

            for v in adj[current]:
                if v != par:
                    dfs_income(v, current, income + amount[v])
                    down += 1

            if down == 0:
                nonlocal maxincome
                maxincome = max(maxincome, income)

        dfs_income(0, -1, amount[0])

        return maxincome