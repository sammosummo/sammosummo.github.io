---
layout: page
title: Writing
---

Please be aware that none of the following was peer reviewed. Posts could contain typos, specious reasoning, or plain
old nonsense!

Tags: {% assign sorted = site.tags | sort %} {% for tag in sorted %}<a href="#{{ tag[0] }}" style="font-size: {{ tag[1] | size | times: 1 | plus: 12 }}px">🏷 {{ tag[0] }} </a>{% endfor %}

<h2><a name="chron"></a>Posts by date</h2>
<ul>
{% for post in site.posts %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date: '%B %d, %Y'}})
    </li>
{% endfor %}
</ul>

<h2><a name="chron"></a>Posts by tag</h2>
{% for tag in sorted %}
{% assign ttag = tag[0] %}
<h3><a name="{{ ttag }}"></a>{{ ttag }}</h3>
<ul>
{% for post in site.tags[ttag] %}
    <li>
        <a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date: '%B %d, %Y'}})
    </li>
    {% endfor %}
</ul>
{% endfor %}
