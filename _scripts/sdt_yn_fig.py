"""Creates figures to illustrate SDT models.

"""
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sb


if __name__ == '__main__':

    from matplotlib import rcParams as defaults

    figsize = defaults["figure.figsize"]
    defaults["figure.figsize"] = [figsize[0], int(figsize[1] * 2 / 3)]
    defaults["lines.linewidth"] = 2
    defaults["font.size"] = 14

    d = 1
    psi = np.linspace(-3, 3 + d, 10000)
    first = norm.pdf(psi, 0, 1)
    second = norm.pdf(psi, d, 1)

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.plot(psi, first, label=r"$x=0$", linewidth=3)
    ax.plot(psi, second, label=r"$x=1$", linewidth=3)
    ax.set_xlim(-3, 3 + d)
    ax.set_ylim(0, first.max() * 1.05)
    ax.set_xticks([0, d])
    ax.set_xticklabels([0, r"$d$"], fontdict={"fontsize": 12})
    ax.set_yticks([], [])
    ax.set_xlabel(r"$\Psi$")
    ax.set_ylabel("Probability density")
    sb.despine(fig, ax, top=True, right=True)
    f = f"../assets/images/evg_yn_perceptual.svg"
    plt.legend()
    plt.savefig(f, bbox_inches=0, transparent=True)
