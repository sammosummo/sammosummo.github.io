"""Example of Bayesian confirmatory factor analysis in "long form" and the factors are
estimated directly.

"""
from itertools import product

import numpy as np
import pandas as pd
import pymc3 as pm
import theano.tensor as tt
import matplotlib.pyplot as plt
from os.path import exists

from matplotlib import rcParams
from pymc3.math import matrix_dot
from tabulate import tabulate
from theano.tensor.nlinalg import matrix_inverse


def bcfau(items, factors, paths, nu_sd=100, alpha_sd=100, d_beta=10):
    r"""Constructs a Bayesian CFA model in "univariate form" by directly estimating the
    factors.

    Args:
        items (np.array): Data.
        factors (np.array): Factor design matrix.
        paths (np.array): Paths design matrix.
        nu_sd (:obj:`float`, optional): Standard deviation of normal prior on item
            intercepts.
        alpha_sd (:obj:`float`, optional): Standard deviation of normal prior on factor
            intercepts.
        d_beta (:obj:`float`, optional): Scale parameter of half-Cauchy prior on factor
            standard deviation.

    Returns:
        None: Places model in context.

    """
    # get numbers of cases, items, and factors
    n, p = items.shape
    p_, m = factors.shape
    assert p == p_, "Mismatch between data and factor-loading matrices"

    # priors on item intercepts
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=nu_sd, shape=p, testval=np.zeros(p))

    # priors on factor intercepts
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=alpha_sd, shape=m, testval=np.zeros(m))

    # priors on factor loadings
    l = np.asarray(factors).sum()
    lam = pm.Normal(name=r"$\lambda$", mu=0, sd=1, shape=l, testval=np.zeros(l))

    # loading matrix
    Lambda = tt.zeros(factors.shape)
    k = 0
    for i, j in product(range(p), range(m)):
        if factors[i, j] == 1:
            Lambda = tt.inc_subtensor(Lambda[i, j], lam[k])
            k += 1
    pm.Deterministic(name=r"$\Lambda$", var=Lambda)

    # priors on paths
    g = np.asarray(paths).sum()
    gam = pm.Normal(name=r"$\gamma$", mu=0, sd=1, shape=g, testval=np.zeros(g))

    # path matrix
    Gamma = tt.zeros(paths.shape)
    k = 0
    for i, j in product(range(m), range(m)):
        if paths[i, j] == 1:
            Gamma = tt.inc_subtensor(Gamma[i, j], gam[k])
            k += 1
    pm.Deterministic(name=r"$\Gamma$", var=Gamma)

    # priors on factor residuals
    zeta = pm.Normal(name=r"$\zeta$", mu=0, sigma=1, shape=(n, m), testval=0)

    # latent variables
    I = np.eye(m)
    M = nu + matrix_dot(
        matrix_dot((alpha + zeta), matrix_inverse(I - Gamma.T)), Lambda.T
    )

    # item residual standard deviations
    S = pm.HalfCauchy(
        name=r"$\sqrt{\theta}$", beta=d_beta, shape=p, testval=items.std(axis=0)
    )

    # observations
    pm.Normal(name="$Y$", mu=M, sigma=S, observed=items, shape=items.shape)


