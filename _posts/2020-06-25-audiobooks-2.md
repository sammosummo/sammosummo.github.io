---
date: 2020-06-25
has_code: true
has_comments: true
layout: post
short_title: Audiobooks II
tags:
- audiobooks
- lists
title: 'Recommended listens: My favorite audiobooks so far'
---

{% assign counter=0 %}
{% for audiobook in site.data.audiobooks %}
  {% assign counter=counter | plus:1 %}
{% endfor %}

Here are my top 20 favorite audiobooks of all time (or rather since 2019, when I stared reviewing them). This list is
dynamic, meaning that it will update as I listen to and review more audiobooks. To date, I've reviewed {{ counter }} of
them. If you are interested in how I made this list, I outline the method at the [end of this post](#method).
<hr>
{% assign counter=0 %}
{% assign audiobooks = site.data.audiobooks | sort:"overall_score" | reverse %}
{% for book in audiobooks limit:20 %}
  {% assign counter=counter | plus:1 %}
  {% include audiobook.html %}<hr>
{% endfor %}

## Method

Creating this list was rather easy; it required just two lines of Liquid code. The first
line reorders the data stored in my `audiobooks.yaml` file ([see here](audiobooks#code)).
The second line loops through the first 20 entries and formats each entry using my
`audiobook.html` template.

{% raw %}
```liquid
{% assign audiobooks = site.data.audiobooks | sort:"overall_score" | reverse %}
{% for book in audiobooks limit:10 %}{% include audiobook.html %}{% endfor %}
```
{% endraw %}