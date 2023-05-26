import numpy as np
from numba import njit

@njit
def get_intersection(first, second):
    i = j = k = 0
    buffer = np.empty(min(first.size, second.size), dtype=first.dtype)
    while i < first.size and j < second.size:
        if first[i] == second[j]:
            buffer[k] = first[i]
            k += 1
            i += 1
            j += 1
        elif first[i] < second[j]:
            i += 1
        else: 
            j += 1
    return buffer[:k]