---
layout: post
title: Pure tones
date: 2019-03-22
has_math: true
has_code: true
has_comments: true
tags:
 - Python
 - sound
 - psychophysics
revisions:
 - date: 2019-03-27
   reason: Added links
 - date: 2019-03-28
   reason: Added figure captions
---


In my [previous post](playing-a-pure-tone-interactively), I showed you how to generate and
play a pure tone from a Python interactive session. But I didn’t explain what pure tones
are, why they are useful, or how the line of code that generated the tone actually worked.
This post fills in these gaps.


## What is a pure tone?

![](/assets/images/pure_tones_0.svg)
*A pure tone. Scaling of the axes is arbitrary.*

A pure tone is a sound whose waveform is _sinusoidal_, or like a sine wave, smoothly
cycling from positive to negative pressure and back again. They are sometimes called
_sinusoids_. Pure tones can be fully defined by four features. The first is _duration_,
normally expressed in seconds (s) or milliseconds (ms).

![](/assets/images/pure_tones_1.svg)
*Two pure tones. The tone represented by the solid orange curve has a slightly longer
duration than the tone represented by the dashed blue curve.*

The second is _frequency_, or rate of change from positive to negative pressure, normally
expressed in cycles per second (Hz).

![](/assets/images/pure_tones_2.svg)
*Two more pure tones. The green curve represents a tone with a higher frequency.*

The third is _starting phase_, or where it begins its cycle, normally expressed in radians
(rad).

![](/assets/images/pure_tones_3.svg)
*Two pure tones with different phases.*

The fourth is _level_, expressed in decibels (dB). Level is related to _amplitude_, or the
instantaneous pressure at the peaks. 

![](/assets/images/pure_tones_4.svg) 
*Two more pure tones. The purple curve represents a tone with a larger amplitude, and
therefore a higher level*

Conceptually, level is a bit more complicated than duration, frequency, and starting
phase. Firstly, it depends on several factors that don’t influence the other three
features, such as the distance and material between you and the sound source. This should
be obvious: if you stand further away from a loudspeaker, or cover your ears, any sounds
emitted from the speaker will have a lower level at your ears. Even different models of
headphones will deliver pure tones at wildly different levels, all else being equal.

A second complication is that level is relative rather than absolute. When we say a pure
tone is presented at 60 dB, we actually mean it is presented 60 dB above some reference
pressure value. The typical choice of reference pressure is 0.00002 pascals (Pa). When a
pure tone has a root mean square (RMS) pressure of 0.00002 Pa, it is said to have _sound
pressure level (SPL)_ of 0 dB. Thus, SPL is level relative to a fixed standard. Another
standardized level is _hearing level (HL)_, where 0 dB HL represents a typical person’s
_hearing threshold_, or the lowest level they can hear. A third is _sensation level (SL)_,
where 0 dB SL represents a specific person’s threshold. Because thresholds differ at
different frequencies, and everyone’s thresholds are different, the relationships between
SPL, HL, and SL are not constant across frequencies. 

It is possible to create tones whose frequencies and amplitudes change mid-waveform. Such
changes are called _frequency modulation (FM)_ and _amplitude modulation (AM)_,
respectively. Technically, FM and AM tones are not pure tones and are beyond the scope of
this post.

Pure tones are arguably the simplest sounds that exist (certainly the simplest _periodic_
sounds, anyway). This property makes them extremely important for psychoacoustics. Indeed,
some of the most fundamental discoveries of psychoacoustics were made using pure tones.
These include critical bands, equal-loudness contours, streaming, and numerous auditory
illusions.

Perhaps the commonest use of pure tones is in _audiometry_, which aims to measure a
listener’s thresholds. Pure tones at different frequencies—commonly 250, 500, 1000, 2000,
4000, and 8000 Hz—are presented _monaurally_, or one ear at a time, and the listener
indicates whether they heard them. The levels of these tones are varied across trials in
such a way as to converge upon a threshold value. Audiometry is one of many clinical tools
used diagnose hearing impairments, and to screen for normal hearing.

