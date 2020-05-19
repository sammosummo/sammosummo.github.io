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


def bcfam(items, factors, paths, nu_sd=2.5, alpha_sd=2.5, d_beta=2.5):
    r"""Constructs a Bayesian CFA model in "multivariate form".

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
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=nu_sd, shape=p, testval=items.mean(axis=0))

    # priors on factor intercepts
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=alpha_sd, shape=m, testval=np.zeros(m))

    # priors on factor loadings
    l = np.asarray(factors).sum()
    lam = pm.Normal(name=r"$\lambda$", mu=0, sd=1, shape=l, testval=np.ones(l))

    # loading matrix
    Lambda = tt.zeros(factors.shape)
    k = 0
    for i, j in product(range(p), range(m)):
        if factors[i, j] == 1:
            Lambda = tt.inc_subtensor(Lambda[i, j], lam[k])
            k += 1
    pm.Deterministic(name=r"$\Lambda$", var=Lambda)

    # item means
    mu = nu + matrix_dot(Lambda, alpha)

    # item residual covariance matrix
    d = pm.HalfCauchy(
        name=r"$\sqrt{\theta}$", beta=d_beta, shape=p, testval=items.std(axis=0)
    )
    Theta = tt.diag(d) ** 2

    # factor covariance matrix
    Psi = I = np.eye(m)

    # priors on paths
    g = np.asarray(paths).sum()
    gam = pm.Normal(name=r"$\gamma$", mu=0, sd=1, shape=g, testval=np.ones(g))

    # path matrix
    Gamma = tt.zeros(paths.shape)
    k = 0
    for i, j in product(range(m), range(m)):
        if paths[i, j] == 1:
            Gamma = tt.inc_subtensor(Gamma[i, j], gam[k])
            k += 1
    pm.Deterministic(name=r"$\Gamma$", var=Gamma)

    # item covariance matrix
    Sigma = (
        matrix_dot(
            Lambda,
            matrix_inverse(I - Gamma),
            Psi,
            matrix_inverse(I - Gamma.T),
            Lambda.T,
        )
        + Theta
    )

    # observations
    pm.MvNormal(name="$Y$", mu=mu, cov=Sigma, observed=items, shape=items.shape)


def bcfau(items, factors, paths, nu_sd=2.5, alpha_sd=2.5, d_beta=2.5):
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
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=nu_sd, shape=p, testval=items.mean(axis=0))

    # priors on factor intercepts
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=alpha_sd, shape=m, testval=np.zeros(m))

    # priors on factor loadings
    l = np.asarray(factors).sum()
    lam = pm.Normal(name=r"$\lambda$", mu=0, sd=1, shape=l, testval=np.ones(l))

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
    gam = pm.Normal(name=r"$\gamma$", mu=0, sd=1, shape=g, testval=np.ones(g))

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


def bcfabin(
    items, factors, nu_sd=2.5, alpha_sd=2.5, d_beta=2.5,
):
    r"""Constructs a Bayesian CFA model in "univariate form" by directly estimating the
    factors, with a binomial likelihood.

    Args:
        items (np.array): Array of item data.
        factors (np.array): Factor design matrix.
        beta (:obj:`float` or `'estimate'`, optional): Standard deviation of normal
            prior on cross loadings. If `'estimate'`,  beta is estimated from the data.
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

    binom_n = np.zeros_like(items) + items.max(axis=1).til

    # priors on item intercepts
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=nu_sd, shape=p, testval=items.mean(axis=0))

    # priors on factor intercepts
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=alpha_sd, shape=m, testval=np.zeros(m))

    # priors on factor loadings
    l = np.asarray(factors).sum()
    lam = pm.Normal(name=r"$\lambda$", mu=0, sd=1, shape=l, testval=np.ones(l))

    # loading matrix
    Lambda = tt.zeros(factors.shape)
    k = 0
    for i, j in product(range(p), range(m)):
        if factors[i, j] == 1:
            Lambda = tt.inc_subtensor(Lambda[i, j], lam[k])
            k += 1
    pm.Deterministic(name=r"$\Lambda$", var=Lambda)

    # starting values for factors
    st = np.dot(items, factors) / factors.sum(axis=0)

    # priors on factors
    eta = pm.Normal(name=r"$\eta$", mu=0, sigma=1, shape=(n, m), testval=st)

    # item means
    p = pm.math.sigmoid(nu + matrix_dot(alpha + eta, Lambda.T))

    # # item residual standard deviations
    # d = pm.HalfCauchy(
    #     name=r"$\sqrt{\theta}$", beta=d_beta, shape=p, testval=items.std(axis=0)
    # )

    # observations
    pm.Binomial(name="$Y$", p=p, n=binom_n, observed=items, shape=items.shape)


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

        # define the path to save results
        f = f"../data/BSEM (long) examples/{school} (uni)"

        # select the 19 commonly used variables
        items = sdf[item_names]

        # for numerical convenience, standardize the data
        items = (items - items.mean()) / items.std()

        with pm.Model():

            # construct the model
            bcfau(items, factors, paths)

            if not exists(f):

                # sample and save
                trace = pm.sample(10000, tune=1000, chains=1)
                pm.save_trace(trace, f)
                pm.traceplot(trace, compact=True)
                rcParams["font.size"] = 14
                plt.savefig(f"{f}/traceplot.png")

            else:

                trace = pm.load_trace(f)

        # create a nice summary table
        loadings = pd.DataFrame(
            trace[r"$\Lambda$"].mean(axis=0).round(2)[:, :-1],
            index=[v.title() for v in item_names],
            columns=["Spatial", "Verbal", "Speed", "Memory"],
        )
        loadings.to_csv(f"{f}/loadings.csv")
        print(tabulate(loadings, tablefmt="pipe", headers="keys"))

        _paths = pd.DataFrame(
            trace[r"$\Gamma$"].mean(axis=0).round(2)[:-1, -1],
            index=["Spatial", "Verbal", "Speed", "Memory"],
            columns=["g"],
        )
        _paths.to_csv(f"{f}/factor_paths.csv")
        print(tabulate(_paths, tablefmt="pipe", headers="keys"))


if __name__ == "__main__":
    main()
