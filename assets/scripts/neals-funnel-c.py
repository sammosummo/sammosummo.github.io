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

        # set up model
        v_ = pm.Normal("v", mu=0, sd=3)
        xt_ = pm.Normal("xt", mu=0, sd=1, shape=k)
        x_ = pm.Deterministic("x", pm.math.exp(v_ / 2) * xt_)

        # sample and save samples
        trace = pm.sample(n, chains=1)
        v_samples = trace["v"][:]
        xt_samples = trace["xt"][:].T
        x_samples = trace["x"][:].T

        # plot samples
        # plot simulated data
        fig, axes = plt.subplots(1, 2, constrained_layout=True)
        ax = axes[0]
        ax.scatter(
            xt_samples[0], v_samples, marker=".", alpha=0.05, rasterized=True, color="r"
        )
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-9, 9)
        ax.set_xlabel(r"$\tilde{x}_0$")
        ax.set_ylabel("$v$")
        ax = axes[1]
        ax.scatter(
            x_samples[0], v_samples, marker=".", alpha=0.05, rasterized=True, color="r"
        )
        ax.set_xlabel("$x_0$")
        ax.set_xlim(-20, 20)
        ax.set_ylim(-9, 9)

        # save
        plt.savefig("../images/neals-funnel-c.svg", bbox_inches=0, transparent=True)


if __name__ == "__main__":
    main()
