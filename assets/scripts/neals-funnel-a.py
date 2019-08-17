"""Generate data from Neal's funnel distribution.

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import norm


def main():

    # set up figure
    fs = rcParams["figure.figsize"]
    rcParams["figure.figsize"] = (fs[0], fs[0] / 2)
    rcParams["lines.linewidth"] = 2
    rcParams["font.size"] = 14

    # generate data
    np.random.seed(0)
    k = 9
    n = 10000
    v = norm.rvs(0, 3, n)
    x = norm.rvs(0, np.exp(v / 2), (k, n))

    # plot data
    fig, axes = plt.subplots(1, 2, constrained_layout=True)
    ax = axes[0]
    ax.scatter(x[0], v, marker=".", alpha=0.05, rasterized=True)
    ax.set_xlim(-20, 20)
    ax.set_ylim(-9, 9)
    ax.set_xlabel("$x_0$")
    ax.set_ylabel("$v$")

    # plot analytic log-likelihood
    ax = axes[1]
    r = 500
    x, v = np.meshgrid(np.linspace(-20, 20, r), np.linspace(-9, 9, r))
    logp = norm.logpdf(v, 0, 3) + norm.logpdf(x, 0, np.exp(v / 2))
    ax.imshow(logp, vmin=-7.5, vmax=-2.5, cmap="viridis", origin="lower")
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticks(np.linspace(0, 499, 5))
    ax.set_xticklabels(np.linspace(-20, 20, 5).astype(int))
    ax.set_xlabel("$x_0$")

    # save
    plt.savefig("../images/neals-funnel-a.svg", bbox_inches=0, transparent=True)


if __name__ == "__main__":
    main()
