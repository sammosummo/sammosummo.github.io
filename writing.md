---
layout: page
title: Writing
---

{% assign counter=0 %}
{% for post in site.posts %}
  {% assign counter = counter | plus:1 %}
{% endfor %}

Below is a list of posts sorted by when they were originally posted. To see them organized into topic instead, <a href="/tags">click here</a>.
I tend to review and edit posts occasionally, but I haven't figured out how to sort them this way. 🤷‍
<ul>
{% for post in site.posts %}
    <li>
      {% include post.html %}
    </li>
{% endfor %}
</ul>


