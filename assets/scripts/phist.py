"""How to create a partially filled histogram.

"""
import matplotlib.pyplot as plt
from matplotlib import rcParams as defaults
from numpy.random import normal

defaults["lines.linewidth"] = 2
defaults["font.size"] = 14


if __name__ == "__main__":

    y = normal(0, 1, 1000)  # generate some data
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ns, bins, _ = ax.hist(y, 20, histtype="step")  # plot the unfilled histogram
    start, stop = [-1.96, 1.96]  # range to fill between

    for n, l, r in zip(ns, bins, bins[1:]):

        if l > start:
            if r < stop:
                # these bins fall completely within the range
                ax.fill_between([l, r], 0, [n, n], alpha=0.5)
            elif l < stop < r:
                ax.fill_between([l, stop], 0, [n, n], alpha=0.5)  # partial fill
        elif l < start < r:
            ax.fill_between([start, r], 0, [n, n], alpha=0.5)  # partial fill

    plt.savefig(f"../../assets/images/phist.svg", bbox_inches=0, transparent=True)
