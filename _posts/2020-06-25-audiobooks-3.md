---
date: 2020-06-25
has_code: true
has_comments: true
layout: post
short_title: Audiobooks III
tags:
- books
title: My bottom 10 audiobooks
---

Here is a list my least favorite audiobooks so far. If you are
interested in how I created this list, check out my [earlier post](audiobooks).

{% assign audiobooks = site.data.audiobooks | sort:"overall_score" %}
{% for book in audiobooks limit:10 %}<hr>{% include audiobook.html %}{% endfor %}