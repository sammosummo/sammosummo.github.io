"""Generate data and sample from Neal's funnel distribution.

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pymc3 as pm
from scipy.stats import norm


def main():

    with pm.Model():

        # set up figure
        fs = rcParams["figure.figsize"]
        rcParams["figure.figsize"] = (fs[0], fs[0] / 2)
        rcParams["lines.linewidth"] = 2
        rcParams["font.size"] = 14

        # simulate data
        np.random.seed(0)
        k = 9
        n = 10000
        v = norm.rvs(0, 3, n)
        x = norm.rvs(0, np.exp(v / 2), (k, n))

        # plot simulated data
        fig, axes = plt.subplots(
            1, 2, constrained_layout=True, sharex=True, sharey=True
        )
        ax = axes[0]
        ax.scatter(x[0], v, marker=".", alpha=0.05, rasterized=True)
        ax.set_xlim(-20, 20)
        ax.set_ylim(-9, 9)
        ax.set_xlabel("$x_0$")
        ax.set_ylabel("$v$")

        # set up model
        v_ = pm.Normal("v", mu=0, sd=3)
        x_ = pm.Normal("x", mu=0, sd=pm.math.exp(v_ / 2), shape=k)

        # sample and save samples
        trace = pm.sample(n, chains=1)
        v_samples = trace["v"][:]
        x_samples = trace["x"][:].T

        # plot samples
        ax = axes[1]
        ax.scatter(
            x_samples[0], v_samples, marker=".", alpha=0.05, rasterized=True, color="r"
        )
        ax.set_xlabel("$x_0$")

        # save
        plt.savefig("../images/neals-funnel-b.svg", bbox_inches=0, transparent=True)


if __name__ == "__main__":
    main()
