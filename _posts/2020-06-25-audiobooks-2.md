---
date: 2020-06-25
has_code: true
has_comments: true
layout: post
short_title: Audiobooks II
tags:
- books
title: My top 10 audiobooks
---

Here is a simple dynamic list my favorite audiobooks so far, in descending order of overall rating. If you are
interested in how I created this list, check out my [earlier post](audiobooks).

{% assign audiobooks = site.data.audiobooks | sort:"overall_score" | reverse %}
{% for book in audiobooks limit:10 %}<hr>{% include audiobook.html %}{% endfor %}