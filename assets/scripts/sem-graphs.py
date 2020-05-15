"""Create some graphs of SEM models.

"""
from graphviz import Digraph


if __name__ == '__main__':

    g = Digraph("../images/hs-1", format="svg")
    g.attr("graph", bgcolor="transparent")
    g.attr("graph",  rankdir="RL")
    items = [
        "visual",
        "cubes",
        "paper",
        "flags",
        "general",
        "paragrap",
        "sentence",
        "wordc",
        "wordm",
        "addition",
        "code",
        "counting",
        "straight",
        "wordr",
        "numberr",
        "figurer",
        "object",
        "numberf",
        "figurew",
    ]
    factors = ["Spatial", "Verbal", "Speed", "Memory", "g"]
    loadings = [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
    ]
    paths = [
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
    ]
    for item, loading in zip(items, loadings):

        g.node(item, shape="box")

        for factor, l, path in zip(factors, loading, paths):

            if l == 1:

                g.edge(factor, item)

    for f1, path in zip(factors, paths):

        for f2, p in zip(factors, path):

            if p == 1:

                g.edge(f2, f1)




    g.view()