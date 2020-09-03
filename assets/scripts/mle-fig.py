"""Figure illustrating a bimodal distribution.

"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

from scipy.stats import norm

if __name__ == "__main__":

    from matplotlib import rcParams as defaults

    figsize = defaults["figure.figsize"]
    defaults["figure.figsize"] = [figsize[0], int(figsize[0] / 2)]
    defaults["lines.linewidth"] = 2
    defaults["font.size"] = 14

    fig, axes = plt.subplots(1, 2, constrained_layout=True)
    data = norm.rvs(1, 1, size=1000)
    x = np.linspace(-3.5, 3.5)
    y = norm.pdf(x)
    axes[0].hist(data, bins=50, normed=True)
    axes[0].plot(x, y, "k")
    axes[0].set_xticks([], [])
    axes[0].set_yticks([], [])
    sb.despine(fig, axes[0], top=True, right=True)
    axes[0].set_title("Unfitted model")

    axes[1].hist(data, bins=50, normed=True)
    y = norm.pdf(x, 1, 1)
    axes[1].plot(x, y, "k")
    axes[1].set_xticks([], [])
    axes[1].set_yticks([], [])
    sb.despine(fig, axes[1], top=True, right=True)
    axes[1].set_title("Fitted model")

    plt.savefig(f"../../assets/images/mle-fig.svg", bbox_inches=0, transparent=True)
