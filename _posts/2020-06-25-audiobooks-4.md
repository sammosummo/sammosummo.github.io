---
date: 2020-06-25
has_code: true
has_comments: true
layout: post
short_title: Audiobooks IV
tags:
- books
title: All audiobooks from best to worst
---

The title says it all. If you are
interested in how I created this list, check out my [earlier post](audiobooks).

{% assign audiobooks = site.data.audiobooks | sort:"overall_score" | reverse %}
{% for book in audiobooks %}<hr>{% include audiobook.html %}{% endfor %}