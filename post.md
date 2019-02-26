---
layout: default
---

<span/>

{% if page.has_code %}
  <link rel="stylesheet" type="text/css" href="{{ "/assets/code.css" | relative_url }}">
{% endif %}

{% if page.has_math %}
  {% include mathjax.html %}
{% endif %}

<section>
  <h2>{{ page.title }}</h2>

  {% if page.date %}
    <p class="small"><i>Originally posted {{ page.date | date: '%B %d, %Y' }}.</i></p>
  {% endif %}

  {{ content }}
  
  <p class="small"><i>I haven't enabled comments yet. Meanwhile, if you spot an error
  or have a question, email me at <a href="mailto:{{ site.email }}">{{ site.email }}</a>.</i></p>
</section>
