---
layout: post
title: Formatting floating-point numbers for LaTeX
date: 2019-10-04
has_code: true
has_comments: true
tags:
 - LaTeX
---
The following Python function converts a float to a LaTeX-friendly string formatted
to three significant digits and with very large or small values in presented in
standard notation.

```python
{{ site.data.code.fmt_val_latex__py }}
```

This is probably not the best way to do it. I'm sure there is a much more elegant
regex-only solution. I haven't tested it exhaustively with different values of `p`.
But it seems to do the job.