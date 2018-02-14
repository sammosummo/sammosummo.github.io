---
layout: post
title: Heritability, part I
date: 2018-02-10
categories:
- Genetics
description:
image: https://sammosummo.github.io/images/6005224610_3c82918a2f_o.jpg
image-sm: https://sammosummo.github.io/images/6005224610_81af12b832_z.jpg
image-description: "From Illustriertes Prachtwerk sämtlicher Tauben-rassen (ca. 1906) by E. Schachtzabel"
---

Heritability remains one of the core concepts in quantitative genetics. A number of methods for estimating heritability have been proposed, but these days the most commonly used method is variance-components decomposition. This method is actually is quite straightforward, and is described below.

As explained in this article[<sup>1</sup>], the total (or phenotypic) variance of a trait has both genetic and environmental components:

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

*Common* environmental effects are those shared between two or more individuals in the cohort. *Unique* environmental effects are those specific to one individual — these would be shared, however, between multiple measurements of the trait taken from the same individual (i.e., repeated measures). *Residual error* is specific to a single individual and measure. To keep things simple going forward, let’s assume no common or unique environmental effects, so that:

$$
\sigma^2_\textrm{E} = \sigma^2_\textrm{RE}
$$

Heritability is defined as the proportion of the phenotypic variance that is genetic:

$$
H^2 = \frac{\sigma^2_\textrm{G}}{\sigma^2_\textrm{P}}
$$

This is also called *broad-sense heritability*. Another kind of heritability, *narrow-sense heritability*, is defined as the proportion of the phenotypic variance that is explained by additive genetic factors (i.e., ignoring dominance and epistasis):

$$
h^2 = \frac{\sigma^2_\textrm{A}}{\sigma^2_\textrm{P}}
$$

It turns out that for complex traits, most genetic variance is additive[<sup>2</sup>], making narrow-sense heritability a useful statistic in the modern genomics era. From here on, I refer to narrow-sense heritability as just heritability.

[<sup>2</sup>]: https://doi.org/10.1371/journal.pgen.1000008 "Hill, W. G., Goddard, G. E., & Visscher, P. M. (2008). Data and theory point to mainly additive genetic variance for complex traits. PLoS Genetics, 4(2): e1000008."

So now that we have defined heritability, how do we estimate it?

