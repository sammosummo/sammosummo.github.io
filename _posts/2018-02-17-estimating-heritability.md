---
layout: post
title: Estimating heritability
date: 2018-02-15
categories:
- Genetics
description:
image: https://sammosummo.github.io/images/Pieter_Bruegel_the_Elder-_The_Seven_Deadly_Sins_or_the_Seven_Vices_-_Gluttony.JPG
image-sm: https://sammosummo.github.io/images/Pieter_Bruegel_the_Elder-_The_Seven_Deadly_Sins_or_the_Seven_Vices_-_Gluttony_sm.JPG
image-description: "Guttony (1558) by Pieter Bruegel the Elder"
---

[Previously](https://sammosummo.github.io/2018/02/10/heritability/), I presented the theory behind the method of variance components for estimating heritability. Here, I simulate some data according to the theory, and recover its parameters using maximum likelihood (ML).
 
We can simulate a trait according to the process

$$
\mathbf{y} \sim \mathrm{MvNormal}\left(\mathbf{X}\beta, \left[\mathbf{A}h^2 + \mathbf{I}\left(1-h^2\right)\right]\right)
$$

where $$\mathbf{y}$$ is the trait vector, $$\mathbf{X}$$ is an arbitrary design matrix, $$\beta$$ is a vector of coefficients, $$\mathbf{A}$$ is an arbitrary kinship matrix, $$\mathbf{I}$$ is an identity matrix, and $$h^2$$ is the narrow-sense heritability. The total or phenotypic variance of this trait will always be 1.

The following Python code generates 500 values of a trait with heritability of 0.5. It also generates random design and kinship matrices, which are needed to recover the trait’s heritability.
 
~~~ python
import numpy as np

np.random.seed(0)

beta = np.array([1, 2, 3])
h2 = 0.5
n = 500

X = np.random.rand(n, len(beta))
X[:, 0] = np.ones(n)  # design mtrx w/ intcpt

r = np.random.randn
A = np.array([r(n) + r(1) for i in range(n)])
A = np.dot(A, np.transpose(A))
Dh = np.diag(np.diag(A) ** -0.5)
A = np.dot(Dh, np.dot(A, Dh))  # kinship mtrx

mvn = np.random.multivariate_normal
I = np.eye(n)
y = mvn(np.dot(X, beta), A * h2 + I * (1 - h2))
~~~

The trait values look like this:

~~~
[ 5.71247592  4.28558369  6.45218623  2.4389544   4.63147031  2.13295085
  5.86265059  3.70842926  3.7455305   4.33422427  3.94104989  1.95915748
 …
~~~

We can find ML estimates of $$\beta$$ and $$h^2$$ quickly and easily using SciPy’s optimisation routines. The limited-memory BFGS algorithm[<sup>1</sup>] works well.

[<sup>1</sup>]: https://doi.org/10.1137/0916069 "Byrd, R. H., Lu,P., Nocedal, J., & Zhu, C. (1995). A limited memory algorithm for bound constrained optimization. SIAM Journal on Scientific and Statistical Computing. 16(5), 1190–1208."

~~~python
from scipy.stats import multivariate_normal
from scipy.optimize import minimize

def f(params):
    """Function to minimise."""
    *beta_, h2_ = params
    mu = np.dot(X, beta_)
    cov = A * h2_ + np.eye(n) * (1 - h2_)
    ll = multivariate_normal.logpdf(y, mu, cov)
    return -ll

x0 = np.zeros(len(beta) + 1)
b = [(None, None)] * len(beta) + [(0, 1)]
result = minimize(f, x0, method='L-BFGS-B', bounds=b)
~~~

The `result` object looks like this:

~~~
      fun: 616.3858826051669
 hess_inv: <4x4 LbfgsInvHessProduct with dtype=float64>
      jac: array([ 0.0017053 , -0.00621867,  0.00106866,  0.0063892 ])
  message: b'CONVERGENCE: REL_REDUCTION_OF_F_<=_FACTR*EPSMCH'
     nfev: 80
      nit: 13
   status: 0
  success: True
        x: array([ 1.05540513,  1.78761443,  3.16921527,  0.54159681])
~~~

This produced the correct estimates in just a few seconds on my MacBook Air (2011). Not bad for illustrative purposes, but this might impractically slow for real-world data sets with thousands — if not tens or even hundreds of thousands — of data points. It also doesn’t help improve our understanding because the most important steps (calculation of the log likelihood and the minimisation routine) were done under the hood by SciPy.

Let’s implement our own version of the multivariate normal log likelihood function, which is

$$
\ln\left(L\right)=-\frac{1}{2}\ln\left(\lvert\Sigma\rvert\right)+\left(\mathbf{x}-\mu\right)^\mathrm{T}\Sigma^{-1}\left(\mathbf{x}-\mu\right)+k\ln\left(2\pi\right)
$$