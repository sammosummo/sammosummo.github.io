"""Generate data from a more realistic hierarchical distribution.

"""
import numpy as np
import pymc3 as pm
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import norm, halfcauchy


def main():

    # generate data
    np.random.seed(0)
    n = 1
    m = 10000
    mu = norm.rvs(0, 1, m)
    sigma = halfcauchy.rvs(0, 1, m)
    y = norm.rvs(mu, sigma, (n, m))

    # set up model
    with pm.Model():

        mu_ = pm.Normal("mu", 0, 1)
        sigma_ = pm.HalfCauchy("sigma", 1)
        yt_ = pm.Normal("yt", 0, 1, shape=n)
        pm.Deterministic("y", mu_ + yt_ * sigma_)
        # y_ = pm.Normal("y", mu_, sigma_, shape=n)

        # sample and save samples
        trace = pm.sample(m, chains=1)
        mu_samples = trace["mu"][:]
        sigma_samples = trace["sigma"][:]
        yt_samples = trace["yt"].T[:]
        y_samples = trace["y"].T[:]

    # plot 2-D figures
    sc = 5
    fs = rcParams["figure.figsize"]
    rcParams["figure.figsize"] = (fs[0], fs[0])
    rcParams["lines.linewidth"] = 2
    rcParams["font.size"] = 14
    fig, axes = plt.subplots(2, 2, constrained_layout=True)

    ax = axes[0, 0]
    ax.scatter(
        yt_samples[0], mu_samples, marker=".", alpha=0.05, rasterized=True, color="r"
    )
    ax.set_xlim(-sc, sc)
    ax.set_ylim(-sc, sc)
    ax.set_ylabel("$\mu$")
    ax.set_xticklabels([])

    ax = axes[0, 1]
    ax.scatter(
        y_samples[0], mu_samples, marker=".", alpha=0.05, rasterized=True, color="r"
    )
    ax.set_xlim(-sc, sc)
    ax.set_ylim(-sc, sc)
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    ax = axes[1, 0]
    ax.scatter(
        yt_samples[0], sigma_samples, marker=".", alpha=0.05, rasterized=True, color="r"
    )
    ax.set_xlim(-sc, sc)
    ax.set_ylim(0, sc / 2)
    ax.set_xlabel(r"$\tilde{y}_0$")
    ax.set_ylabel("$\sigma$")

    ax = axes[1, 1]
    ax.scatter(
        y_samples[0], sigma_samples, marker=".", alpha=0.05, rasterized=True, color="r"
    )
    ax.set_xlim(-sc, sc)
    ax.set_ylim(0, sc / 2)
    ax.set_yticklabels([])
    ax.set_xlabel("$y_0$")

    # save
    plt.savefig("../images/realistic-funnel-b.svg", bbox_inches=0, transparent=True)


if __name__ == "__main__":
    main()
