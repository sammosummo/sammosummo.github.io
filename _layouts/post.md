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
</section>

{% if page.has_comments %}
  <div id="commento"></div>
  <script src="https://cdn.commento.io/js/commento.js"></script>
 {% endif %}