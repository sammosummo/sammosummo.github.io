---
date: 2020-06-25
has_code: true
has_comments: true
layout: post
short_title: Audiobooks III
tags:
- audiobooks
- lists
title: 'The dregs: My least favorite audiobooks'
---
Here is a dynamic list my least favorite audiobooks so far. I'm not sure why anyone would
want to see this, but it was easy to generate, so why not. As you might expect, it was
created in much the same way as my previous list of [favorite audiobooks](audiobooks-2).
Ranking is based on average of book and performance score in ascending order, meaning that
number 1 is the worst.

Enjoy, I suppose 🤷
{% assign counter=0 %}
{% assign audiobooks = site.data.audiobooks | sort:"overall_score" %}
{% for book in audiobooks limit:20 %}<hr>
  {% assign counter=counter | plus:1 %}
  {% include audiobook.html %}
{% endfor %}