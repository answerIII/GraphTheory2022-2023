from typing import List, Union
from dataclasses import dataclass

Num = Union[int, float]

@dataclass
class Node:
    idx: int
    pos_in_heap: int
    dist: Num = float('inf')
    visited: bool = False
    
@dataclass()
class Edge:
    dist: int
    to_idx: int

class Solution:
    def minimumWeight(self, size: int, edges_unord: List[List[int]],
                      src1: int, src2: int, dest: int) -> int:
        edges: List[List[Edge]] = [[] for _ in range(size)]
        edges_transposed: List[List[Edge]] = [[] for _ in range(size)]
        
        for edge in edges_unord:
            edges[edge[0]].append(Edge(to_idx=edge[1], dist=edge[2]))
            edges_transposed[edge[1]].append(Edge(to_idx=edge[0], dist=edge[2]))
        
        min_weight = min(map(sum, zip(
            Solution.dijkstra(edges, src1),
            Solution.dijkstra(edges, src2),
            Solution.dijkstra(edges_transposed, dest))
        ))
        
        return min_weight if min_weight != float('inf') else -1
    
    @staticmethod
    def dijkstra(edges: List[List[Edge]], from_idx: int):
        # returns distances 
        size = len(edges)
        nodes_heap: List[Node] = [Node(idx=idx, pos_in_heap=idx) for idx in range(size)]
        # shallow copy, to get distance by vertex index
        nodes = nodes_heap.copy()
        
        nodes[from_idx].dist = 0
        siftdown(nodes_heap, 0, from_idx)
        
        while nodes_heap and nodes_heap[0].dist != float('inf'):
            node = heappop(nodes_heap)
            
            for edge in edges[node.idx]:
                child_node = nodes[edge.to_idx]
                if not child_node.visited:
                    new_dist = node.dist + edge.dist
                    if new_dist < child_node.dist:
                        child_node.dist = new_dist
                        siftdown(nodes_heap, 0, child_node.pos_in_heap)
            
            node.visited = True
            
        return [node.dist for node in nodes]

# code from `heapq.py` - built-in module. Changed to accept `Node` and change positions

def siftup(heap: List[Node], pos:int):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos].dist < heap[rightpos].dist:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        heap[pos].pos_in_heap = pos
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    newitem.pos_in_heap = pos
    siftdown(heap, startpos, pos)

def heappop(heap: List[Node]):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        lastelt.pos_in_heap = 0
        siftup(heap, 0)
        return returnitem
    return lastelt

def siftdown(heap: List[Node], startpos: int, pos: int):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem.dist < parent.dist:
            heap[pos] = parent
            parent.pos_in_heap = pos
            pos = parentpos
            continue
        break
    heap[pos] = newitem
    newitem.pos_in_heap = pos
