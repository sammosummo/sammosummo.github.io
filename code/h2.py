import numpy as np
from scipy.stats import multivariate_normal
from scipy.optimize import minimize
from time import time


# parameters and other constants
n = 1000
beta = np.array([4, 10])
sigma_g = 7
sigma_e = 3

# seed
np.random.seed(1)

# arbitrary "kinship" matrix
A = np.array([np.random.randn(n) + np.random.randn(1) for i in range(n)])
A = np.dot(A, np.transpose(A))
D_half = np.diag(np.diag(A) ** -0.5)
A = np.dot(D_half, np.dot(A, D_half))

# fixed-effects design matrix
X = np.array([np.ones(n), np.random.rand(n)]).transpose()

# breeding values
g = np.random.multivariate_normal(np.zeros(n), A * sigma_g ** 2)

# error
e = np.random.normal(0, sigma_e, n)

# phenotype
y = np.dot(X, beta) + g + e


def nll_1(params):

    *beta_, sigma_g_, sigma_e_ = params
    mu = np.dot(X, np.array(beta_))
    sigma = A * sigma_g_ ** 2 + np.eye(n) * sigma_e_ ** 2
    return -multivariate_normal.logpdf(y, mu, sigma)


def min(func, method):

    start = time()
    x = minimize(func, [1, 1, 1, 1], method=method)
    stop = time()
    print(x.x, (stop - start))


for method in ['Nelder-Mead', 'Powell', 'L-BFGS-B']:

    min(nll_1, method)