"""Figure illustrating a bimodal distribution.

"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from scipy.stats import norm

if __name__ == "__main__":

    from matplotlib import rcParams as defaults

    figsize = defaults["figure.figsize"]
    # defaults["figure.figsize"] = [figsize[0], int(figsize[0] / )]
    defaults["lines.linewidth"] = 2
    defaults["font.size"] = 14

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    a = norm.rvs(size=1000)
    b = norm.rvs(6, 2, size=1000)
    x = np.concatenate([a, b])
    ax.hist(x, bins=50)
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    sb.despine(fig, ax, top=True, right=True)
    ax.set_xlabel("Bimodal data")
    ax.set_xticks([])
    ax.set_ylabel("Count")
    #
    # props = dict(facecolor='black', shrink=0.05)
    # plt.annotate("Garbage in, garbage out", (-1, -1), (-0.8, -0.9), arrowprops=props)
    # plt.annotate("Stating the obvious", (1, -1), (-0.1, -0.7), arrowprops=props)
    #
    ax.axvline([x.mean()], ls="--", c="k")
    # plt.annotate("Most real-world data", (-0.35, 0.07))

    plt.savefig(
        f"../../assets/images/bimodal-distribution.svg", bbox_inches=0, transparent=True
    )
