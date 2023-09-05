from collections import deque

def kSimilarity(s1, s2):
    if s1 == s2:
        return 0

    queue = deque([(s1, 0)])
    visited = set([s1])

    while queue:
        current, swaps = queue.popleft()

        if current == s2:
            return swaps

        i = 0
        while current[i] == s2[i]:
            i += 1

        for j in range(i + 1, len(current)):
            if current[j] == s2[i]:
                new_str = list(current)
                new_str[i], new_str[j] = new_str[j], new_str[i]
                new_str = ''.join(new_str)
                if new_str not in visited:
                    visited.add(new_str)
                    queue.append((new_str, swaps + 1))


s1 = "fffeaacbdbdafcfbbafb"
s2 = "abcbdfafffefabdbbafc"
result = kSimilarity(s1, s2)
print(result) #10