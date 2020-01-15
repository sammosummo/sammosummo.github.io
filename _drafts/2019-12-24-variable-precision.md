---
layout: post
title: Fitting a variable-precision estimation model
date: 2019-12-22
has_code: true
has_comments: true
has_math: true
tags:
 - Python
 - vision
 - psychophysics
include_references: true
references:
 - 
---
Studies of visual short-term memory (VSTM, commonly called *visual working memory* in the literature, but I dislike
this term) often employ
*delayed-estimation tasks*. A trial in a typical delayed-estimation task goes like this. First, the observer sees an
array of colored squares. The array is removed, then after a delay, a location is probed. The observer selects the color
from the probed location using a color wheel. The idea behind delayed-estimation tasks is to measure the precision with
which the observer reproduces the probed color. Data from many trials are usually modeled using some variation of Von
Mises distribution with a concentration parameter that reflects the observer's precision.

In a famous study, [Zhang and Luck (2007) ](#Zhang2007a) used delayed-estimation tasks to provide evidence for the
*item-based view* of visual short-term memory. This view says that argue that observers remember
up to about four items from the array with essentially fixed precision