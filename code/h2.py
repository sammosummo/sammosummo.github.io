import numpy as np
from scipy.stats import multivariate_normal
from scipy.optimize import minimize
from time import time


def gen_data(β, σA, σE, n):
    """Generate a trait.

    Args:
        β (array): m-length vector of coefficients.
        σA (float): Additive genetic std.
        σE (float): Residual std.
        n (int): number of observations.

    Returns:
        X (array): n-by-m design matrix.
        A (array): n-by-n kinship matrix.
        u (array): n-length vector of breeding values.
        e (array): n-length vector of errors.
        y (array): n-length phenotype vector.

    """
    if not hasattr(β, '__iter__'):

        β = np.array(β)

    X = np.random.rand(n, len(β))
    X[:, 0] = np.ones(n)

    A = np.array([np.random.randn(n) + np.random.randn(1) for i in range(n)])
    A = np.dot(A, np.transpose(A))
    D_half = np.diag(np.diag(A) ** -0.5)
    A = np.dot(D_half, np.dot(A, D_half))

    u = np.random.multivariate_normal(np.zeros(n), A * σA ** 2)

    e = np.random.normal(0, σE, n)

    y = np.dot(X, β) + u + e

    return X, A, u, e, y


def crude_mle(X, A, y):
    """Crudely find parameter values using iterative MLE.

    """
    def f(θ):
        """Function to minimise."""
        *_β, _σA, _σE = θ
        μ = np.dot(X, _β)
        Σ = np.dot(A, _σA ** 2) + np.dot(np.eye(len(y)), _σE ** 2)

        return -multivariate_normal.logpdf(y, μ, Σ)

    result = minimize(f, np.ones(X.shape[1] + 2), method='L-BFGS-B')

    return result.x


def main():

    print('generating data ...')
    X, A, u, e, y = gen_data([1, 2, 3], 9, 3, 1500)
    print('recovering parameters ...')
    start = time()
    θ = crude_mle(X, A, y)
    stop = time()
    print('values:', θ)
    print('time taken: %i second(s)' % np.round(stop - start))


if __name__ == '__main__':

    main()