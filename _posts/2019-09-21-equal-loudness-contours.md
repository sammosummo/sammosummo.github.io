---
layout: post
title: Equal-loudness contours
date: 2019-09-21
has_code: true
has_comments: true
---
Two tones with different frequencies presented at the same sound pressure level (SPL) may
not sound equally loud. *Equal-loudness contours* represent these variations in perceived
loudness across frequencies for an average person. The basis of the equal-loudness contour
is the *phon*, a unit of loudness that represents the dB SPL necessary for a tone to
elicit the same loudness as a 1000-Hz reference tone. For example, if a given tone is
perceived to be as loud as a 60-dB tone at 1000 Hz, it has a loudness of 60 phon.
Equal-loudness contours are defined by [standard 226 of the International Organization for
Standardization (ISO)](https://www.iso.org/standard/34222.html).

Below is a Python script that provides the frequencies and SPLs associated with a given
phon value according to this standard, and plots the contours for phons between 0 and 90.

```python
{{ site.data.code.equal-loudness__py }}
```

![](/assets/images/equal-loudness-contours.svg)
*Equal-loudness contours in 10-phon steps in the range 0–100 phon.*

It is worth pointing out that numerous factors influence the loudness of a tone besides
frequency and level that are not accounted for by ISO 226. For example, longer sounds
generally sound louder than shorter ones, and the standard contours are valid only for
"side-presented" sounds (i.e., via headphones). Note also that ISO 226 is only valid for
a certain range of frequencies and SPLs.