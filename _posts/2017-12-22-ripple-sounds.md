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

Ripples are synthetic sounds with sinusoidal spectral or spectro-temporal profiles. Here, I provide a conceptual description of ripples and some code to generate them.

**(Disclaimer: This is a re-post. The code below uses the `brian` Python package, which has been recently superseded by `brian2`; see [here](http://briansimulator.org).)**

Ripples are commonly used to measure the response properties of neurons in the auditory system, and are frequently compared with visual gratings[<sup>1</sup>]. They have also been used to study auditory short-term memory [<sup>2</sup>].

To create a ripple, we first need to create a mixture of many sinusoids whose frequencies are spaced evenly along a logarithmic frequency axis. Each sinusoid should also have a random starting phase, and their amplitudes should be modified so that the resulting sound has approximately equal power-spectrum density per octave. We’ll also randomise the amplitude of each sinusoid. The resulting sound can be expressed in terms of the time-varying function, $$y\left(t\right)$$, defined by the following set of equations:

$$\begin{eqnarray} &amp;y\left(t\right) &amp;=&amp; \sum_{i=1}^{N}{s_i\left(t\right)}, \\ \textrm{where}&amp; \nonumber \\ &amp;s_i\left(t\right) &amp;=&amp; \gamma_i\cdot\frac{1}{\sqrt{f_i}}\cdot{}\sin{\left(2\pi\cdot{}f_i\cdot{}t+\phi_i\right)}, \\ &amp;f_i &amp;=&amp; f_1\cdot{}\left(\frac{f_N}{f_1}\right)^\frac{i-1}{N-1}, \\ &amp;\gamma_i&amp;\sim&amp;\mathcal{U}\left(0,1\right), \nonumber \\ &amp;\phi{}_i&amp;\sim&amp;\mathcal{U}\left(0,2\pi{}\right), \nonumber \\ &amp;f_1 &amp;=&amp; 250, \nonumber \\ &amp;f_N &amp;=&amp; 8000, \nonumber \\ \textrm{and}&amp; \nonumber \\ &amp;N &amp;=&amp; 1000. \nonumber \end{eqnarray}$$
