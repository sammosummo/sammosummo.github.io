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

[<sup>1</sup>]: https://doi.org/10.1038/nrg2322 "Visscher, P. M., Hill, W. G., & Wray, N. R. (2008). Heritability in the genomics era — concepts and misconceptions. Nature Reviews Genetics, 9(4), 255–266."

$$
\sigma^2_\textrm{P} = \sigma^2_\textrm{G} + \sigma^2_\textrm{E}
$$

Genetic variance can be further decomposed into additive, dominance, and epistatic components:

$$
\sigma^2_\textrm{G} = \sigma^2_\textrm{A} + \sigma^2_\textrm{D} + \sigma^2_\textrm{I}
$$

An *additive* genetic effect is when an allele at a given locus contributes to the trait. For example, suppose a specific locus influences human height. A person with a copy of the minor allele at this locus (Aa) will be taller, all other things being equal, than a person without a copy of the minor allele (AA). A person with two copies of the minor allele (aa) will be even taller, on average.

*Dominance* refers to the effects of interactions between alleles at the same locus. For example, suppose a locus influences height, but that the major allele is dominant over the minor allele. In this case, a single copy of the minor allele would make no difference to a person’s height. However, two copies of the minor allele (aa) would cause them to be taller, all other things being equal.

*Epistasis* refers to interactions between alleles at different loci. For example, the minor allele at one locus causes a person to be taller, but only when another minor allele is present at a different locus.

Similarly, environmental variance can be decomposed into common effects, unique effects, and residual error:

$$
\sigma^2_\textrm{E} = \sigma^2_\textrm{CE} + \sigma^2_\textrm{UE} + \sigma^2_\textrm{RE}
$$

*Common* environmental effects are those shared between two or more individuals in the cohort. *Unique* environmental effects are those specific to one individual—these would be shared, however, between multiple measurements of the trait taken from the same individual (i.e., repeated measures). *Residual error* is specific to a single individual and measure. To keep things simple going forward, let’s assume no common or unique environmental effects, so that:

$$
\sigma^2_\textrm{E} = \sigma^2_\textrm{RE}
$$

Heritability is defined as the proportion of the phenotypic variance that is genetic:

$$
H^2 = \frac{\sigma^2_\textrm{G}}{\sigma^2_\textrm{P}}
$$

This is also called *broad-sense heritability*. Another kind of heritability, or *narrow-sense heritability*, is defined as the proportion of the phenotypic variance that is explained by additive genetic factors (i.e., ignoring dominance and epistasis):

$$
h^2 = \frac{\sigma^2_\textrm{A}}{\sigma^2_\textrm{P}}
$$

It turns out that for complex traits, most genetic variance is additive[<sup>2</sup>], making narrow-sense heritability a useful statistic in the modern genomics era. From here on, I refer to narrow-sense heritability as just heritability.

[<sup>2</sup>]: https://doi.org/10.1371/journal.pgen.1000008 "Hill, W. G., Goddard, G. E., & Visscher, P. M. (2008). Data and theory point to mainly additive genetic variance for complex traits. PLoS Genetics, 4(2): e1000008."

So now that we have defined heritability, how do we estimate it?

The first step is to place a linear mixed-effects model on the quantitative trait. You may be familiar with linear mixed-effects models from the perspective of regression (see [here](https://ourcodingclub.github.io/2017/03/15/mixed-models.html)).