Provided that they are of sufficient duration and level, and their frequencies are within
certain limits, pure tones evoke the sensation of _pitch_. This means that they can be
used to create musical melodies. Such melodies typically sound quite boring because pure
tones have no real _timbre_ to speak of. The pitch of a pure tone is related to its
frequency, but frequency and pitch are not the same thing. Pitch and timbre are
complicated and fascinating phenomena. I’ll return to them in future posts.

Pure tones that are presented at a higher level tend to sound louder. However, just like
frequency and pitch aren’t the same thing, neither are level and _loudness_. Loudness is
complicated, too.

Things get very interesting (and complicated) when two or more pure tones with different
frequencies are presented at the same time. Again, this is a topic for another post.

## Mathematical definition

Let $$\mathrm{sinusoid}$$ represent the function that generates a pure tone, such that
$$\mathrm{sinusoid}\left(t\right)$$ gives the instantaneous pressure of a pure tone at
time point $$t$$ in s. The formula is

$$\begin{equation}
\mathrm{sinusoid}\left(t\right)=a\cdot\sin\left(\omega{}t+\varphi\right)
\end{equation}$$

where $$a$$ is the amplitude in Pa, $$\omega$$ is the so-called _angular frequency_ in
rad/s, and $$\varphi$$ is the starting phase in rad. Angular frequency is related to
_ordinary frequency_, denoted by $$f$$ and expressed in Hz, by

$$\begin{equation}
\omega=2\pi{}f
\end{equation}$$

We usually prefer to define pure tones in terms of SPL rather than amplitude. To convert
between these two quantities, we first need to observe that the relationship between the
amplitude and RMS pressure of a pure tone, denoted by $$p$$ and expressed in Pa, is

$$\begin{equation}
p=\frac{1}{\sqrt{2}}a
\end{equation}$$

Note that this is only true for pure tones. The relationship is different for other types
of sounds. For example, it is $$p=a$$ for square waves and $$p=\frac{1}{\sqrt{3}}a$$ for
sawtooth waves.

The SPL of a pure tone, denoted by $$l$$, is related to its RMS pressure by

$$\begin{equation}
l=20\log_{10}\left(\frac{p}{p_0}\right)
\end{equation}$$

where $$p_0$$ is the reference pressure mentioned earlier (0.00002 Pa). Now the previous
equations can be combined to yield the following

$$\begin{equation}
\mathrm{sinusoid}\left(t\right)=a_010^\frac{l}{20}\sin\left(2\pi{}ft+\varphi\right)\tag{1}\label{eq:one}
\end{equation}$$

where $$a_0$$ is the reference amplitude, $$\sqrt{8\cdot10^{-10}}$$ Pa. Notice that to
define a pure tone whose level is expressed relative to some other reference we simply
use a different value of $$a_0$$.

## Python function

In a moment, we will write a Python function that creates digital representations of pure
tones with specified durations, frequencies, phases, and levels by sampling from equation
$$\eqref{eq:one}$$ at regular time intervals. But first we need to choose a reference
amplitude and a sample rate.

It is extremely difficult to figure out at what SPL you are playing a sound over
headphones with consumer-grade electronics. Even if you knew all the specs of your
computer’s sound card and headphones, you wouldn’t know the SPL for sure unless you
measured it, and a $20 sound level meter from RadioShack won’t cut any mustard. Thus, for
the present purposes, we’ll just choose a very small value of $$a_0$$, say
$$1\cdot10^{-5}$$. We will be able to specify the level of a tone relative to a tone with
this amplitude, but not its SPL. I recommend experimenting with your volume settings and
this value until a 0-dB tone is just detectable, a 60-dB is comfortable to listen to, and
a 85-dB tone is loud, approaching uncomfortable.

The _sample rate_ is how many times per second we should sample. A sensible choice is
44100 Hz.

Now here’s the code:

```python
{{ site.data.code.pure-tones__py }}
```

## Next steps

The [next post](spectral-splatter) tackles the issue of spectral splatter, which affects
pure tones and other periodic stimuli.

