---
layout: post
title: Drift-diffusion model plots
date: 2020-01-15
has_code: true
has_comments: true
has_math: false
tags:
 - Python
 - psychophysics
 - reaction-times
include_references: true
references:
 - Ratcliff2016a
 - Wiecki2013a
 - Mathias2016a
 - Mathias2017a
 - Wagenmakers2009a
 - Wiecki2013a
---

The drift-diffusion model (DDM), sometimes simply called the diffusion model, is one of
the most popular models of decision making in psychology and cognitive neuroscience (for
a fairly recent review, see [Ratcliff et al., 2016](#Ratcliff2016a)). The DDM is usually
applied to experiments that require subjects to quickly choose between two response
alternatives on each trial. The model is able to predict the proportions of responses
and the distributions of their associated reaction times (RTs).

DDM papers often contain figures similar the one below. Some time ago, I needed to make
several such "DDM plots" for one of my own papers (Fig. 1 in
[Mathias et al., 2017](#Mathias2016a)), so I wrote a Python script to automate the
process. This script (with some minor modifications and extra comments) is presented at
the end of this post.

![](/assets/images/ddm-fig.svg)
*A barebones DDM plot. The plot is divided into the three panels. The top panel shows
a kernel density estimate (KDE) of the degenerate distribution of RTs associated with one
of the response options. These are actual trials simulated from a given set of DDM
parameters via the HDDM package [(Wiecki et al., 2013)](#Wiecki2013a). The middle panel
illustrates the paths of the decision variable on two trials. The lower panel is the
degenerate distribution of RTs associated with the other response options.*

The first thing the script does is simulate a bunch of trials under the DDM for a given
set of parameters. This is done using [HDDM](http://ski.clps.brown.edu/hddm_docs/), a Python package for fitting DDMs using
Bayesian hierarchical inference [(Wiecki et al., 2013)](#Wiecki2013a). HDDM is slightly
tricky to install these days. However, if you are interested in making DDM plots in
Python, there is a good chance you're already using or want to use HDDM. For this post, I
installed HDDM into a new conda environment using the following commands:

```bash
conda create --name py36 python=3.6
conda activate py36
conda install conda-build
conda install pymc3
conda install pandas patsy matplotlib scipy tqdm
pip install cython
pip install hddm
```

Thanks to [Esin Turkakin](https://groups.google.com/forum/#!topic/hddm-users/bdQXewfUzLs)
for posting this solution to the HDDM mailing list!

If you are interested in learning more about the DDM, you may wish to read a mini-review
I wrote on the topic for a psychoacoustics audience [(Mathias, 2016)](#Mathias2016b).
Or for a thorough review, see [Wagenmakers (2009)](#Wagenmakers2009a]).

Here is the code:

```python
{{ site.data.code.ddm-fig__py }}
```

