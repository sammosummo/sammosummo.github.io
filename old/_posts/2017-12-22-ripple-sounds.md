---
layout: post
title: Ripple sounds
date: 2017-12-22
categories:
 - Sound
description:
image: https://sammosummo.github.io/images/lake-george-1857.jpg
image-sm: https://sammosummo.github.io/images/lake-george-1857-sm.jpg
image-description: "Lake George (1857) by John William Casilear"

---

Ripples are synthetic sounds with sinusoidal spectral or spectro-temporal profiles. Here, I provide a conceptual description of ripples and some code for generating them.

**(Disclaimer: This is a re-post. The code below uses the `brian` Python package, which has been recently superseded by `brian2`; see [here](http://briansimulator.org).)**

Ripples are commonly used to measure the response properties of neurons in the auditory system, and are frequently compared with visual gratings[<sup>1</sup>]. They have also been used to study auditory short-term memory [<sup>2</sup>].

[<sup>1</sup>]: https://doi.org/10.1016/S1364-6613(00)01704-6 "Shamma, S. (2001). On the role of space and time in auditory processing. Trends in Cognitive Sciences, 5(8), 340–348."

[<sup>2</sup>]: https://doi.org/10.1371/journal.pbio.0050056 "Visscher, K. M., Kaplan, E., Kahana, M. J., & Sekuler, R. (2007). Auditory short-term memory behaves like visual short-term memory. PLoS Biology, 5(3), e56."


To create a ripple, we first need to create a mixture of many sinusoids whose frequencies are spaced evenly along a logarithmic frequency axis. Each sinusoid should also have a random starting phase, and their amplitudes should be modified so that the resulting sound has approximately equal power-spectrum density per octave. We’ll also randomise the amplitude of each sinusoid. Symbolically,

$$
y\left(t\right) = \sum_{i=1}^{N}{s_i\left(t\right)}\\
s_i\left(t\right) = \gamma_i\frac{1}{\sqrt{f_i}}\sin{\left(2\pi{}f_it+\phi_i\right)}\\
f_i = f_1\left(\frac{f_N}{f_1}\right)^\frac{i-1}{N-1}\\
\gamma_i\sim\mathrm{Uniform}\left(0,1\right)\\
\phi{}_i\sim\mathrm{Uniform}\left(0,2\pi{}\right)\\
f_1 = 250\\
f_N = 8000\\
N = 1000
$$

These equations work as follows. The first equation sums together $$N$$ sinusoids. The second equation generates each sinusoid, and scales and randomises their amplitudes. The third equation determines the frequency of the sinusoids in Hz, and ensures that they are evenly spaced on a musical (log2) scale between 250 Hz and 8 KHz. The random variable $$\gamma_i$$ is the amplitude randomisation applied to the $$i$$th tone; this is not strictly necessary, so $$\gamma_i$$ could be set to 1. The second random variable $$\phi_i$$ represents the phase of the $$i$$th tone in radians. The python snippet below implements this process:

~~~ python
import numpy as np
from scipy.stats import uniform

duration = 1.  # in seconds
fs = 44100.  # in Hz

ntones = 1000.
fmin = 250.
fmax = 8000
t = np.linspace(0, duration, duration * fs)
i = np.arange(ntones) + 1
f = fmin * (fmax / fmin)**((i - 1)/(ntones - 1))
gamma = uniform.rvs(0, 1, size=ntones)
phi = uniform.rvs(0, 2 * np.pi, size=ntones)

# turn all vectors into matrices, could take a few seconds ...
T = np.tile(t, (ntones, 1))
F = np.tile(f, (t.size, 1)).T
Gamma = np.tile(gamma, (t.size, 1)).T
Phi = np.tile(phi, (t.size, 1)).T

Y = Gamma * np.sin(2 * np.pi * F * T + Phi) / np.sqrt(F)
y = np.sum(Y, axis=0)
~~~

Click to hear it: <audio controls="controls"><source type="audio/wav" src="https://sammosummo.github.io/sounds/ripple_1.wav"></source><p>Your browser does not support the audio element.</p></audio>

All we have done so far is create pink noise, albeit via a rather circuitous method. The spectrogram of the stimulus looks like this:

![](https://sammosummo.github.io/images/ripple_1_specgram.png)

Notice the lack of any interesting spectral or spectro-temporal features. To add a sinusoidal spectral ripple to the sound, we replace the first equation with

$$
y\left(t\right)=\sum_{i=1}^{N}{a_is_i\left(t\right)}\\
a_i = 1 + d\sin\left(2\pi{}\Omega{}x_i + \varphi\right)\\
x_i = \log_2\left(\frac{f_i}{f_0}\right)
$$

which multiplies each sinusoid by an amplitude-modulation function before summing them. There three new parameters: $$d$$ represents the ripple depth — this is set to 1 or 0.9 in most studies; $$\Omega$$ represents the ripple density in cycles per octave; and $$\varphi$$ represents the starting phase of the ripple in radians. The output of the function can be visualised easily:

![](https://sammosummo.github.io/images/ripple_2_env.png)

Some code to create a spectral ripple in python:

~~~python
import numpy as np
from scipy.stats import uniform

duration = 1.
fs = 44100.

ntones = 1000.
fmin = 250.
fmax = 8000
t = np.linspace(0, duration, duration * fs)
i = np.arange(ntones) + 1
f = fmin * (fmax / fmin)**((i - 1)/(ntones - 1))
gamma = uniform.rvs(0, 1, size=ntones)
phi = uniform.rvs(0, 2 * np.pi, size=ntones)

T = np.tile(t, (ntones, 1))
F = np.tile(f, (t.size, 1)).T
Gamma = np.tile(gamma, (t.size, 1)).T
Phi = np.tile(phi, (t.size, 1)).T

d = 1.
omega = 0.5
ripple_phi = 0.
X = np.log2(F / fmin)
A = 1 + d*np.sin(2 * np.pi * omega * X + ripple_phi)

S = Gamma * np.sin(2 * np.pi * F * T + Phi) / np.sqrt(F)
Y = A * S
y = np.sum(Y, axis=0)
~~~

Click to hear it: <audio controls="controls"><source type="audio/wav" src="https://sammosummo.github.io/sounds/ripple_2.wav"></source><p>Your browser does not support the audio element.</p></audio>

We can see the spectral ripple in the new sound's spectrogram (though due to the linear vertical axis, it is not as clear as in the previous figure):

![](https://sammosummo.github.io/images/ripple_2_specgram.png)

Now we have succeeded in creating a stationary ripple. However, single-unit recording studies have shown that neurons respond selectively to sounds with specific ripple densities <em>and</em> phases[<sup>1</sup>]. Studies of auditory physiology have often used moving ripple sounds, where the instantaneous phase of the ripple changes over time. We can achieve this by replacing the amplitude-modulation function with a time-varying function:

$$y\left(t\right) = \sum_{i=1}^{N}{a_i\left(t\right)s_i\left(t\right)}\\
a_i\left(t\right) = 1 + d\sin\left[2\pi{}\left(wt+\Omega{}x_i\right) + \varphi\right]
$$

This modification adds a ‘drift’ to the amplitude-modulation function corresponding to $$w$$ in Hz:

![](https://sammosummo.github.io/images/ripple_3_env.png)

It also adds a striking new perceptual feature to the sound: <audio controls="controls"><source type="audio/wav" src="https://sammosummo.github.io/sounds/ripple_3.wav"></source><p>Your browser does not support the audio element.</p></audio>

Finally, we can go one step further and create dynamic moving ripples[<sup>3</sup>]. To implement these, we need to slightly modify the equations:

[<sup>3</sup>]: https://www.ncbi.nlm.nih.gov/pubmed/12019330 "Escabi, M. E. & Schreiner, C. E. (2002). Nonlinear spectrotemporal sound analysis by neurons in the auditory midbrain. The Journal of Neuroscience, 22(10), 4114–4131."

$$a_i\left(t\right) = 1 + d\sin\left \{2\pi\left[w^\prime\left(t\right)+\Omega{}\left(t\right)x_i\right] + \varphi\right \}\\w^\prime\left(t\right) = \int_0^\tau{}w(\tau)\,\mathrm{d}\tau$$

Now $$\Omega$$ and $$w$$ are arbitrary vectors of length $$t$$, describing the instantaneous ripple density and ripple velocity of the sound, respectively.

The gist below puts everything together. Any of the sounds you heard earlier can be created by passing the appropriate arguments to the `ripple_sound()` function in this script. A featureless, noise-like sound like the first example is created by setting both $$\Omega$$ and $$w$$ to zero; a stationary ripple like the second example has a non-zero $$\Omega$$; and so on.

<script src="https://gist.github.com/sammosummo/9b0983f4f598c9f9372e0c2e8ff4c79b.js"></script>

Here is an example of a dynamic moving sound where $$\Omega$$ and $$w$$ go on independent random walks: <audio controls="controls"><source type="audio/wav" src="https://sammosummo.github.io/sounds/ripple_4.wav"></source><p>Your browser does not support the audio element.</p></audio>

![](https://sammosummo.github.io/images/ripple_4_env.png)

![](https://sammosummo.github.io/images/ripple_4_specgram.png)