---
layout: page
title: Posts by topic
---
{% assign sorted = site.tags | sort %}
{% for tag in sorted %}
{% assign ttag = tag[0] %}
<h2><a name="{{ ttag }}">{{ ttag | capitalize | replace: "-", " " }}</a></h2>
<ul>
{% for post in site.tags[ttag] %}
    <li>
{% include post.html %}
    </li>
    {% endfor %}
</ul>
{% endfor %}
