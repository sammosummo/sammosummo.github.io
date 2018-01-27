---
layout: post
title: DDM figure
date: 2018-01-23
categories:
 - Decision making
description:
image: https://sammosummo.github.io/images/the-rec-center-2017.jpg
image-sm: https://sammosummo.github.io/images/the-rec-center-2017-sm.jpg
image-description: "The Rec Center (2017) by Aron Wiesenfeld"

---
Here is a small python snippet to create a simple figure illustrating the drift-diffusion model. I’ve been using some variation of this code in a couple of recent papers, so I thought I’d share it.

It produces something along these lines:

![](https://sammosummo.github.io/images/ddm.png){:width=10px}

A nice feature of the code is that it takes real values of drift rate, threshold, etc., so you have the option to plot several parameter configurations and compare them visually. Another feature is that the traces in the central panel get coloured depending on whether they cross the an upper or lower boundary. Enjoy!

<script src="https://gist.github.com/sammosummo/dbc28e35cc40bd7f9e020f6920a43142.js"></script>
