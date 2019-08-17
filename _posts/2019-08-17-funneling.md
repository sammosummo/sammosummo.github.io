---
layout: post
title: Non-centered parameterizations of Bayesian hierarchical models
date: 2019-08-17
has_code: true
has_comments: true
has_math: true
include_references: true
references:
 - Neal2003a
 - Gelman2006a
 - Lee2013a
 - Salvatier2016a
 - Hoffman2014a
 - Geman1984a
 - Neal2011a
 - Betancourt2015a
 - Papaspiliopoulos2007a
---

Bayesian hierarchical (or multilevel) models have two or more layers of random variables.
Commonly, variables from one layer are drawn from a parent distribution whose shape
depends on the variables from the layer above it. This imposition of structure on the
random variables causes *partial pooling* (or shrinkage), which can lead to hierarchical
models having drastically improved out-of-sample predictive accuracy compared to their
non-hierarchical counterparts. For a real-world demonstration of this, see
[Gelman (2006)](#Gelman2006a).

Unfortunately, it can be difficult to sample the posterior distributions of hierarchical
models properly, especially when there are few data, due to a phenomenon sometimes called
*funneling*. In this post, I demonstrate funneling using some simple models and show how
it can be remedied via reparameterization.

While the funneling problem and its solution have been written about before, in my
opinion, they are not well known enough among Bayesian modelers. For instance, in their
introductory textbook on Bayesian modeling for cognitive scientists, [Lee and Wagenmakers
(2013)](#Lee2013a) present numerous models that will likely suffer from funneling if
applied to psychological experiments containing few data.

## Neal's funnel

[Neal (2003)](#Neal2003a) provides the classic demonstration of funneling. This
paper was written to show the inadequacies of older Markov chain Monte Carlo (MCMC)
sampling methods, such as Gibbs sampling ([Geman & Geman, 1984](#Geman1984a)). However, as
we shall see momentarily, even contemporary MCMC sampling methods struggle to properly
sample from Neal's funnel.

Suppose we have the following ten normally distributed random variables:

$$\begin{align}
v&\sim\textrm{Normal}\left(0, 3\right)\\
x_i&\sim\textrm{Normal}\left(0,e^v\right)\textrm{ for }i=0\textrm{ to }8\textrm{.}
\end{align}$$

(Actually, we don't need $$x_1$$ to $$x_8$$ to demonstrate funneling, but this is what Neal
used, so we'll stick with it.) Let's simulate some data and visualize this probability
distribution using Python. (Thanks to [Junpeng Lao](https://junpenglao.xyz/) for creating
the [notebook](https://github.com/junpenglao/advance-bayesian-modelling-with-PyMC3/blob/master/Notebooks/Code5%20-%20Neals_Funnel.ipynb)
where I got most of this code.)

```python
{{ site.data.code.neals-funnel-a__py }}
```

![](/assets/images/neals-funnel-a.svg)
*Random samples (left) and log likelihood (right) of two parameters from Neal's funnel,
$$x_0$$ and $$v$$.*


Now let's try to sample from this distribution using [PyMC3](https://docs.pymc.io/), a
Bayesian modeling package for Python [(Salvatier, Wiecki, & Fonnesbeck, 2016)](#Salvatier2016a).
We will definine our random variables and assign them the correct prior
distributions, but will not provide any data with which to update the priors. Thus, the
model's prior and posterior distributions are identical. When we sample from the posterior
distribution using MCMC, we should obtain samples that are extremely similar to the data
we simulated earlier.

For continuous random variables, PyMC3 uses no-U-turn sampling (NUTS;
[Hoffman & Gelman, 2014](#Hoffman2014a)), a form of adaptive Hamiltonian Monte Carlo (HMC;
[Neal, 2011](#Neal2011a)), by default. This sampling method is considered to be state of
the art and is considerably more efficient than older MCMC sampling methods such as
Gibbs.

```python
{{ site.data.code.neals-funnel-b__py }}
```

![](/assets/images/neals-funnel-b.svg)
*The same random samples as before (left) and the posterior samples from the Bayesian
model (right).*

Clearly something has gone wrong. Posterior samples appear to have been drawn from the
top part of the funnel only; small values of $$v$$ are not represented. As mentioned
earlier, [Neal (2003)](#Neal2003a) proposed this example to demonstrate the problems of
older MCMC sampling methods. However, as demonstrated above, NUTS also fails to sample
Neal's funnel correctly (see [Betancourt & Girolami, 2015](#Betancourt2015a)).

## A more realistic example

Neal's funnel is a somewhat unrealistic distribution to propose as a model for any
real-world data-analysis problem. Let's define a distribution that more closely resembles
something we might actually use:

$$\begin{align}
\mu&\sim\textrm{Normal}\left(0,1\right)\\
\sigma&\sim\textrm{Half-Cauchy}\left(1\right)\\
y_{i}&\sim\textrm{Normal}\left(\mu, \sigma^2\right)\textrm{ for }i=0\textrm{ to }n\textrm{.}
\end{align}$$

Here, $$y_0$$ to $$y_n$$ could plausibly be some observed data drawn from the same
distribution whose mean and variance are unknown. For the sake of simplicity we
will set $$n$$ to 1. As demonstrated in by the code and figure below, funneling occurs
here too.

```python
{{ site.data.code.realistic-funnel-a__py }}
```

![](/assets/images/realistic-funnel-a.svg)
*Random samples from the new distribution (blue) and posterior samples from its Bayesian
model (red).*

One can perhaps see that the problem lies in the sampling of the *hyperparameters*, the
higher-level random variables that control the shapes of the prior distributions on the
lower-level variables. In both examples, small values of those variables dictating the
scale of the prior, $$v$$ in Neal's funnel and $$\sigma$$ above, are not represented.

## Reparameterization

As explained by [Betancourt and Girolami (2015)](#Betancourt2015a), the problem is caused
by the fact that random variables within hierarchical models are necessarily highly
dependent on one another when the data are sparse. (Actually, Betancourt and Girolami
describe this as a *correlation* between variables. Perhaps this is the correct term in
a mathematical sense, but in the empirical sciences, correlation usually implies a linear
relationship, and the kinds of dependencies we see in hierarchical models are typically not
linear. For example, the Pearson product–moment coefficient of $$v$$ and
$$x_0$$ in Neal's funnel is 0.) Although modern MCMC sampling methods do better than
older ones, the performance of all methods is degraded in the presence of such
dependencies.

As more data are added, dependencies between random variables in the joint posterior
distribution are reduced, which allows MCMC sampling to better explore it. So long
as a hierarchical model is provided with enough data, funneling is minimized. But
how many data are sufficient? This is a difficult question to answer, but as this [blog post
by Thomas Wiecki](https://www.google.com/search?q=wiecki+funnel&rlz=1C5CHFA_enUS842US842&oq=wiecki+&aqs=chrome.0.69i59j69i57j69i59j0l3.2812j0j4&sourceid=chrome&ie=UTF-8)
shows, funneling occurs in the hierarchical analysis of fairly typical
datasets. Moreover, in almost all real-life data-analysis situations, researchers do not
have the luxury of collecting more data. Therefore, a more general solution is required.

It has long been known that correlations between random variables in hierarchical models
can be reduced by adopting *non-centered parameterizations* (NCPs;
[Papaspiliopoulos, Roberts, & Sköld, 2007](#Papaspiliopoulos2007a)). A successful NCP
of Neal's funnel is

$$\begin{align}
v&\sim\textrm{Normal}\left(0, 3\right)\\
\tilde{x_i}&\sim\textrm{Normal}\left(0,1\right)\textrm{ for }i=0\textrm{ to }8\\
x_i&=e^v\tilde{x_i}\textrm{.}
\end{align}$$

There are two differences between the NCP and the original, centered parameterization:
first, $$x_0$$ through $$x_8$$ are now *deterministic* rather than *stochastic* random
variables, meaning that MCMC sampling methods do not update them directly; second, the
new stochastic random variables, denoted by $$\tilde{x_i}$$, are independent of $$v$$.
This NCP of Neal's funnel is presented in PyMC3 code below, along with a figure that
demonstrates independence between the stochastic random variables and lack of funneling.

```python
{{ site.data.code.neals-funnel-c__py }}
```

![](/assets/images/neals-funnel-c.svg)
*Posterior samples from the NCP of Neal's funnel. As shown in the left panel, the
dependencies between the stochastic random variables are gone. As shown in the right
panel, the joint distribution is sampled properly.*

(Strangely, in other definitions of the NCP of Neal's funnel, such as the one found in the
[Stan user manual](https://mc-stan.org/docs/2_18/stan-users-guide/reparameterization-section.html),
$$v$$ is also a deterministic variable where $$\tilde{v}\sim\textrm{Normal}\left(0,1\right)$$,
and $$v=3\tilde{v}$$. But intuitively one can see that this extra step is not necessary
because it doesn't make any difference to the dependencies between the stochastic random
variables. Perhaps it is included for historical reasons, much like the additional
unnecessary lower-level variables in Neal's funnel.)

Similarly, our second example distribution can be reparameterized as

$$\begin{align}
\mu&\sim\textrm{Normal}\left(0,1\right)\\
\sigma&\sim\textrm{Half-Cauchy}\left(1\right)\\
\tilde{y}_{i}&\sim\textrm{Normal}\left(0, 1\right)\textrm{ for }i=0\textrm{ to }n\\
y&=\mu+\tilde{y}_{i}\sigma\textrm{.}
\end{align}$$

Again, the NCP removes the dependencies between all the stochastic random variables, and
reduces funneling, as shown below.

```python
{{ site.data.code.realistic-funnel-b__py }}
```

![](/assets/images/realistic-funnel-b.svg)
*Posterior samples from the NCP of the second example distribution.*

