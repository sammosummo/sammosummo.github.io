---
layout: post
title: Ripple sounds
date: 2019-12-10
has_code: true
has_comments: true
has_math: true
tags:
 - Python
 - sound
 - psychophysics
include_references: true
references:
 - Shamma2001a
 - Visscher2007a
---

Ripple sounds, sometimes just called *ripples*, are synthetic sounds with sinusoidal
spectral or spectrotemporal profiles. They are commonly used to measure the response
properties of neurons in the auditory system and are frequently compared with visual
gratings [(Shamma, 2001)](#Shamma2001a). They have also been used to study auditory short-
term memory [(Visscher et al., 2007)](#Visscher2007a). In this post, I provide a
conceptual description of ripple sounds and some code for generating them.

To create a ripple sound, we first need to create a mixture of many sinusoids whose
frequencies are spaced evenly along a logarithmic frequency axis. Each sinusoid should
also have a random starting phase, and their amplitudes should be modified so that the
resulting sound has approximately equal energy per octave. We’ll also randomize the
amplitude of each sinusoid. Symbolically,

$$\begin{equation}
y\left( t \right) = \sum_{i=1}^{N}{s\left( i, t \right)}
\end{equation}$$