"""Create SDT figures.

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

    r = 500
    d = 2
    q = 4
    psi = np.linspace(-q, q + d, r)
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.plot(psi, norm.pdf(psi), label=r"$X=0$")
    ax.plot(psi, norm.pdf(psi, d, 1), label=r"$X=1$")
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    sb.despine(fig, ax, top=True, right=True)
    ax.set_xlabel("$\Psi$")
    ax.set_xticks([0, d])
    ax.set_xticklabels([0, "$d$"])
    ax.set_ylabel("Probability density")
    ax.set_xlim(psi.min(), psi.max())
    ax.set_ylim(0, norm.pdf(psi).max() * 1.1)
    ax.legend(fancybox=False, framealpha=0)
    plt.savefig(
        f"../../assets/images/sdt-evg-perceptual.svg", bbox_inches=0, transparent=True
    )

    k = 0.8
    ax.set_xticks([0, k, d])
    ax.set_xticklabels([0, "$k$", "$d$"])
    ax.vlines([k], 0, norm.pdf(psi).max(), zorder=10)
    plt.savefig(
        f"../../assets/images/sdt-evg-response.svg", bbox_inches=0, transparent=True
    )

    ix = np.argmin(np.abs(psi - k))
    x = psi[ix]
    fill = ax.fill_between(psi[ix:], norm.pdf(psi[ix:], 0, 1), alpha=0.3)
    plt.savefig(f"../../assets/images/sdt-evg-fa.svg", bbox_inches=0, transparent=True)
    fill.remove()

    fill = ax.fill_between(psi[ix:], norm.pdf(psi[ix:], d, 1), alpha=0.3)
    plt.savefig(f"../../assets/images/sdt-evg-h.svg", bbox_inches=0, transparent=True)
    fill.remove()
