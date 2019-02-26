---
layout: page
title: Writing
---

Posts are ordered by when they were originally posted, not last edited. I haven't figured
out how to do that. <g-emoji class="g-emoji" alias="man_shrugging" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f937-2642.png">🤷‍♂️</g-emoji>

<ul>
{% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date: '%B %d, %Y'}})
    </li>
{% endfor %}
</ul>
