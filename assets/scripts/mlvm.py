"""Example of a multivariate latent variable mdoel.

"""
import numpy as np
import pymc3 as pm
import pandas as pd
import statsmodels.api as sm
import theano.tensor as tt

from numpy.random import multivariate_normal as mvn
from scipy.stats import binom
from scipy.special import expit


if __name__ == '__main__':

    # simulate some data
    n = 500
    X = np.ones((n, 1))
    B = np.array([[-0.5], [0], [0.5]]).T
    c = 0.5
    Sigma = np.array([[1, c, -c], [c, 1, 0], [-c, 0, 1]])
    E = mvn([0, 0, 0], Sigma, size=n)
    Psi = np.dot(X, B) + E
    Pi = expit(Psi)
    Y = binom.rvs(np.ones_like(Pi).astype(int), Pi)

    for i in range(3):

        # frequentist logistic regressions
        logit = sm.Logit(Y[:, i], X)
        result = logit.fit()
        print(result.summary())

    # Bayesian logistic regressions
    with pm.Model():

        for i in range(3):
            betas = pm.Normal(name=f"betas_{i}", sd=2.5, shape=1, testval=0)
            pi = pm.math.sigmoid(pm.math.matrix_dot(X, betas))
            pm.Bernoulli(name=f"Y_{i}", p=pi, observed=Y[:, i])

        trace = pm.sample(12000, tune=2000)
        print(pm.summary(trace))

    # Bayesian multivariate LVM
    with pm.Model():

        B = pm.Normal(name=f"B", sd=2.5, shape=B.shape, testval=0)
        Mu = pm.math.matrix_dot(X, B)

        # Prior on the correlation matrix ----------------------------------------------
        f = pm.Lognormal.dist(sd=1)
        L = pm.LKJCholeskyCov(name="L", eta=1, n=3, sd_dist=f)
        ch = pm.expand_packed_triangular(3, L, lower=True)
        cov = pm.math.matrix_dot(ch, ch.T)
        sd = tt.sqrt(tt.diag(cov))
        Theta = pm.Deterministic("Theta", cov / sd[:, None] / sd[None, :])
        # ------------------------------------------------------------------------------

        Psi = pm.MvNormal(name="Psi", mu=Mu, cov=Theta, shape=Y.shape)
        Pi = pm.math.sigmoid(Psi)
        pm.Bernoulli(name="Y", p=Pi, observed=Y)

        trace = pm.sample(15000, tune=5000)
        print(pm.summary(trace, var_names=["B", "Theta"]))

