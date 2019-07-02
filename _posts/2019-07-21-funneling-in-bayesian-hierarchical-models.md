---
layout: post
title: Funneling in Bayesian hierarchical models
date: 2019-07-02
has_code: true
has_comments: true
has_math: true
---

Here is a simple Bayesian hierarchical model. At the lower level of the model, there are $n$ random variables with the
following prior distributions

$$\begin{equation}
x_i\sim\textrm{Normal}\left(\mu,\sigma^2\right)
\end{equation}
$$
 
where $$i$$ indexes the random variable, and $$\mu$$ and $$\sigma$$ are hyperparameters representing means and standard
deviations, respectively. The hyperprior on $$\mu$$ is 

$$\begin{equation}\mu\sim\textrm{Normal}\left(0,1\right)\end{equation}$$

and the hyperprior on $$\sigma$$ is

$$\begin{equation}\mu\sim\textrm{Half-Cauchy}\left(1\right)\end{equation}$$

We can construct this model in PyMC3 very easily.

```python
import pymc3 as pm
import matplotlib.pyplot as plt


with pm.Model():

    n = 2
    mu = pm.Normal(name="$\mu$", mu=0, sd=1)
    sd = pm.HalfCauchy(name="$\sigma$", beta=1)
    x = pm.Normal(name="$x$", mu=mu, sd=sd, shape=n)

```

Quite deliberately, this model contains no data, which means that the joint posterior distribution of the model is
theoretically identical to its joint prior distribution. Therefore, if we estimate the posterior distributions of the
random variables from this model, they should all look like they are supposed to; namely a normal distribution
($$\mu$$), a half-Cauchy ($$sigma$$), and two normal-ish curves ($$x$$).

Let’s add the following lines to the code and see what happens. I’ve deliberately chosen a very short run, so that the sampling finished quickly and the produced figure is small.

```python
    trace = pm.sample(1000, nchains=1)
    pm.traceplot(trace)
    plt.savefig('model_1.png')
```

![](/assets/images/funnel_example_model_1.svg) 

Oh no! The posterior distribution of $\mu$ (top-left panel) looks terrible, not like a normal distribution at all. The top right-hand panel shows the Markov chain produced by the sampling algorithm for this parameter, which has numerous flat portions, indicating that the sampler got “stuck” several times. The chains for the other parameters also look bad.

What happened? Did we choose the wrong sampling method? No—we used no U-turn sampling (NUTS), which is widely considered to be the best sampler currently available and the default choice in PyMC3.

The reason for poor sampling is a phenomenon called _funneling_. [Betancourt and Girolami](https://arxiv.org/pdf/1312.0906.pdf) describe funneling as follows

> Because the $n$ contributions at the bottom of the hierarchy all depend on the global parameters, a small change in [the hyperparameters] induces large changes in the density. Consequently, when the data are sparse the density of these models looks like a “funnel”, with a region of high density but low volume below a region of low density and high volume. The probability mass of the two regions, however, is comparable and any successful sampling algorithm must be able to manage the dramatic variations in curvature in order to fully explore the posterior.

Here, the data are as sparse they can be (i.e., they don’t exist), creating an extreme example of funneling.  Fortunately, there is a relatively reparameterization of the model which eliminates funneling. We create a new collection of standard normal random variables, denoted by $\delta$, to represent the standardized offsets of each $x$ from  $\mu$. Under this new model, $x_i$ is a deterministic variable given by $x_i=\mu+\delta_i\sigma$.

The reparameterized model can be coded and sampled in PyMC3 as follows:

```python
with pm.Model():

    n = 20
    mu = pm.Normal(name="$\mu$", mu=0, sd=1)
    sd = pm.HalfCauchy(name="$\sigma$", beta=1)
    de = pm.Normal(name="$\delta$", mu=0, sd=1, shape=n)
    x = pm.Deterministic("$x$", mu + de * sd)

    trace = pm.sample(1000, nchains=1)
    pm.traceplot(trace)
    plt.savefig('model_2.svg')
```

![](/assets/images/funnel_example_model_2.svg) 

Sampling is now free from the pathology we observed earlier.

I’d like to thank [Thomas Wiecki for his previous post](https://twiecki.io/blog/2017/02/08/bayesian-hierchical-non-centered/), which provides a more detailed yet extremely clear explanation of funneling.



