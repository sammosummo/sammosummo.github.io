---
layout: post
title: Partially filled histograms in Matplotlib
date: 2019-10-03
has_code: true
has_comments: true
tags:
 - figures
 - Python
 - matplotlib
---
Here is a recipe for plotting a histogram with its bars partially filled and partially
transparent. I used this in a manuscript to show the distribution of posterior samples
from a Bayesian model, and to highlight its 95% credible interval. Enjoy!

```python
{{ site.data.code.phist__py }}
```

![](/assets/images/phist.svg)
*Partially filled histogram.*