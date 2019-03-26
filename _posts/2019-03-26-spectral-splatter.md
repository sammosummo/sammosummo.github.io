---
layout: post
title: Spectral splatter
date: 2019-03-26
has_code: true
---

So far in this series, we’ve generated and played pure tones using Python.  If you’ve been following along, you might have noticed little clicks at the beginnings and/or ends of these tones, particularly if you set your computer volume rather high.

One likely reason for hearing onset/offset clicks is _spectral splatter_. There is a [wikipedia article](https://en.wikipedia.org/wiki/Spectral_splatter) about spectral splatter. It reads,

> Spectral splatter (also called switch noise) refers to spurious emissions that result from an abrupt change in the transmitted signal, usually when transmission is started or stopped. For example, a device transmitting a sine wave produces a single peak in the frequency spectrum; however, if the device abruptly starts or stops transmitting this sine wave, it will emit noise at frequencies other than the frequency of the sine wave. This noise is known as spectral splatter.

This is a pretty succinct explanation. You can actually see splatter when you look at the _spectrogram_ of a pure tone:

![](/assets/images/splatter.svg)

Spectral splatter can be reduced by gradually _ramping_ the amplitude of the tone. A common choice of ramp shape is _raised cosine_, which looks like this:

![](/assets/images/ramps.svg)

The ramp on the left is applied to the beginning of the sound, and the ramp on the right is applied to the end. The spectrogram of the ramped tone looks like this:

![](/assets/images/nosplatter.svg)

While ramping reduces splatter, it doesn’t eliminate it completely, and the effectiveness of the ramps depends on their duration. If you listen carefully, you can clearly hear the difference between tones with, say, 10-ms and 30-ms ramps. I’m not aware of any research on this matter—although I’m sure there is some, buried away in back issues of _The Journal of the Acoustical Society of America_—but in my experience, 25-ms ramps work well.

If you hear clicks even with sufficiently long ramps, or in the middle of a tone, it could be a buffering issue. Examples of buffering issues include delivering sounds to the audio output before it is ready to receive them, closing the connection to the audio output before the sound is finished, or delivering more than one sound to the audio output at once. Commonly such issues can be resolved by _padding_, or adding a few ms of silence to the beginning or end of the sound waveform. Padding can occasionally present issues in circumstances where timing is critical, such as in a psychological experiment, but most of the time it’s ok pad a little.

Clicks and other noticeable imperfections in sound playback can occur for any number of system-specific reasons and it is impossible to list them all here. However, in my experience, some combination or ramping and padding fixes most issues.