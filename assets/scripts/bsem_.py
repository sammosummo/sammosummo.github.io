"""Bayesian structural equation model (BSEM) using PyMC3.

"""
import numpy as np
import pandas as pd
import pymc3 as pm
import theano.tensor as tt
from matplotlib import pyplot as plt
from pymc3.math import matrix_dot


def cfa(Y, M):
    r"""Bayesian confirmatory factor analysis (CFA) model.

    Args:
        Y (numpy.ndarray): An $n \times p$ matrix of data where $n$ is the sample size
            and $p$ is the number of manifest variables.
        M (numpy.ndarray): An $p \times m$ matrix to describe model structure where $m$
            is the number of latent variables.

    Notes:
        $$\mathbf{Y}$$ probably should be standardized first if you are using continuous
        data.

        Entries in $\mathbf{M}$ should be [0, 1].

        $\mathbf{M}_{(i,j)}$ represents the variance of the normal prior placed on the
        regression coefficient from the $j$th latent variable to the $i$th manifest
        variable. Values of 0 remove the coefficient from the model entirely, 1
        represents a "full-strength" coefficient, and values (0, 1) are for
        cross-loadings.

    """
    # counts
    n, p = Y.shape
    p_, m = M.shape
    assert p == p_, "M is the wrong shape"

    # intercepts for manifest variables
    sd = max(np.abs(Y.mean()).max() * 2.5, 2.5)
    nu = pm.Normal(name=r"$\nu$", mu=0, sd=sd, shape=p, testval=Y.mean())

    # unscaled regression coefficients
    Phi = pm.Normal(name=r"$\Phi$", mu=0, sd=1, shape=M.shape, testval=M)

    # scaled regression coefficients
    Lambda = pm.Deterministic(r"$\Lambda$", Phi * np.sqrt(M))

    # intercepts for latent variables
    alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=2.5, shape=m, testval=0)

    # means of manifest variables
    mu = nu + matrix_dot(Lambda, alpha)

    # standard deviations of manifest variables
    D = pm.HalfCauchy(name=r"$D$", beta=2.5, shape=p, testval=Y.std())

    # correlations between manifest variables
    Omega = np.eye(p)

    # covariance matrix for manifest variables
    Theta = pm.Deterministic(r"$\Theta$", D[None, :] * Omega * D[:, None])

    # covariance matrix on latent variables
    f = pm.Lognormal.dist(sd=0.25)
    L = pm.LKJCholeskyCov(name=r"$L$", eta=1, n=m, sd_dist=f)
    ch = pm.expand_packed_triangular(m, L, lower=True)
    Gamma = tt.dot(ch, ch.T)
    sd = tt.sqrt(tt.diag(Gamma))
    Psi = pm.Deterministic(r"$\Psi$", Gamma / sd[:, None] / sd[None, :])

    # covariance of manifest variables
    Sigma = matrix_dot(Lambda, Psi, Lambda.T) + Theta

    # observations
    pm.MvNormal(name="Y", mu=mu, cov=Sigma, observed=Y, shape=Y.shape)


def main():

    df = pd.read_csv("../../assets/data/HS.csv", index_col=0)

    for school, Y in df.groupby("school"):

        for x in (0, 0.1):

            name = f"{school}_{'%.1f' % x}"
            Y = Y[
                [
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
            ]  # just the 19 commonly used variables
            Y = (Y - Y.mean()) / Y.std()  # for numerical convenience
            M = np.array(
                [
                    [1, x, x, x],
                    [1, x, x, x],
                    [1, x, x, x],
                    [1, x, x, x],
                    [x, 1, x, x],
                    [x, 1, x, x],
                    [x, 1, x, x],
                    [x, 1, x, x],
                    [x, 1, x, x],
                    [x, x, 1, x],
                    [x, x, 1, x],
                    [x, x, 1, x],
                    [x, x, 1, x],
                    [x, x, x, 1],
                    [x, x, x, 1],
                    [x, x, x, 1],
                    [x, x, x, 1],
                    [x, x, x, 1],
                    [x, x, x, 1],
                ]
            )  # hypothesized structure

            with pm.Model():

                print(name)
                cfa(Y, M)
                trace = pm.sample(15000, tune=5000, chains=2)
                pm.traceplot(trace, compact=True)
                plt.savefig(f"{name}.png")
                pm.save_trace(trace, name)


if __name__ == "__main__":
    main()
