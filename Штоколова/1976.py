class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int: 
        if n == 1:
          return 1

        ver = defaultdict(list)
        for k, v, t in roads:
            ver[k].append([v, t])
            ver[v].append([k, t])

        inf = 10**15
        times = [inf] * n
        use = [False] * n
        times[0] = 0 
        curr_v = 0
        min_time = 0 
        count_min_road = 0
        count_road = [0]*n
        count_road[0] = 1

        while min_time < inf:
          i = curr_v  
          use[i] = True 
          for j in ver[i]:
            if times[i] + j[1] < times[j[0]]:
              times[j[0]] = times[i] + j[1] 
              count_road[j[0]] = count_road[i]
              use[j[0]] = False 
            elif times[i] + j[1] == times[j[0]]:
              count_road[j[0]] += count_road[i] # % (10**9 + 7) 

            min_time = inf

            for ss in range(n):
              if times[ss] < min_time and not use[ss]:
                # for j in ver[ss]:
                #   if (not use[j[0]]) and times[j[0]] < min_time: 
                    # min_time = times[j[0]]
                    # curr_v = j[0] 
                min_time = times[ss]
                curr_v = ss

        return count_road[n-1] % (10**9 + 7) 
