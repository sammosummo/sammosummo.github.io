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


class Constant(pm.Continuous):
    """I defined a continuous distribution so that its dist() function could be used to
    create a JKL correlation prior. All I did was change pm.Constant from a subclass of
    pm.Discrete to pm.Continuous, and removed the bound function from logp method.

    """

    def __init__(self, c, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mean = self.median = self.mode = self.c = c = tt.as_tensor_variable(c)

    def random(self, point=None, size=None):
        c = pm.draw_values([self.c], point=point, size=size)[0]
        dtype = np.array(c).dtype

        def _random(c, dtype=dtype, size=None):
            return np.full(size, fill_value=c, dtype=dtype)

        return pm.generate_samples(
            _random, c=c, dist_shape=self.shape, size=size
        ).astype(dtype)

    def logp(self, value):
        c = self.c
        return tt.eq(value, c)

    def _repr_latex_(self, name=None, dist=None):
        if dist is None:
            dist = self
        name = r"\text{%s}" % name
        return r"${} \sim \text{{Constant}}()$".format(name)


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
        L = pm.LKJCholeskyCov(name=r"$L$", eta=1, n=m, sd_dist=Constant.dist(c=1))
        ch = pm.expand_packed_triangular(m, L, lower=True)
        Psi = pm.Deterministic(r"$\Psi$", tt.dot(ch, ch.T))

        # covariance of manifest variables
        Sigma = matrix_dot(Lambda, Psi, Lambda.T) + Theta

        # observations
        # pm.MvNormal(name="Y", mu=mu, cov=Sigma, observed=df, shape=df.shape)

        # sample
        trace = pm.sample(15000, tune=5000, chains=2)
        pm.traceplot(trace, compact=True)
        plt.savefig("tmp.png")

        # pm.save_trace(trace, "bsem_hs_modelb")


if __name__ == "__main__":
    main()
