---
layout: page
title: Writing
---

Posts are uncategorized and ordered by when they were originally posted. I haven't figured
out how to create separate lists for different categories. 🤷‍

Please be aware that none of the following was peer reviewed and therefore could contain
nonsense!

<ul>
{% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date: '%B %d, %Y'}})
    </li>
{% endfor %}
</ul>
