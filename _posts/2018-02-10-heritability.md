---
layout: post
title: Heritability
date: 2018-02-10
categories:
- Genetics
description:
image: https://sammosummo.github.io/images/6005224610_3c82918a2f_o.jpg
image-sm: https://sammosummo.github.io/images/6005224610_81af12b832_z.jpg
image-description: "From Illustriertes Prachtwerk sämtlicher Tauben-rassen (ca. 1906) by E. Schachtzabel"
---

Heritability remains one of the core concepts in quantitative genetics. It is actually quite easy to build a model to estimate the heritability of a quantitative trait, provided one knows the familial relationships between individuals in the sample.

As explained nicely in this article[<sup>1</sup>], the total (or phenotypic) variance of a trait has both genetic and environmental components:

[<sup>1</sup>]: https://doi.org/10.1038/nrg2322 "Visscher, P. M., Hill, W. G., & Wray, N. R. (2008). Nature Reviews Genetics, 9(4), 255–266."

$$
\sigma^2_\textrm{P} = \sigma^2_\textrm{G} + \sigma^2_\textrm{E}
$$

Broad-sense heritability, denoted by $$H^2$$, is defined as the proportion of the phenotypic variance that is genetic:

$$
H^2 = \frac{\sigma^2_\textrm{G}}{\sigma^2_\textrm{P}}
$$

Genetic variance has additive, dominance, and epistatic components:

$$
\sigma^2_\textrm{G} = \sigma^2_\textrm{A} + \sigma^2_\textrm{D} + \sigma^2_\textrm{I}
$$

Dominance refers to the effects of interactions between alleles at the same locus, whereas epistatic refers to interactions between alleles at different loci. For complex traits, it is likely that most genetic variance is additive. Therefore, nowadays quantitative genetics is mostly interested in narrow-sense heritability, denoted by $$h^2$$, which is defined as the proportion of the phenotypic variance that is explained by additive genetic factors:

$$
h^2 = \frac{\sigma^2_\textrm{A}}{\sigma^2_\textrm{P}}
$$

Environmental variance can be decomposed into common effects, unique effects, and residual error:

$$
\sigma^2_\textrm{E} = \sigma^2_\textrm{CE} + \sigma^2_\textrm{UE} + \sigma^2_\textrm{RE}
$$

Common environmental effects are those shared between two or more individuals in the cohort. Unique environmental effects are those specific to one individual—these would be shared, however, between multiple measurements of the trait taken from the same individual (i.e., repeated measures). Residual error is specific to a single individual and measure. Here, just like we assumed no dominance or epistasis, we are going to assume no common or unique environment effects, so that

$$
\sigma^2_\textrm{E} = \sigma^2_\textrm{RE}
$$

With these concepts defined, how do we estimate $$h^2$$?

Let $$\mathbf{y}$$ denote a 1-by-$$n$$ matrix (or vector), where $$n$$ is the number of individuals for whom we have data, and where $$y_i$$ is the trait value for the $$i$$th individual:

$$
\mathbf{y} = \begin{pmatrix} 
a & b \\
c & d 
\end{pmatrix}
$$

 First, we place a linear mixed-effects model on $$\mathbf{y}$$:

$$
\mathbf{y} = \mathbf{X}\beta + \mathbf{g} + \mathbf{e}
$$

Here, $$\mathbf{X}$$ is a $$m$$-by-$$n$$ matrix of fixed-effects covariates (i.e., a design matrix). Typically, values in the first column are all 1 (the intercept). The remaining columns are filled with non-genetic covariates that are likely to influence the trait, such as age and sex. $$\beta$$ is a 1-by-$$m$$ matrix of coefficients to be estimated. $$g$$ is a 1-by-$$n$$ matrix of genetic (or breeding) values. Typically, breeding values are unknown, so we model this as a multivariate normal random distribution:

$$
g\sim{}\mathrm{MvNormal}\left(0, \mathbf{A}\right)
$$

where $$A$$ is a variance-covariance matrix.