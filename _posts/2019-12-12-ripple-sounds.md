---
layout: post
title: Ripple sounds
date: 2019-12-12
has_code: true
has_comments: true
has_math: true
tags:
 - Python
 - sound
 - psychophysics
include_references: true
references:
 - Kowalski1996a
 - Shamma2001a
 - Visscher2007a
 - Shapley1985a
 - Escabi2002a
 - Glasberg1990a
---

Ripple sounds are broadband stimuli with sinusoidal spectral envelopes. They were first
proposed by [Kowalski e al. (1996)](#Kowalski1996a) to measure the response properties of
neurons within the auditory system (reviewed by [Shamma, 2001](#Shamma2001a)). They are
frequently described as the auditory equivalent to visual gratings (cf. [Shapley & Lennie,
1985](#Shapley1985a)). Indeed, as we shall see shortly, plotted ripple envelopes look
exactly like gratings. Ripple sounds have also been used to study auditory short-term
memory [(Visscher et al., 2007)](#Visscher2007a).

## Mathematical definition

Ripple sounds are essentially a kind of broadband noise, but in practice it is difficult
to create noise and shape it with filters to a desired envelope because this would
require a very elaborate filter design. Instead, ripple sounds are created by
summing together many amplitude-modulated [sinusoids](pure-tones) with different
frequencies. The amplitude-modulation function controls the ripple envelope and
can be used to create ripples with different *depths*, *densities*, *velocities*, and
*initial phases*.

The symbolic definition is a bit cumbersome. First, we define a function that returns the
instantaneous pressure of a ripple sound at a given time point as

$$\begin{equation}
\mathrm{ripple}\left( t \right) = \sum_{i=1}^{n}{
s\left( i, t \right) \cdot
a\left( i, t \right) \cdot
q\left( i \right)
}
\end{equation}$$

where $$t$$ is time in s, $$i$$ indexes the sinusoid, $$n$$ is the number of sinusoids
(typically in the hundreds or thousands), and the three terms in the summation are all
functions defined below.

The first term, $$s$$, returns the waveform of an unmodulated sinusoid,

$$\begin{equation}
s\left( i, t \right) = \sin\left[2\pi{}\cdot f\left(i\right)\cdot t+\varphi\right]
\end{equation}$$

where $$f$$ is the ordinary frequency of the tone in Hz and $$\varphi$$ is the starting
phase in radians. I discussed sinusoids in detail in a [previous post](pure-tones).
Frequencies are usually spaced logarithmically over a wide range. For example, tones can
be spaced evenly along a $$\log_2$$ (i.e., musical) scale using 

$$\begin{equation}
f\left( i \right) = f_0\left(\frac{f_\left(n-1\right)}{f_0}\right)^{\frac{i}{n - 1}}
\end{equation}$$

where $$f_0$$ is the frequency of the lowest tone in Hz and $$f_\left(n-1\right)$$ is the
frequency of the highest tone in Hz. Another option is to space tones evenly in terms
of equivalent rectangular bandwidths [(Glasberg & Moore, 1990)](#Glasberg1990a). I'll
implement this in a future post. Starting phases should be random, so we draw them from a 
circular uniform distribution,

$$\begin{equation}
\varphi \sim \mathrm{Uniform}\left( 0, 2\pi \right)
\end{equation}$$

The next term, $$a$$, is the amplitude-modulation function,

$$\begin{equation}
a\left( i, t \right) = 1 + \\
\Delta\left(t\right) \cdot \sin \left\{ 2\pi \left[
w^\prime\left(t\right) + \Omega\left(t\right) \cdot x\left(i\right)
\right] + \phi \right\}
\end{equation}$$

where

$$\begin{equation}
x\left( i \right) = \log_2\left(\frac{f\left(i\right)}{f_0}\right)
\end{equation}$$

and

$$\begin{equation}
w^\prime\left( t \right) = \int_0^t w \left( \tau \right)\: \mathrm{d}\tau
\end{equation}$$

and $$\Delta$$, $$\Omega$$, and $$w$$ are potentially time-varying functions that
control ripple depth, density, and velocity, respectively, and $$\phi$$ is the ripple
starting phase.
 
The last term, $$q$$, scales the amplitude-modulated sinusoids so that the resulting sound
has a desired long-term average spectrum. For example, to ensure equal energy per octave,
as in [pink noise](https://en.wikipedia.org/wiki/Pink_noise), we can use

$$\begin{equation}
q\left(i\right)=\frac{1}{\sqrt{f\left(i\right)}}
\end{equation}$$

Alternatively, we could use $$q\left(i\right)=1$$ to ensure a flat long-term average
spectrum, like [white noise](https://en.wikipedia.org/wiki/White_noise).

(Nitpicker's note: The above definition produces ripple sounds at arbitrary overall sound
pressure levels (SPLs). To produce sounds at a desired overall SPL, the simplest solution
is to re-scale the entire waveform.)

## Examples

When $$\Delta\left( t \right) = 0$$, there is no sinusoidal variation in the envelope and
the result is just noise.

When $$\Delta\left( t \right)$$ and $$\Omega\left( t \right)$$ are constant, non-zero
values and $$w\left( t \right) = 0$$, "stationary"
ripple sounds are created. These sounds have sinusoidal spectral envelopes, but their
envelopes do not change over time.

![](/assets/images/static-ripples.svg)
*Envelopes of three stationary ripple sounds. Brighter areas have more energy. The middle
sound has a higher ripple density ($$\Omega$$) than the leftmost sound, and the rightmost
sound has a shallower ripple depth ($$\Delta$$).*

Setting $$\Delta\left( t \right)$$, $$\Omega\left( t \right)$$, and $$w\left( t \right)$$
to constant, non-zero values creates "moving" ripple sounds. These are the most common
kind of ripple sound found in the literature [(Shamma, 2001)](#Shamma2001a).

![](/assets/images/moving-ripples.svg)
*Envelopes of moving ripple sounds. The middle
sound has a greater ripple drift ($$w$$) than the leftmost sound, while the rightmost
sound has a negative drift.*

Finally, we can create "dynamic" moving ripples by defining $$\Delta\left( t \right)$$,
$$\Omega\left( t \right)$$, and $$w\left( t \right)$$ as time-varying functions [(Escabi,
2002)](#Escabi2002a).

![](/assets/images/dynamic-ripples.svg)
*Envelopes of dynamic moving ripple sounds. In each example, one of
$$\Delta\left( t \right)$$ (leftmost),
$$\Omega\left( t \right)$$ (middle), and $$w\left( t \right)$$ (rightmost) was defined as
a spline between multiple different values, creating a smooth walk.*

## Python code

Below is some Python code that creates and plays all of the examples from above. It can
also produce the envelope figures, but this takes a really long time, so you might want to
comment out those lines or reduce the value of $$n$$ (in the script, this is `n` inside
`main()`).

```python
{{ site.data.code.ripple-sounds__py }}
```

