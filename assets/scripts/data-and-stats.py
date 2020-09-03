"""Figure showing my perception on the relationship between the utility of statistics
and data quality.

"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

if __name__ == "__main__":

    from matplotlib import rcParams as defaults

    figsize = defaults["figure.figsize"]
    defaults["figure.figsize"] = [figsize[0], int(figsize[0] / 2)]
    defaults["lines.linewidth"] = 2
    defaults["font.size"] = 14

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    x = np.linspace(-1, 1, 50)
    y = -(x ** 2)
    ax.plot(x, y, lw=4)
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    sb.despine(fig, ax, top=True, right=True)
    ax.set_xlabel("Data quality")
    ax.set_xticks([])
    ax.set_ylabel("Usefulness of statistics")

    props = dict(facecolor="black", shrink=0.05)
    plt.annotate("Garbage in, garbage out", (-1, -1), (-0.8, -0.9), arrowprops=props)
    plt.annotate("Stating the obvious", (1, -1), (-0.1, -0.7), arrowprops=props)

    ax.vlines([-0.5, 0.5], -0.5, 0.1, ls="--")
    plt.annotate("Most real-world data", (-0.35, 0.07))

    plt.savefig(
        f"../../assets/images/data-and-stats.svg", bbox_inches=0, transparent=True
    )
