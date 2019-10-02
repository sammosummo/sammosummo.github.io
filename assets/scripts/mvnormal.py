import numpy as np
import pymc3 as pm
from matplotlib import pyplot as plt


if __name__ == '__main__':

    with pm.Model():
        mu = np.zeros(3)
        true_cov = np.array([[1.0, 0.5, 0.1],
                             [0.5, 2.0, 0.2],
                             [0.1, 0.2, 1.0]])
        data = np.random.multivariate_normal(mu, true_cov, 100)
        print(data)

        sd_dist = pm.HalfCauchy.dist(beta=2.5, shape=3)
        chol_packed = pm.LKJCholeskyCov('chol_packed',
            n=3, eta=2, sd_dist=sd_dist)
        chol = pm.expand_packed_triangular(3, chol_packed)
        vals = pm.MvNormal('vals', mu=mu, chol=chol, observed=data)

        trace = pm.sample()
        pm.traceplot(trace)
        plt.savefig("tmp.png")