The first step towards estimating heritability using the variance-components method is to place a linear mixed-effects model on the quantitative trait. You may be familiar with linear mixed-effects models from the perspective of regression (see [here](https://ourcodingclub.github.io/2017/03/15/mixed-models.html)). If not, don’t worry — they are actually a little easier to understand in the context of heritability estimation, in my opinion.

Linear mixed-effects models assume that a dependent variable is the sum of one or more fixed effects, one or more random effects, and error:

<p>
<center>dependent variable = fixed effect(s) + random effect(s) + error</center>
</p>

Here, the dependent variable is the trait. Let $$\mathbf{y}$$ denote a 1-by-$$n$$ matrix (or vector), where $$n$$ is the number of individuals for whom we have data, and where $$y_i$$ is the trait value for the $$i$$th individual:

$$
\mathbf{y} = \begin{pmatrix} 
y_1 \\
y_2 \\
\vdots \\
y_n 
\end{pmatrix}
$$

Fixed effects are covariates whose values per individual are known. These values are stored in an $$m$$-by-$$n$$ design matrix, where $$m$$ is the number of covariates, denoted by $$\mathbf{X}$$:

$$
\mathbf{X} = \begin{pmatrix} 
1 & x_{12} & \cdots & x_{1m} \\
1 & x_{22} & \cdots & x_{2m} \\
\vdots & \vdots & \ddots & \vdots \\
1 & x_{n2} & \cdots & x_{nm}
\end{pmatrix}
$$

Notice that the values in the first column are all 1, meaning that the first covariate is always an intercept. Other covariates are usually environmental factors influencing the trait, such as age, sex, and so on. Each covariate in $$\mathbf{X}$$, including the intercept, has a corresponding coefficient in the vector $$\beta$$:

$$
\beta = \begin{pmatrix} 
\beta_1 \\
\beta_2 \\
\vdots \\
\beta_m 
\end{pmatrix}
$$

The coefficients within $$\beta$$ are free parameters in the model. To obtain a combined prediction of all the fixed effects, $$\mathbf{X}$$ and $$\beta$$ are matrix multiplied:

$$
\mathbf{X}\beta = \begin{pmatrix} 
1 & x_{12} & \cdots & x_{1m} \\
1 & x_{22} & \cdots & x_{2m} \\
\vdots & \vdots & \ddots & \vdots \\
1 & x_{n2} & \cdots & x_{nm}
\end{pmatrix} \begin{pmatrix} 
\beta_1 \\
\beta_2 \\
\vdots \\
\beta_m 
\end{pmatrix} = \begin{pmatrix} 
1\beta_1 + x_{12}\beta_2 + \cdots + x_{1m}\beta_m\\
1\beta_1 + x_{22}\beta_2 + \cdots + x_{2m}\beta_m \\
\vdots \\
1\beta_1 + x_{n2}\beta_2 + \cdots + x_{nm}\beta_m 
\end{pmatrix}
$$

Like fixed effects, random effects are found by matrix multiplying a design matrix $$\mathbf{Z}$$ and a vector $$\mathbf{u}$$. The critical difference is that the values within $$\mathbf{u}$$ are not free parameters but rather the whole vector is considered to be random. We’ll get back to random effects a little later on.

The final term is the error, denoted by $$\epsilon$$, which is a random vector of length $$n$$. We consider it to have a univariate random normal distribution with zero mean:

$$
\epsilon \sim \mathrm{Normal}\left(0, \sigma^2_\epsilon\right)
$$

The above can also be written as a multivariate random normal distribution as follows:

$$
\epsilon \sim \mathrm{MvNormal}\left(0, \mathbf{I}\sigma^2_\epsilon\right)
$$

Where $$\mathbf{I}$$ is an $$n$$-by-$$n$$ identity matrix. Earlier we equated environmental variance with residual error. Therefore we can replace $$\sigma^2_\epsilon$$ with $$\sigma^2_\mathrm{E}$$:

$$
\epsilon \sim \mathrm{MvNormal}\left(0, \mathbf{I}\sigma^2_\mathrm{E}\right)
$$

Why we would want to write it this way will become clear later.

Putting all of this together, we get:

$$
\mathbf{y} = \mathbf{X}\beta + \mathbf{Z}\mathbf{u} + \epsilon
$$

This is the linear mixed-effects model in its general form. This form can accept any number of fixed or random effects, but here we are only interested in one random effect in particular, namely the additive effect of genetics. Therefore, the vector $$$\mathbf{u}$$ is of length $$n$$ and contains what are sometimes called *breeding values*. An individual’s breeding value represents what the value of the trait would be if it was 100% heritable and not influenced by any fixed effects, dominance, or epistasis:

$$
\mathbf{u} = \begin{pmatrix} 
u_1 \\
u_2 \\
\vdots \\
u_n 
\end{pmatrix}
$$

We consider $$\mathbf{u}$$ to be a random vector with multivariate random normal distribution:

$$
\mathbf{u} \sim \mathrm{MvNormal}\left(0, \mathbf{A}\sigma^2_\mathrm{A}\right)
$$

$$\mathbf{A}$$ is an $$n$$-by-$$n$$ matrix which summarises the genetic similarities between all individuals in the sample. This must be known prior to setting up the model. It can be generated in various ways. For a family study, often $$\mathbf{A}=2\Phi$$, where $$\Phi$$ is the *kinship matrix* constructed using pedigree information as described [here](https://brainder.org/2015/06/13/genetic-resemblance-between-relatives/). Alternatively, if there are genetic data from the individuals, an empirical genetic similarity/relatedness/kinship matrix can be generated using various software packages, including GCTA[<sup>3</sup>], LDAK[<sup>4</sup>], or IBDLD[<sup>5</sup>]. From my limited experience of reading these papers and using empirical matrices, it seems like IBDLD may be the best current choice.

[<sup>3</sup>]: http://doi.org/10.1016/j.ajhg.2010.11.011 "Yang, J., Lee, S. H., Goddard, M. E., & Visscher, P. M. (2011). GCTA: A tool for genome-wide complex trait analysis. American Journal of Human Genetics, 88(1), 76–82."

[<sup>4</sup>]: http://doi.org/10.1016/j.ajhg.2012.10.010 "Speed, D., Hemani, G., Johnson, M. R., & Balding, D. J. (2012). Improved heritability estimation from genome-wide SNPs. American Journal of Human Genetics, 91(6), 1011–1021."

[<sup>5</sup>]:http://doi.org/10.1002/gepi.20606 "Han, L., & Abney, M. (2011). Identity by descent estimation with dense genome-wide genotype data. Genetic Epidemiology, 35(6), 557–567."

Since $$\mathbf{u}$$ is of length $$n$$ and each individual contributes one data point to $$\mathbf{y}$$, $$\mathbf{Z}$$ must be an $$n$$-by-$$n$$ identity matrix, and therefore can be ignored. Now we have a simpler equation for the model:

$$
\mathbf{y} = \mathbf{X}\beta + \mathbf{u} + \epsilon
$$

where

$$
\mathbf{u} \sim \mathrm{MvNormal}\left(0, \mathbf{A}\sigma^2_\mathrm{A}\right)\\
\epsilon \sim \mathrm{MvNormal}\left(0, \mathbf{I}\sigma^2_\mathrm{E}\right)
$$

Bayesians amongst you might prefer the more compact form, as I do:

$$
\mathbf{y} \sim \mathrm{MvNormal}\left(\mathbf{X}\beta, \mathbf{A}\sigma^2_\mathrm{A} + \mathbf{I}\sigma^2_\mathrm{E}\right)
$$

And that’s it! In a future post, I will describe how to fit this model to data.