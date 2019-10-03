"""Bayesian structural equation modeling in PyMC3

This is an attempt to implement Bayesian structural equation modeling (BSEM), as
described by Muthen and Asparouhov (2012), using the Holzinger and Swineford (1939) data
set.

"""
import numpy as np
import pandas as pd
import pymc3 as pm
import matplotlib as mp
import theano.tensor as tt
from matplotlib import pyplot as plt
from pymc3.math import matrix_dot


mp.rc('text', usetex=True)
mp.rcParams["text.latex.preamble"] = [r"\usepackage{bm}"]


def main():
    """Construct and fit the model, and create summary.

    """
    # load and format the data
    df = pd.read_csv("../../assets/data/HS.csv", index_col=0)
    df = df[df.school == "Pasteur"]  # just one school
    df = df[[
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
        "figurew"
    ]]  # just the 19 commonly used variables
    df = (df - df.mean()) / df.std()  # standardize for numerical convenience

    # define hypothesized factor structure
    M = np.array([
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
    ])

    # construct the model
    with pm.Model():

        # counts
        n, p = df.shape
        p_, m = M.shape
        assert p == p_, "incorrect shape for M"

        # priors on manifest variable intercepts
        nu = pm.Normal(name=r"$\bm{\nu}$", mu=0, sd=10, shape=p, testval=df.mean())

        # priors on loadings
        l = pm.Normal(
            name=r"$\bm{\Lambda^{*}}$", mu=0, sd=10, shape=M.shape, testval=M
        )
        Lambda = pm.Deterministic(r"$\bm{\Lambda}$", l * M)

        # priors on latent variable intercepts
        alpha = pm.Normal(name=r"$\bm{\alpha}$", mu=0, sd=10, shape=m, testval=0)

        # means of manifest variables
        mu = nu + matrix_dot(Lambda, alpha)

        # priors on manifest variable standard deviations
        D = pm.HalfCauchy(name=r"$\bm{D}$", beta=2.5, shape=p, testval=1)

        # prior on manifest variable correlation matrix
        Ta = np.eye(p)

        # manifest variable covariance matrix
        Theta = pm.Deterministic(r'$\bm{\Theta}$', D[None, :] * Ta * D[:, None])

        # prior on latent variable correlation matrix
        # Psi = np.eye(m)
        sd_dist = pm.HalfNormal.dist(sd=1)
        packed_chol = pm.LKJCholeskyCov(name='_chol_cov', eta=1, n=m, sd_dist=sd_dist)
        chol = pm.expand_packed_triangular(m, packed_chol, lower=True)
        cov = tt.dot(chol, chol.T)
        sd = tt.sqrt(tt.diag(cov))
        Psi = pm.Deterministic(r"$\bm{Psi$}", cov / sd[:, None] / sd[None, :])
        # Psi = tt.fill_diagonal(pf[np.zeros((m, m), dtype=np.int64)], 1.)

        # covariance of manifest variables
        Sigma = matrix_dot(Lambda, Psi, Lambda.T) + Theta

        # observations
        pm.MvNormal(name="Y", mu=mu, cov=Sigma, observed=df)

        # sample
        trace = pm.sample(chains=2)
        pm.traceplot(trace, compact=True)
        plt.savefig("tmp.png")

        # # priors on loadings
        # lambdas = pm.Normal(name=r"$\lambda$", mu=0, sd=1, shape=k, testval=[0] * k)
        #
        # # loading matrix
        # # TODO: There must be a better way to do this!
        # Lambda = tt.stack([
        #     tt.stack([1, 0, 0, 0], axis=0),
        #     tt.stack([lambdas[0], 0, 0, 0], axis=0),
        #     tt.stack([lambdas[1], 0, 0, 0], axis=0),
        #     tt.stack([lambdas[2], 0, 0, 0], axis=0),
        #     tt.stack([0, 1, 0, 0], axis=0),
        #     tt.stack([0, lambdas[3], 0, 0], axis=0),
        #     tt.stack([0, lambdas[4], 0, 0], axis=0),
        #     tt.stack([0, lambdas[5], 0, 0], axis=0),
        #     tt.stack([0, lambdas[6], 0, 0], axis=0),
        #     tt.stack([0, 0, 1, 0], axis=0),
        #     tt.stack([0, 0, lambdas[7], 0], axis=0),
        #     tt.stack([0, 0, lambdas[8], 0], axis=0),
        #     tt.stack([0, 0, lambdas[9], 0], axis=0),
        #     tt.stack([0, 0, 0, 1], axis=0),
        #     tt.stack([0, 0, 0, lambdas[10]], axis=0),
        #     tt.stack([0, 0, 0, lambdas[11]], axis=0),
        #     tt.stack([0, 0, 0, lambdas[12]], axis=0),
        #     tt.stack([0, 0, 0, lambdas[13]], axis=0),
        #     tt.stack([0, 0, 0, lambdas[14]], axis=0),
        # ])
        #
        # # priors on latent var intercepts
        # alpha = pm.Normal(name=r"$\alpha$", mu=0, sd=1, shape=m, testval=[0] * m)
        # # alpha = np.zeros(m)
        #
        # # means of manifest variables
        # mu = nu + matrix_dot(Lambda, alpha)
        #
        # # priors on manifest variable standard deviations
        # s = pm.HalfCauchy(name=r"$\sqrt{\theta}}$", beta=2.5, shape=p, testval=[1] * p)
        # Theta = tt.diag(s ** 2)
        #
        # # # prior on the latent variable covariance matrix
        # # packed_L = pm.LKJCholeskyCov(
        # #     name=r'$\mathbf{L}$', n=m, eta=1., sd_dist=pm.HalfCauchy.dist(2.5)
        # # )
        # # L = pm.expand_packed_triangular(m, packed_L)
        # # Psi = L.dot(L.T)
        #
        # # priors on latent variable standard deviations
        # # ps = pm.HalfCauchy(name=r"$\sqrt{\psi}}$", beta=2.5, shape=m, testval=[1] * m)
        # ps = np.ones(m)
        #
        # # priors on latent variable correlations
        # # omega = pm.LKJCorr(name="r$\omega$", eta=1, n=m)
        # omega = np.zeros(m)
        # ix = np.array([np.roll(np.arange(m), 1 - i) for i in range(m)])
        # Omega = tt.fill_diagonal(omega[ix], 1)
        # D = tt.diag(ps)
        # Psi = matrix_dot(D, Omega, D)
        # # Psi = tt.diag(ps ** 2)
        #
        # # covariance of manifest variables
        # Sigma = matrix_dot(Lambda, Psi, Lambda.T) + Theta
        #

if __name__ == "__main__":
    main()
