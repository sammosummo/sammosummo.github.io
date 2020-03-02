---
layout: page
title: Posts by topic
---
{% assign sorted = site.tags | sort %}
{% for tag in sorted %}
{% assign ttag = tag[0] %}
<h4><a name="{{ ttag }}"></a>{% if site.data.emojis contains ttag %}{{ site.data.emojis[ttag] }}{% else %}🏷️{% endif %} {{ ttag }}</h4>
<ul>
{% for post in site.tags[ttag] %}
    <li>
{% include post.html %}
    </li>
    {% endfor %}
</ul>
{% endfor %}
