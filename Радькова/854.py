class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        N = len(s1)
        Q = []
        Q.append(s1)

        swaps = 0  # resulting value

        visited = set()
        visited.add(s1)

        while Q:
            qlen = len(Q)

            for i in range(qlen):
                curstr = Q.pop(0)  # get string from queue

                if curstr == s2:
                    return swaps

                j = 0
                curlist = list(curstr)

                while curlist[j] == s2[j]:  # check number of char matches
                    j += 1

                for k in range(j, N):  # search for swap
                    if s2[k] != curlist[k] and s2[j] == curlist[k]:
                        curlist[j], curlist[k] = curlist[k], curlist[j]

                        newstr = ''.join(curlist)
                        if newstr not in visited:
                            Q.append(newstr)
                            visited.add(newstr)

                        curlist[j], curlist[k] = curlist[k], curlist[j]  # revert changes

            swaps += 1

        return swaps