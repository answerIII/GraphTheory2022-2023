class Solution(object):
    def countPaths(self, n, roads):
        """
        :type n: int
        :type roads: List[List[int]]
        :rtype: int
        """
        times = [[-1 for i in range(n)] for i in range(n)]
        new_roads = [[] for i in range(n)]
        for road in roads:
            new_roads[road[0]].append(road[1])
            new_roads[road[1]].append(road[0])
            times[road[0]][road[1]] = road[2]
            times[road[1]][road[0]] = road[2]

        infinity = 10**9 * 200 + 1

        paths = [[infinity, 0] for i in range(n)]

        paths[0] = [0, 1]

        queue = [(0, 0)]

        def get(a):
            return (a[0])

        while len(queue) > 0:
            queue.sort(key=get)
            u = queue.pop(0)[1]
            for v in new_roads[u]:
                if times[u][v] + paths[u][0] < paths[v][0]:
                    paths[v][0] = times[u][v] + paths[u][0]
                    paths[v][1] = paths[u][1]
                    for i in range(len(queue)):
                        if queue[i][1] == v:
                            queue.pop(i)
                            break
                    queue.append((paths[v][0], v))
                elif times[u][v] + paths[u][0] == paths[v][0]:
                    paths[v][1] += paths[u][1]

        mod = 10 ** 9 + 7

        return (paths[-1][1] % mod)
