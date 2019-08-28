"""Create figurea to illustrate noise and noise plus a pure tone.

"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb


if __name__ == "__main__":

    from matplotlib import rcParams as defaults

    figsize = defaults["figure.figsize"]
    defaults["figure.figsize"] = [figsize[0], int(figsize[1] / 2)]
    defaults["lines.linewidth"] = 2
    defaults["font.size"] = 14

    n = 2000
    x = np.linspace(0, 40 * np.pi, n)
    noise = np.random.normal(size=n)
    tone = np.sin(x)
    fig, axes = plt.subplots(1, 2, constrained_layout=True, sharex=True, sharey=True)
    ax0, ax1 = axes
    ax0.plot(noise, "C0")
    ax0.set_title(r"Noise ($X=0$)", fontsize=14)
    ax1.plot(noise + tone, "C0")
    ax1.set_title(r"Noise plus signal ($X=1$)", fontsize=14)
    for ax in axes:
        ax0.set_xticks([], [])
        ax0.set_yticks([], [])
        sb.despine(fig, ax, top=True, right=True)
        ax.set_xlabel("Time")
        ax.set_ylabel("Pressure")
    ax1.set_xlim(0, n)
    ax1.set_ylim((noise + tone).min(), (noise + tone).max())
    plt.savefig(
        f"../../assets/images/noise_toneplusnoise.svg", bbox_inches=0, transparent=True
    )
