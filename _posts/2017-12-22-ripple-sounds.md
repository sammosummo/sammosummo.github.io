---
layout: post
title: Ripple sounds
date: 2017-12-22
categories:
 - Sound
description:
image: https://sammosummo.github.io/images/kanagawa-1831.jpg
image-sm: https://sammosummo.github.io/images/kanagawa-1831-sm.jpg
image-description: "The Great Wave off Kanagawa (1831) by Katsushika Hokusai"

---

Ripples are synthetic sounds with sinusoidal spectral or spectro-temporal profiles. Here, I provide a conceptual description of ripples and some code for generating them.

**(Disclaimer: This is a re-post. The code below uses the `brian` Python package, which has been recently superseded by `brian2`; see [here](http://briansimulator.org).)**

Ripples are commonly used to measure the response properties of neurons in the auditory system, and are frequently compared with visual gratings[<sup>1</sup>]. They have also been used to study auditory short-term memory [<sup>2</sup>].

To create a ripple, we first need to create a mixture of many sinusoids whose frequencies are spaced evenly along a logarithmic frequency axis. Each sinusoid should also have a random starting phase, and their amplitudes should be modified so that the resulting sound has approximately equal power-spectrum density per octave. We’ll also randomise the amplitude of each sinusoid. Symbolically,

$$
y\left(t\right) = \sum_{i=1}^{N}{s_i\left(t\right)}\\
s_i\left(t\right) = \gamma_i\cdot\frac{1}{\sqrt{f_i}}\sin{\left(2\pif_it+\phi_i\right)}\\
f_i = f_1\left(\frac{f_N}{f_1}\right)^\frac{i-1}{N-1}\\
\gamma_i\sim\mathrm{Uniform}\left(0,1\right)\\
\phi{}_i\sim\mathrm{Uniform}\left(0,2\pi{}\right)\\
f_1 = 250\\
f_N = 8000\\
N = 1000
$$

These equations work as follows. The first equation sums together $$N$$ sinusoids. The second equation generates each sinusoid, and scales and randomises their amplitudes. The third equation determines the frequency of the sinusoids in Hz, and ensures that they are evenly spaced on a musical (log2) scale between 250 Hz and 8 KHz. The random variable $$\gamma_i$$ is the amplitude randomisation applied to the $$i$$th tone; this is not strictly necessary, so $$\gamma_i$$ could be set to 1. The second random variable $$\phi_i$$ represents the phase of the $$i$$th tone in radians. The python snippet below implements this process: