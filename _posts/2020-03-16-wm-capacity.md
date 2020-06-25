---
date: 2020-03-16
has_code: true
has_comments: true
has_math: true
include_references: true
layout: post
references:
- Cowan2001a
- Luck2013a
- Ma2014a
- Mathias2018a
- Morey2011a
- Morey2011b
- Pashler1988a
- Rouder2008a
- Salvatier2016a
revisions:
- date: 2020-03-27
  reason: Corrected definition of g
short_title: Working-memory capacity
tags:
- python
- cognition
- memory
- bayesian
title: Measuring working-memory capacity
---
*Working memory* (WM) is the name given to the memory system that stores information over short periods, which is strictly
limited in terms of duration and capacity. In this post, I present a model for measuring WM capacity from psychophysical
data using Bayesian hierarchical inference.

The nature of WM capacity limitation is a source of current debate. Some researchers argue that WM is "slots"-based, stating
that we can remember up to a fixed number of discrete items at once {{ site.data.refs.Luck2013a.citep }}. Others suggest
that WM is a finite flexible resource {{ site.data.refs.Ma2014a.citep }}. Personally, I lean more towards the latter view.
However, item-based storage has long been the dominant view, and the maximum number of items stored in WM, denoted by $$ k $$,
remains a popular dependent variable in the cognitive sciences.

A simple way of measuring $$ k $$ is to apply a formula proposed by either {{ site.data.refs.Pashler1988a.citet }} or
{{ site.data.refs.Cowan2001a.citet }} to the data from a *change-detection task*. On each trial, the observer is presented
with a stimulus comprising several distinct items (e.g., a visual array of objects) and after a few seconds, a second stimulus
is presented. The second stimulus contains at least one item from the original stimulus (the probed item), which may or
may not have changed in some way, and the observer indicates whether a change occurred. The choice of formula depends on
whether the second stimulus also contains the remaining items from the original stimulus: if so, Pashler’s formula should
be used; if it contains just the probed item, Cowan’s should be used.

These formulae are easy to implement and are widely used in research, but there are several problems with them. First, using
these formulae, $$k$$ can only be calculated from trials with the same set size—experiments typically include trials with
various set sizes, so estimates of $$ k $$ must be calculated separately for each set size and then combined, rather than
calculating a single estimate from all the data. Second, since $$k$$ can never exceed the set size, it is systematically
underestimated whenever the set size is smaller than the true $$ k $$. Third, the formulae can yield negative values of
$$ k $$, which are obviously impossible. Fourth, the formulae cannot be used to calculate $$k$$ at all when performance
is at ceiling or floor.

To remedy these issues, {{ site.data.refs.Morey2011b.citet }} formalized a Bayesian hierarchical model for the measurement
of WM capacity from change-detection tasks. The model largely deals with the problems listed above, and is much more
efficient (in the sense that it recovers parameters more accurately for a given data set) than Pashler and Cowan's formulae.
Morey provides his own software to fit the model {{ site.data.refs.Morey2011a.citep }}.

