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

Environmental variance can be decomposed into common factors, unique factors, and residual error:

$$
\sigma^2_\textrm{E} = \sigma^2_\textrm{CE} + \sigma^2_\textrm{UE} + \sigma^2_\textrm{RE}
$$

Common environmental factors are those shared between two or more individuals in the cohort. Unique environmental factors are those specific to one individual—these would be shared, however, between multiple measurements of the trait taken from the same individual (i.e., repeated measures). Residual error is specific to a single individual and measure.

Suppose we have a normal distributed trait
