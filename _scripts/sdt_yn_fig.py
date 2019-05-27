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
    defaults["lines.linewidth"] = 3
    defaults["font.size"] = 14

    d = 1
    psi = np.linspace(-3, 3 + d, 10000)
    first = norm.pdf(psi, 0, 1)
    second = norm.pdf(psi, d, 1)

    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.plot(psi, first, label=r"$X=0$")
    ax.plot(psi, second, label=r"$X=1$")
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

    k = 0.3
    line = plt.axvline(k, c="black")
    ax.set_xticks([0, k, d])
    ax.set_xticklabels([0, r"$k$", r"$d$"], fontdict={"fontsize": 12})
    f = f"../assets/images/evg_yn_response.svg"
    plt.savefig(f, bbox_inches=0, transparent=True)

    a = np.where(psi.round(3) == k)[0][0]
    fill = plt.fill_between(psi[a:], first[a:], alpha=0.3)
    f = f"../assets/images/evg_yn_fa.svg"
    plt.savefig(f, bbox_inches=0, transparent=True)

    fill.set_visible(False)
    fill = plt.fill_between(psi[a:], second[a:], alpha=0.3)
    f = f"../assets/images/evg_yn_hit.svg"
    plt.savefig(f, bbox_inches=0, transparent=True)

    fill.set_visible(False)
    line.set_visible(False)
    kun = d / 2
    line = plt.axvline(kun, c="black")
    a = np.where(psi.round(3) == kun)[0][0]
    fill0 = plt.fill_between(psi[a:], second[a:], alpha=0.3, color="C1")
    fill1 = plt.fill_between(psi[:a], first[:a], alpha=0.3, color="C2")
    ax.set_xticks([0, kun, d])
    ax.set_xticklabels([0, r"$k_\mathrm{unb}$", r"$d$"], fontdict={"fontsize": 12})
    f = f"../assets/images/evg_yn_unbiased.svg"
    plt.savefig(f, bbox_inches=0, transparent=True)

    k = 0.2
    fill0.set_visible(False)
    fill1.set_visible(False)
    line.set_visible(False)
    ax.set_xticks([0, k, kun, d])
    ax.set_xticklabels(
        [0, r"$k$", r"$k_\mathrm{unb}$", r"$d$"], fontdict={"fontsize": 12}
    )
    ax.annotate("", (k, 0.3), (kun, 0.3), arrowprops={"arrowstyle": "|-|"})
    plt.text((k+kun)/2.5, 0.22, "$c$")
    f = f"../assets/images/evg_yn_criterion.svg"
    plt.savefig(f, bbox_inches=0, transparent=True)




