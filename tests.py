import os
import json
import numpy as np
from code.base import Graph, Node


from code.structural.structural_features import first_task


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, Graph):
            nodes = obj.nodes.values()
            edges_f = {}
            for fr, to in obj.edges_set:
                fr, to = int(fr), int(to)
                edges_f[fr] = edges_f.get(fr, [])
                edges_f[fr].append(to)

                edges_f[to] = edges_f.get(to, [])
                edges_f[to].append(fr)
            return {"edges": edges_f, "nodes": list(nodes)}
        if isinstance(obj, Node):
            return obj.u_id
        return super(MyEncoder, self).default(obj)


PATH = "./graphs/tests"
OUT_PATH = "./tests_out"


def rewrite(path: str):
    data: list[list[str]] = []
    with open(path, "r") as file:
        data = list(map(lambda x: x.split(), file.readlines()))
    if len(data[0]) == 4:
        return

    with open(path, "w") as file:
        for i in data:
            file.write(f"{i[0]} {i[1]} 1 1\n")


try:
    os.mkdir(OUT_PATH)
except FileExistsError:
    pass

for i in next(os.walk(PATH))[2]:
    in_name = f"{PATH}/{i}"
    out_name = f"{OUT_PATH}/{i.replace('.txt', '.json')}"
    

    rewrite(in_name)

    if not os.path.isfile(out_name):
        print(f"{i} start")
        ans = first_task(in_name, full=True)
        with open(out_name, "w", encoding="utf-8") as file:
            # ans["conn_comps"] = len(ans["conn_comps"])
            # ans.pop("max_conn_comp")
            json.dump(ans, file, indent=4)
        print(f"{i} complite")
    else:
        print(f"{i} was skipped")
