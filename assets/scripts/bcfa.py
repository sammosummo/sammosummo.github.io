"""Example of Bayesian confirmatory factor analysis in PyMC3.

"""
import numpy as np
import pandas as pd
import pymc3 as pm
import theano.tensor as tt
import matplotlib.pyplot as plt
from os.path import exists

from matplotlib import rcParams
from pymc3.math import matrix_dot
from tabulate import tabulate


def bcfa(
    items,
    factors,
    beta="estimate",
    nu_sd=2.5,
    alpha_sd=2.5,
    d_beta=2.5,
    corr_items=True,
    corr_factors=True,
    g_eta=100,
    l_eta=1,
    beta_beta=1,
):
    r"""Constructs a Bayesian CFA model.

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
        corr_factors (:obj:`bool`, optional): Allow correlated factors.
        corr_items (:obj:`bool`, optional): Allow correlated items.
        g_eta (:obj:`float`, optional): Shape parameter of LKJ prior on residual item
            correlation matrix.
        l_eta (:obj:`float`, optional): Shape parameter of LKJ prior on factor
            correlation matrix.
        beta_beta (:obj:`float`, optional): Beta parameter of beta prior on beta.

    Returns:

        None: Places model in context.

    """
    # get numbers of cases, items, and factors
    n, p = items.shape
    p_, m = factors.shape
    assert p == p_, "Mismatch between data and factor-loading matrices"

    # place priors on item and factor intercepts
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=nu_sd, shape=p, testval=items.mean(axis=0))
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=alpha_sd, shape=m, testval=np.zeros(m))

    # place priors on unscaled factor loadings
    Phi = pm.Normal(name=r"$\Phi$", mu=0, sd=1, shape=factors.shape, testval=factors)

    # create masking matrix for factor loadings
    if isinstance(beta, str):
        assert beta == "estimate", f"Don't know what to do with '{beta}'"
        beta = pm.Beta(name=r"$\beta$", alpha=1, beta=beta_beta, testval=0.1)
    M = (1 - np.asarray(factors)) * beta + np.asarray(factors)

    # create scaled factor loadings
    Lambda = pm.Deterministic(r"$\Lambda$", Phi * M)

    # determine item means
    mu = nu + matrix_dot(Lambda, alpha)

    # place priors on item standard deviations
    D = pm.HalfCauchy(name=r"$D$", beta=d_beta, shape=p, testval=items.std(axis=0))

    # place priors on item correlations
    f = pm.Lognormal.dist(sd=0.25)
    if not corr_items:
        Omega = np.eye(p)
    else:
        G = pm.LKJCholeskyCov(name=r"$G$", eta=g_eta, n=p, sd_dist=f)
        ch1 = pm.expand_packed_triangular(p, G, lower=True)
        K = tt.dot(ch1, ch1.T)
        sd1 = tt.sqrt(tt.diag(K))
        Omega = pm.Deterministic(r"$\Omega$", K / sd1[:, None] / sd1[None, :])

    # determine residual item variances and covariances
    Theta = pm.Deterministic(r"$\Theta$", D[None, :] * Omega * D[:, None])

    # place priors on factor correlations
    if not corr_factors:
        Psi = np.eye(m)
    else:
        L = pm.LKJCholeskyCov(name=r"$L$", eta=l_eta, n=m, sd_dist=f)
        ch = pm.expand_packed_triangular(m, L, lower=True)
        _psi = tt.dot(ch, ch.T)
        sd = tt.sqrt(tt.diag(_psi))
        Psi = pm.Deterministic(r"$\Psi$", _psi / sd[:, None] / sd[None, :])

    # determine variances and covariances of items
    Sigma = matrix_dot(Lambda, Psi, Lambda.T) + Theta

    # place priors on observations
    pm.MvNormal(name="$Y$", mu=mu, cov=Sigma, observed=items, shape=items.shape)


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
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
        ]
    )

    # iterate over the two schools
    for school, sdf in df.groupby("school"):

        # define the path to save results
        f = f"../data/BCFA examples/{school}"

        # select the 19 commonly used variables
        items = sdf[item_names]

        # for numerical convenience, standardize the data
        items = (items - items.mean()) / items.std()

        with pm.Model():

            # construct the model
            bcfa(items, factors)

            if not exists(f):

                # sample and save
                trace = pm.sample(19000, tune=1000, chains=2)
                pm.save_trace(trace, f)
                pm.traceplot(trace, compact=True)
                rcParams["font.size"] = 14
                plt.savefig(f"{f}/traceplot.png")

            else:

                trace = pm.load_trace(f)

        # create a nice summary table
        loadings = pd.DataFrame(
            trace[r"$\Lambda$"].mean(axis=0).round(3),
            index=[v.title() for v in item_names],
            columns=["Spatial", "Verbal", "Speed", "Memory"],
        )
        loadings.to_csv(f"{f}/loadings.csv")
        print(tabulate(loadings, tablefmt="pipe", headers="keys"))
        correlations = pd.DataFrame(
            trace[r"$\Psi$"].mean(axis=0).round(3),
            index=["Spatial", "Verbal", "Speed", "Memory"],
            columns=["Spatial", "Verbal", "Speed", "Memory"],
        )
        correlations.to_csv(f"{f}/factor_correlations.csv")
        print("\n")
        print(tabulate(correlations, tablefmt="pipe", headers="keys"))
        correlations = pd.DataFrame(
            trace[r"$\Omega$"].mean(axis=0).round(3),
            index=item_names,
            columns=item_names,
        )
        correlations.to_csv(f"{f}/item_correlations.csv")


if __name__ == "__main__":
    main()
