from typing import Dict
from graph import Graph, Edge
from heapq import heappop, heappush
from collections import deque
import random

import numpy as np


def dijkstra_iteration(
    d: int, edges: list[Edge], dist: Dict[int, float], heap: list[tuple[int, int]], func
):
    for edge in set(edges):
        u_id = func(edge)
        new_d = d + 1
        if (tmp := dist.get(u_id, float("inf"))) == float("inf") or tmp > new_d:
            dist[u_id] = new_d
            heappush(heap, (new_d, u_id))


def dijkstra(graph: Graph, start_node: int):
    heap: list[tuple[int, int]] = []
    heappush(heap, (0, start_node))

    dist: Dict[int, float] = {}

    while heap:
        d, cur_el = heappop(heap)

        node = graph[cur_el]

        dijkstra_iteration(d, node.edges_to, dist, heap, lambda x: x.to_node.u_id)
        dijkstra_iteration(d, node.edges_from, dist, heap, lambda x: x.from_node.u_id)

    return dist


def dijkstra_with_finish(graph: Graph, start_node: int, finish_node: int):
    heap: list[tuple[int, int]] = []
    heappush(heap, (0, start_node))

    dist: Dict[int, float] = {}

    while heap:
        d, cur_el = heappop(heap)

        if finish_node == cur_el:
            break

        node = graph[cur_el]

        dijkstra_iteration(d, node.edges_to, dist, heap, lambda x: x.to_node.u_id)
        dijkstra_iteration(d, node.edges_from, dist, heap, lambda x: x.from_node.u_id)

    return dist


def create_snowball(graph: Graph, count):
    root = random.choice(graph.get_all_ids())
    queue = deque()
    queue.append(root)

    s = set()

    ans_graph = Graph(None)

    while queue:
        cur_el = queue.popleft()

        if cur_el in s:
            continue

        for i in graph[cur_el].edges_to:
            u_id = i.to_node.u_id
            ans_graph.add_edge(cur_el, u_id, 1, 1)
            queue.append(u_id)

        if len(ans_graph.get_all_ids()) > count:
            break

        for i in graph[cur_el].edges_from:
            u_id = i.from_node.u_id
            ans_graph.add_edge(cur_el, u_id, 1, 1)
            queue.append(u_id)

        s.add(cur_el)

        if len(ans_graph.get_all_ids()) > count:
            break
    return ans_graph


def diameter_radius_quantile(graph: str | Graph):
    def drq_inner(ids: list[int] | list[tuple[int, int]], func):
        diam = 0
        rad = float("inf")
        dists = []
        for i in ids:
            ans = func(i)
            tmp = list(ans.values())

            max_ans = max(tmp)
            diam = max(diam, max_ans)
            rad = min(rad, max_ans)

            dists.extend(tmp)

        return diam, rad, np.percentile(dists, 90)

    _graph = None
    if isinstance(graph, str):
        _graph = Graph(graph)
    elif isinstance(graph, Graph):
        _graph = graph
    else:
        raise TypeError("graph must be str or Graph obj")

    if len(_graph.get_all_ids()) > 2000:
        ids = []
        for _ in range(500):
            a, b = 0, 0
            while a == b:
                a, b = random.choices(_graph.get_all_ids(), k=2)
            ids.append((a, b))
        func = lambda x: dijkstra_with_finish(_graph, x[0], x[1])
        ans1 = drq_inner(ids, func)

        snowball = create_snowball(_graph, 500)
        ids = snowball.get_all_ids()
        func = lambda x: dijkstra(snowball, x)
        ans2 = drq_inner(ids, func)

        return max(ans1[0], ans2[0]), min(ans1[1], ans2[1]), (ans1[2] + ans2[2]) / 2

    ids = _graph.get_all_ids()
    func = lambda x: dijkstra(_graph, x)

    return drq_inner(ids, func)


if __name__ == "__main__":
    print("(Диаметр, радиус, процентиль)")
    # print(
    #     diameter_radius_quantile("./graphs/opsahl-ucsocial/out.opsahl-ucsocial")
    # )  # (8, 2, 4.0)

    # print(
    #     diameter_radius_quantile("./graphs/radoslaw_email/out.radoslaw_email_email")
    # )  # (5, 3, 3.0)

    # print(
    #     diameter_radius_quantile("./graphs/soc-sign-bitcoinalpha/out.soc-sign-bitcoinalpha") # (10, 2, 5.0)
    # )

    # print(
    #     diameter_radius_quantile("./graphs/soc-sign-bitcoinotc/out.soc-sign-bitcoinotc")
    # )  # (9, 2, 5.0)
