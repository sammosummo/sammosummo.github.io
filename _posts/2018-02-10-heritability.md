---
layout: post
title: Bayesian estimation of heritability
date: 2018-02-10
categories:
 - Bayesian
 - Genetics
description:
image: https://sammosummo.github.io/images/one-of-the-small-towers-on-frederiksborg-castle-1834.jpg
image-sm: https://sammosummo.github.io/images/one-of-the-small-towers-on-frederiksborg-castle-1834-sm.jpg
image-description: "One of the Small Towers on Frederiksborg Castle (1834–1835) by Christen Købke"

---
Heritability is the proportion of a trait’s variance that is explained by genetic factors[<sup>1</sup>]. Here, I show that it is quite easy to build a simple Bayesian model to estimate heritability using data from related individuals.

Consider the quantitative trait vector $$\mathbf{y}$$, which has a multivariate normal distribution:

$$
\mathbf{y}\sim{}\mathrm{MvNormal}\left{\textbf{\mu},\textbf{\Sigma}\right)
$$