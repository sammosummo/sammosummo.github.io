---
layout: post
title: Iterated rippled noise
date: 2017-11-21
categories:
 - Sound
description:
image: https://sammosummo.github.io/images/kanagawa-1831.jpg
image-sm: https://sammosummo.github.io/images/kanagawa-1831-sm.jpg
image-description: "The Great Wave off Kanagawa (1831) by Katsushika Hokusai"

---
Iterated rippled noise (IRN) is one of the more popular stimuli in the psychoacoustics literature. In this post, I describe IRN and provide some code for generating it.

In its basic form, IRN is generated in the time domain using broadband noise which is delayed and added back to itself repeatedly. This creates something that sounds like a ‘cracked bassoon’ (according to some authors[<sup>1</sup>]) with a flat noisy pitch at $$\frac{1}{d}$$ Hz, where $$d$$ is the delay interval in seconds. The strength of the pitch depends on the number of delay-and-add iterations, $$n$$. The original formulation by Yost[<sup>2</sup>] also multiplied the delayed waveform by a gain factor $$g$$ prior to adding, but this is normally just set to 1 in most studies. This process is represented mathematically by:

[<sup>1</sup>]: https://doi.org/10.1038/1637 "Griffiths, T.D., Buchel, C., Frackowiak, R.S.J., & Patterson, R.D. (1998). Analysis of temporal structure in sound by the human brain. Nature Neuroscience, 1, 422–427."

[<sup>2</sup>]: https://www.ncbi.nlm.nih.gov/pubmed/8675844 "Yost, W.A. (1996). Pitch of iterated rippled noise. Journal of the Acoustical Society of America, 100(1), 511–518."

$$\begin{eqnarray}y_i\left(t\right)&=&y_{i-1}\left(t\right)+g\cdot{}y_{i-1}\left(t-d\right);\mbox{ for }i=1,2,\ldots{}n\\y_0\left(t\right)&=&x\left(t\right),\mbox{ the input signal.}\end{eqnarray}$$

One could also delay and add the original waveform (IRNO) rather than the same waveform (IRNS) back to itself each time; this would just require changing $$y_{i-1}\left(t\right)$$ to $$y_{0}\left(t\right)$$ above. Below is an IRNS stimulus with constant <em>d</em> and <em>g</em>, but increasing <em>n</em> from 0 (i.e., just plain white noise) to 64. You should hear a pitch at 200 Hz gradually emerge.

<center>
<audio controls="controls">
  <source type="audio/wav" src="https://sammosummo.github.io/sounds/IRN_increasing_n.wav"></source>
  <p>Your browser does not support the audio element.</p>
</audio>
</center>

One can also create IRN with a dynamic pitch contour by changing $$d$$ from a constant to a time-varying function[<sup>3</sup>] [<sup>4</sup>], as in the example below. You should hear an upward-sweeping pitch:

[<sup>3</sup>]: https://doi.org/10.1016/j.biosystems.2004.09.008 "Denham, S. (2005). Pitch detection of dynamic iterated rippled noise by humans and a modified auditory model. Biosystems, 79(1–3), 199–206."

[<sup>4</sup>]: https://doi.org/10.1109/TBME.2007.896592 "Swaminathan, J., Krishnan, A., Gandour, J.T., & Xu, Y. (2008). Applications of static and dynamic iterated rippled noise to evaluate pitch encoding in the human auditory brainstem. IEEE Transactions on Biomedical Engineering, 55(1), 281–287."