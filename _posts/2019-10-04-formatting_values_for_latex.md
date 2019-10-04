---
layout: post
title: Formatting floating-point numbers for LaTeX
date: 2019-10-04
has_code: true
has_comments: true
---
The following Python function converts a float to a LaTeX-friendly string, which is
formatted to three significant digits and presents very large or small values in
standard notation.

```python
{{ site.data.code.fmt_val_latex__py }}
```

This is probably not the best way to do it. I'm sure there is a much more elegant
pure-regex solution rand I haven't tested it exhaustively with different values of `p`.
But it seems to do the job.