---
date: 2020-06-25
has_code: true
has_comments: true
layout: post
short_title: Audiobooks IV
tags:
- audiobooks
- lists
title: Every audiobook review
---
{% assign num=0 %}
{% for audiobook in site.data.audiobooks %}
  {% assign num=num | plus:1 %}
{% endfor %}

Here is another dynamic list of audiobook reviews. This time, it's all {{ num }} of them
in alphabetical order. Not much else to say, really!

{% assign audiobooks = site.data.audiobooks | sort:"sorting_key"%}
{% for book in audiobooks %}<hr>{% include audiobook.html %}{% endfor %}