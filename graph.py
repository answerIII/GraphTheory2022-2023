"""Module for reading graph files"""

import os.path
import weakref
from typing import Self, Dict, List


class Edge:
    """Edge object"""

    def __init__(
        self, from_node: "Node", to_node: "Node", weight: int, timestamp: float
    ):
        self.__from_node = weakref.proxy(from_node)
        self.__to_node = weakref.proxy(to_node)
        self._weight = weight
        self._timestamp = timestamp

    def __repr__(self):
        return f"Edge(from={self.from_node}, to={self.to_node}, weight={self.weight}, timestamp={self.timestamp})"

    def __hash__(self):
        return int(
            (
                str(self.__from_node.u_id).rjust(7, "0")
                + str(self.__to_node.u_id).rjust(7, "0")
            )[::-1]
        )

    def __eq__(self, o: "Edge"):
        if not isinstance(o, Edge):
            return NotImplemented

        if o.from_node == self.from_node and o.to_node == self.to_node:
            return True

        return False

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def weight(self):
        return self._weight

    @property
    def from_node(self):
        return self.__from_node

    @property
    def to_node(self):
        return self.__to_node


class Node:
    """Graph node object"""

    def __init__(self, u_id: int):
        self.__u_id = u_id
        self.__from: List[Edge] = []
        self.__to: List[Edge] = []

    def __repr__(self):
        return f"Node(u_id={self.u_id})"

    def _add_parent(self, node: Self, weight: int, timestamp: float):
        self.__from.append(Edge(node, self, weight, timestamp))

    def _add_child(self, node: Self, weight: int, timestamp: float):
        self.__to.append(Edge(self, node, weight, timestamp))

    @property
    def u_id(self):
        """u_id"""
        return self.__u_id

    @property
    def nodes_to(self) -> List["Node"]:
        """Returns list of vertices where an edge EXISTS. Does not take into account the multiedges

        Returns:
            list[Node]: _description_
        """
        return set(self.edges_to)

    @property
    def edges_to(self) -> List[Edge]:
        """Which vertices have edges from this vertex

        Returns:
            list[Node]: list of nodes
        """

        return self.__to

    @property
    def edges_from(self) -> List[Edge]:
        """From which vertices can one come to this vertex

        Returns:
            list[Node]: list of nodes
        """

        return self.__from


class Graph:
    """Graph object"""

    def __init__(self, path: str):
        """Create graph obj

        Args:
            path (str): Path file "out.{graph_name}"
        Raises:
            OSError: wrond graph path
        """

        count = 0

        self.__graph: Dict[int, Node] = {}

        if not os.path.isfile(path):
            raise OSError("wrond graph path")

        with open(path, "r", encoding="utf-8") as file:
            for cur_str in file:
                if cur_str.startswith("%"):
                    continue

                cur_str = cur_str.replace("\t", " ").replace("  ", " ")
                tmp = cur_str.split(" ")

                v_from, v_to, weight, timestamp = (
                    int(tmp[0]),
                    int(tmp[1]),
                    int(tmp[2]),
                    float(tmp[3]),
                )

                par = self.__graph.get(v_from, Node(v_from))
                ch = self.__graph.get(v_to, Node(v_to))

                par._add_child(ch, weight, timestamp)
                ch._add_parent(par, weight, timestamp)

                self.__graph[v_from] = par
                self.__graph[v_to] = ch

                count += 1

        print("Edges:", count)

    def __str__(self):
        ans = "from\tto\tweight\ttimestamp\n"

        for key in sorted(self.__graph.keys()):
            node = self.__graph[key]

            for j in node.edges_to:
                ans += f"{node.u_id}\t{j.node.u_id}\n"

        return ans

    def __getitem__(self, key: int) -> Node:
        if not isinstance(key, int):
            raise TypeError("Wrong index type")

        if (tmp := self.__graph.get(key, None)) is None:
            raise KeyError("Graph does not contain vertices with such an index")
        else:
            return tmp

    def get_all_nodes(self):
        return self.__graph.items()

    def get_all_ids(self):
        return list(self.__graph.keys())


if __name__ == "__main__":
    # t = Graph("./graphs/radoslaw_email/out.radoslaw_email_email")
    t = Graph("./test.txt")

    node_1 = t[1]
    print(*set(node_1.edges_to), sep="\n")
    print("___________________________")

    node_2 = t[2]
    print(*set(node_2.edges_from), sep="\n")

    # print(t)
