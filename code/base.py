import os
from itertools import takewhile

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike

from .utils import get_intersection


class Node:
    def __init__(self, u_id: int, neighbors: ArrayLike, skip_unique: False = False):
        self._u_id = u_id
        # produces sorted array
        self.neighbors = np.unique(neighbors) if not skip_unique else neighbors
        
    @property
    def u_id(self):
        return self._u_id
    
    @property
    def deg(self):
        return len(self.neighbors)
    
    def subgraph(self, other_nodes: np.ndarray):
        return Node(self.u_id, get_intersection(self.neighbors, other_nodes), skip_unique=True)
    

class Network:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise OSError("wrong graph path")
        
        with open(path) as f:
            skip_rows = len(list(
                takewhile(lambda s: s.startswith("%"), f)
            ))
                
        self.data = pd.read_csv(path, sep=r'\s+', header=None,
                                names=["fr", "to", "weight", "timestamp"], skiprows=skip_rows)\
                        .drop(columns=["weight"])\
                        .sort_values(by="timestamp")
        
        self.edges = np.sort(self.data[["fr", "to"]].values)
        self.total_nodes = self.edges.max()
        self.timestamps = self.data.timestamp.values

    def __str__(self):
        ans = "from\tto\tweight\ttimestamp\n"

        for key in sorted(self.__graph.keys()):
            node = self.__graph[key]

            for j in node.edges_to:
                ans += f"{node.u_id}\t{j.node.u_id}\n"

        return ans


class Graph:
    def __init__(self, network: Network, edges: np.ndarray, nodes: dict[int, Node], 
                 active_nodes_ids: None | list[int] = None):
        self.network = network
        self.edges = edges
        self.edges_set: np.ndarray = np.unique(self.edges, axis=0)
        self.nodes = nodes
        if active_nodes_ids is not None:
            self.active_nodes = active_nodes_ids
        else:
            self.active_nodes = list(self.nodes.keys())
    
    def get_subgraph(self, nodes_ids: ArrayLike) -> "Graph":
        nodes_ids = np.unique(nodes_ids)
        new_nodes = {u_id : self.nodes[u_id].subgraph(nodes_ids)
                     for u_id in nodes_ids}
        new_edges = np.array([
            [u_id, neighbor] for u_id, node in new_nodes.items() for neighbor in node.neighbors
        ])
        
        return Graph(self.network, new_edges, new_nodes, nodes_ids)
    
    @property
    def density(self):
        if len(self.nodes) > 1:
            return 2 * len(self.edges_set) / len(self.nodes) / (len(self.nodes) - 1) 
        return np.nan
    
    def clear(self):
        del self.edges
        del self.network
        del self.edges_set
        del self.nodes
        del self.active_nodes

class StaticGraph(Graph):
    def __init__(self, timestamps, quantile_end, *args, **kwargs):
        self.timestamps = timestamps
        self.quantile_end = quantile_end
        super().__init__(*args, **kwargs)
        
    @staticmethod
    def from_time_slice(network, quantile_end, quantile_start=0) -> "Graph":
        assert 0 <= quantile_start <= quantile_end <= 1, "Incorrect quantiles"
        
        timestamps = network.timestamps
        left, right = np.quantile(timestamps, [quantile_start, quantile_end])
        mask = (left <= timestamps) & (timestamps <= right)
        edges = network.edges[mask]
        timestamps = timestamps[mask]
        
        undirected = np.vstack([edges, edges[:, ::-1]])
        adj_lists = pd.DataFrame(undirected, columns=["v1", "v2"])\
            .groupby("v1")\
            .v2.apply(np.array)
        
        nodes = {u_id : Node(u_id,np.empty(0, dtype=int)) for u_id in np.arange(1, network.total_nodes + 1)}
        nodes |= {u_id : Node(u_id, neighbors) for u_id, neighbors in adj_lists.items()}
        
        return StaticGraph(timestamps, quantile_end, network, edges, nodes)