I have implemented my own version of this model using [PyMC3](http://docs.pymc.io/) {{ site.data.refs.Salvatier2016a.citep }}.
My version is not exactly the same as Morey’s. Most notably, it is much simpler—it measures $$ k $$ and other model
variables just once per observer, and doesn't consider the potential effects of other factors. I'll implement a more
complex model that estimates such effects in a later post. My model also contains a reparameterization trick to deal with
the issue of [funneling](funneling). The code only applies to the Cowan style of change-detection tasks, although it would
be easy to modify it to apply to Pashler-style tasks, or indeed any other variation, provided the decision rule can be
specified.

## The model

### Decision process

We assume that, on a given trial, the observer may or may not suffer a *lapse in attention*. When a lapse occurs, the observer
simply guesses same or different, with no regard for the stimulus. When the observer does not lapse, they perform the task
properly. The probability of a non-lapse is denoted by $$ z $$.

On non-lapse trials, the observer remembers up to $$k$$ items from the stimulus. If the set size, $$M$$, is less than or
equal to $$ k $$, all of the items are remembered, but if $$ M > k $$, a random selection of $$k$$ items are remembered.

If the probed item was one of the ones remembered, the observer correctly responds same or different, depending on the type
of trial. If the probed item was not remembered, the observer guesses, just like on a lapse trial. The probability that the
observer guesses different is assumed to be fixed, and is denoted by $$ g $$.

We have fully defined the decision process. Now we can simulate the observer's response on a trial, provided we know the 
set size $$ M $$, whether the correct response was same or different, and the values of the decision variables, $$ z $$,
$$ k $$, and $$ g $$:

~~~python
def trial(M, different, z, k, g):
    # Returns `True` if different
    from numpy.random import uniform
    if uniform() > z:
        if uniform() < g:
            return True
        else:
            return False
    else:
        if uniform() < k / float(M):
            return different
        else:
            if uniform() < g:
                return True
        else:
            return False

~~~

### Hits and false alarms

To fit this model to data, we need to define *hits* and *false alarms* in a similar way to [signal detection theory](sdt),
and connect them to the variables defined above. We arbitrarily define a hit as a correct response on a different trial,
and a false alarm as an incorrect response on a different trial. The observed number of hits, $$H$$, follows the probability
distribution

$$ H \sim \textrm{Binomial}\left(h,D\right) $$

where $$ h $$ is the hit probability, $$ D $$ is the number of different trials. The corresponding probability distribution
for the observed number of false alarms, $$ F $$, is

$$ F \sim \textrm{Binomial}\left(f,S\right) $$

where $$ f $$ is the false-alarm probability and $$ S $$ is the number of same trials.

The relationships between $$ h $$ and $$ f $$, the trial conditions, and the decision parameters defined by these equations:

$$ h=\left(1-z\right)g+zq+z\left(1-q\right)g\\ f=\left(1-z\right)g+z\left(1-q\right)g $$

where

$$ q=\min\left(1,\frac{k}{M}\right) $$

### Hierarchical estimation

Suppose that we have data from several observers and we want to estimate $$ k $$, $$ g $$, and $$ z $$ for each of them.
It is generally a good idea to do inference on normally distributed variables. However, $$ k $$ cannot be normal, because
negative values of $$ k $$ are impossible. Similarly, $$ g $$ and $$ z $$ cannot be normal either, because they are probabilities
and must fall between 0 and 1. Therefore, we apply these transformations:

$$ k=\max\left(\kappa, 0\right)\\ g=\textrm{logistic}\left(\gamma\right)\\ z=\textrm{logistic}\left(\zeta\right) $$

The new Greek-lettered variables can take any values. {{ site.data.refs.Morey2011b.citet }} recommends the $$\max$$ transformation
for $$ k $$, rather than something like $$ \exp $$, because 0 is a meaningful value of $$ k $$.

Next we'll estimate these parameters hierarchically in order to produce partial pooling, and we'll use a non-centered
parameterization in order to avoid [funneling](funneling):

$$ \kappa_i=\mu_{(\kappa)}+\delta_{(\kappa)_i}\sigma_{(\kappa)}\\
\gamma_i=\mu_{(\gamma)}+\delta_{(\gamma)_i}\sigma_{(\gamma)}\\
\zeta_i=\mu_{(\zeta)}+\delta_{(\zeta)_i}\sigma_{(\zeta)} $$

where $$ i $$ indexes the observer, the $$ \mu $$ and $$ \sigma $$ variables represent group trends and spread, respectively,
and the $$ \delta $$ variables represent observer-specific standardized offsets.

### Priors

All that's left to do is place priors on the stochastic variables.

$$ \mu_{(\kappa)}, \mu_{(\gamma)}, \mu_{(\zeta)} \sim \mathrm{Cauchy}\left(0, 5\right)\\
\delta_{(\kappa)_i}, \delta_{(\gamma)_i}, \delta_{(\zeta)_i} \sim \mathrm{Normal}\left(0, 1\right)\\
\sigma_{(\kappa)}, \sigma_{(\gamma)}, \sigma_{(\zeta)} \sim \textrm{Half-Cauchy}\left(5\right) $$

## Application to real data

Now we will apply this model to the [data set]((https://raw.githubusercontent.com/PerceptionCognitionLab/data0/master/wmPNAS2008/lk2clean.csv))
provided by {{site.data.refs.Rouder2008a.citet}}. The following script will download the data, construct the model, sample
from its joint posterior, and produce a figure.

```python
{{ site.data.code.wm-capacity__py }}
```

![](/assets/images/wm-cap.png)
*Posterior traces under the model.*

## Next steps

As mentioned above, this model does not allow us to look for factors that might affect $$ k $$, $$ g $$, and $$ z $$,
such as different conditions in an experiment, or observer-related effects, such as age. This can be achieved by placing
linear models on the group-level parameters. I'll do this in a future post.

## Shameless plug

You can find a real application of this model in one of my papers {{ site.data.refs.Mathias2018a.citep }}.