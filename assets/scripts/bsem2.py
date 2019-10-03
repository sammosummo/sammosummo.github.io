"""Bayesian structural equation modeling in PyMC3

This is an attempt to implement Bayesian structural equation modeling (BSEM), as
described by Muthen and Asparouhov (2012), using the Holzinger and Swineford (1939) data
set.

"""
import numpy as np
import pandas as pd
import pymc3 as pm
import theano.tensor as tt
from matplotlib import pyplot as plt
from pymc3.math import matrix_dot


def main():
    """Construct and fit the model, and create summary.

    """
    # load and format the data
    df = pd.read_csv("../../assets/data/HS.csv", index_col=0)
    df = df[df.school == "Pasteur"]  # just one school
    df = df[
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
    df = (df - df.mean()) / df.std()  # standardize for numerical convenience

    # hypothesized factor structure
    M = np.array(
        [
            [1, 0.01, 0.01, 0.01],
            [1, 0.01, 0.01, 0.01],
            [1, 0.01, 0.01, 0.01],
            [1, 0.01, 0.01, 0.01],
            [0.01, 1, 0.01, 0.01],
            [0.01, 1, 0.01, 0.01],
            [0.01, 1, 0.01, 0.01],
            [0.01, 1, 0.01, 0.01],
            [0.01, 1, 0.01, 0.01],
            [0.01, 0.01, 1, 0.01],
            [0.01, 0.01, 1, 0.01],
            [0.01, 0.01, 1, 0.01],
            [0.01, 0.01, 1, 0.01],
            [0.01, 0.01, 0.01, 1],
            [0.01, 0.01, 0.01, 1],
            [0.01, 0.01, 0.01, 1],
            [0.01, 0.01, 0.01, 1],
            [0.01, 0.01, 0.01, 1],
            [0.01, 0.01, 0.01, 1],
        ]
    )

    # construct the model
    with pm.Model():

        # counts
        n, p = df.shape
        p_, m = M.shape
        assert p == p_, "incorrect shape for M"

        # intercepts for manifest variable
        nu = pm.Normal(name=r"$\nu$", mu=0, sd=5, shape=p, testval=df.mean())

        # unscaled loadings
        Phi = pm.Normal(name=r"$\Phi$", mu=0, sd=1, shape=M.shape, testval=M)

        # scaled loadings
        Lambda = pm.Deterministic(r"$\Lambda$", Phi * M)

        # intercepts for latent variables
        alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=5, shape=m, testval=0)

        # means of manifest variables
        mu = nu + matrix_dot(Lambda, alpha)

        # standard deviations of manifest variables
        D = pm.HalfCauchy(name=r"$D$", beta=2.5, shape=p, testval=1)

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
        pm.MvNormal(name="Y", mu=mu, cov=Sigma, observed=df, shape=df.shape)

        # sample
        trace = pm.sample(15000, tune=5000, chains=2)
        pm.traceplot(trace, compact=True)
        plt.savefig("tmp.png")

        pm.save_trace(trace, "bsem_hs_modelb")


if __name__ == "__main__":
    main()
