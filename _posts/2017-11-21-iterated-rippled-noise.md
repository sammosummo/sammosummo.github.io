---
layout: post
title: Iterated rippled noise
date: 2017-11-21
categories:
 - Sound
description:
image: https://sammosummo.github.io/images/netsuke.jpg
image-sm: https://sammosummo.github.io/images/netsuke-sm.jpg
image-description: "Netsuke at the Metropolitan Museum of Art"

---
Iterated rippled noise (IRN) is one of the more popular stimuli in the psychoacoustics literature. In this post, I describe IRN and provide some code for generating it.

**(Disclaimer: Some of what appears below was taken from an earlier post on my previous blog.)**


In its basic form, IRN is generated in the time domain using broadband noise which is delayed and added back to itself repeatedly. This creates something that sounds like a ‘cracked bassoon’ (according to some authors) with a flat noisy pitch at $$\frac{1}{d}$$ Hz, where $$d$$ is the delay interval in seconds. The strength of the pitch depends on the number of delay-and-add iterations, $$n$$. The original formulation by Yost also multiplied the delayed waveform by a gain factor $$g$$ prior to adding, but this is normally just set to 1 in most studies. This process is represented mathematically by:

$$
y_i\left(t\right)&=&y_{i-1}\left(t\right)+g\cdot{}y_{i-1}\left(t-d\right);\mbox{ for }i=1,2,\ldots{}n.\nonumber\\y_0\left(t\right)&=&x\left(t\right),\mbox{ the input signal.}
$$
