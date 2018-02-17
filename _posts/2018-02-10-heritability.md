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

Previously, I presented the theory behind the method of variance components for estimating heritability. Here, I simulate some data according to the theory, and attempt to recover its parameters using various methods.
 
Let’s start by defining the parameters we wish to recover.

~~~ python
n = 1000
beta = np.array([4, 10])
sigma_g = 7
sigma_e = 3
~~~

Next we’ll generate the data according to the process $$\mathbf{y} \sim \mathrm{MvNormal}\left(\mathbf{X}\beta, \mathbf{A}\sigma^2_\mathrm{A} + \mathbf{I}\sigma^2_\mathrm{E}\right)$$. See my [previous post](https://sammosummo.github.io/2018/02/10/heritability/) for an explanation of where this comes from.

~~~python
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
~~~