def bcfab(items, factors, paths, nu_sd=100, alpha_sd=100):
    r"""Constructs a Bayesian CFA model in "binomial form".

    Args:
        items (np.array): Data.
        factors (np.array): Factor design matrix.
        paths (np.array): Paths design matrix.
        nu_sd (:obj:`float`, optional): Standard deviation of normal prior on item
            intercepts.
        alpha_sd (:obj:`float`, optional): Standard deviation of normal prior on factor
            intercepts.

    Returns:
        None: Places model in context.

    """
    # get numbers of cases, items, and factors
    n, p = items.shape
    p_, m = factors.shape
    assert p == p_, "Mismatch between data and factor-loading matrices"

    # priors on item intercepts
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=nu_sd, shape=p, testval=np.zeros(p))

    # priors on factor intercepts
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=alpha_sd, shape=m, testval=np.zeros(m))

    # priors on factor loadings
    l = np.asarray(factors).sum()
    lam = pm.Normal(name=r"$\lambda$", mu=0, sd=1, shape=l, testval=np.zeros(l))

    # loading matrix
    Lambda = tt.zeros(factors.shape)
    k = 0
    for i, j in product(range(p), range(m)):
        if factors[i, j] == 1:
            Lambda = tt.inc_subtensor(Lambda[i, j], lam[k])
            k += 1
    pm.Deterministic(name=r"$\Lambda$", var=Lambda)

    # priors on paths
    g = np.asarray(paths).sum()
    gam = pm.Normal(name=r"$\gamma$", mu=0, sd=1, shape=g, testval=np.zeros(g))

    # path matrix
    Gamma = tt.zeros(paths.shape)
    k = 0
    for i, j in product(range(m), range(m)):
        if paths[i, j] == 1:
            Gamma = tt.inc_subtensor(Gamma[i, j], gam[k])
            k += 1
    pm.Deterministic(name=r"$\Gamma$", var=Gamma)

    # priors on factor residuals
    zeta = pm.Normal(name=r"$\zeta$", mu=0, sigma=1, shape=(n, m), testval=0)

    # latent variables
    I = np.eye(m)
    Pi = pm.math.sigmoid(
        nu
        + matrix_dot(matrix_dot((alpha + zeta), matrix_inverse(I - Gamma.T)), Lambda.T)
    )

    # observations
    pm.Binomial(
        name="$Y$", p=Pi, n=items.max(axis=0), observed=items, shape=items.shape
    )


def sampleandsave(f):
    """Sample from the model in context.

    """
    if not exists(f):

        # sample and save

        trace = pm.sample(8000, tune=2000, chains=1)
        pm.save_trace(trace, f)
        pm.traceplot(trace, compact=True)
        rcParams["font.size"] = 14
        plt.savefig(f"{f}/traceplot.png")
        ppc = pm.sample_posterior_predictive(trace)["$Y$"]
        np.savez_compressed(f"{f}/ppc.npz", ppc)

    else:

        trace = pm.load_trace(f)

    return trace


def tables(trace):
    """Print loading and path tables to stdout.

    """
    item_names = [
        "visual",
        "cubes",
        "paper",
        "flags",
        "general",
        "paragrap",
        "sentence",
        "wordc",
        "wordm",
        "addition",
        "code",
        "counting",
        "straight",
        "wordr",
        "numberr",
        "figurer",
        "object",
        "numberf",
        "figurew",
    ]
    loadings = pd.DataFrame(
        trace[r"$\Lambda$"].mean(axis=0).round(2)[:, :-1],
        index=[v.title() for v in item_names],
        columns=["Spatial", "Verbal", "Speed", "Memory"],
    )
    print(tabulate(loadings, tablefmt="pipe", headers="keys"))

    _paths = pd.DataFrame(
        trace[r"$\Gamma$"].mean(axis=0).round(2)[:-1, -1],
        index=["Spatial", "Verbal", "Speed", "Memory"],
        columns=["g"],
    )
    print(tabulate(_paths, tablefmt="pipe", headers="keys"))


def main():

    # load the data
    df = pd.read_csv("../../assets/data/HS.csv", index_col=0)

    # define items to keep
    item_names = [
        "visual",
        "cubes",
        "paper",
        "flags",
        "general",
        "paragrap",
        "sentence",
        "wordc",
        "wordm",
        "addition",
        "code",
        "counting",
        "straight",
        "wordr",
        "numberr",
        "figurer",
        "object",
        "numberf",
        "figurew",
    ]

    # define the factor structure
    factors = np.array(
        [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0],
        ]
    )

    # define paths
    paths = np.array(
        [
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ]
    )

    # iterate over the two schools
    for school, sdf in df.groupby("school"):

        models = {}

        for func, name in zip([bcfau, bcfab], ["uni", "bin"]):

            # define the path to save results
            f = f"../data/BSEM (compare) examples/{school} ({name})"

            # select the 19 commonly used variables
            items = sdf[item_names]

            with pm.Model() as m:

                func(items, factors, paths)
                trace = sampleandsave(f)
                print(trace.varnames)
                tables(trace)

                approx = pm.fit(200000)
                trace = approx.sample()
                tables(trace)

            models[name] = trace

        # print(pm.compare(models))


if __name__ == "__main__":
    main()
