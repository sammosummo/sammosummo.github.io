---
layout: post
title: Displaying the contents of external files in Jekyll
date: 2019-08-18
has_code: true
has_comments: true
---

The website is written in [Jekyll](https://jekyllrb.com/). I like to display code in my
posts, but copy-pasting working code directly from my scripts into [Markdown](https://daringfireball.net/projects/markdown/)
files never felt like an elegant method. For one thing, if I changed my script for whatever
reason, I also needed to go back and edit the Markdown file, which was annoying.

So I came up with the following method. First off, when I write a new script for a blog
post, I always store it within a directory called `/assets/scripts` inside the [GitHub
repository for this website](https://github.com/sammosummo/sammosummo.github.io). After
the script and the related post are both finished, but before I commit and push the
changes to the repo, I run a file called `code2yaml.py` (also within `/assets/scripts`).
This script looks like:

```python
{{ site.data.code.code2yaml__py }}
```

As the name suggests, `code2yaml.py` converts the contents of all files within
`/assets/scripts` to a [YAML](https://yaml.org/) data file called `_data/code.yaml`. As an
added bonus, it also formats any Python scripts using [black](https://black.readthedocs.io/en/stable/).
When Jekyll builds the website, all YAML data within `_data/` become accessible via
[Liquid](https://shopify.github.io/liquid/) tags, which can be wrapped inside a Markdown
code block with the appropriate language selected for syntax highlighting, like so:

{% raw %}
~~~
```python
{{ site.data.code.code2yaml__py }}
```
~~~
{% endraw %}

Now I can make changes to my scripts at any time, and those changes will appear on the
related posts (so long as I don't forget to run `code2yaml.py`!).