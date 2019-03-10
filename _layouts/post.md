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

### Comments

Want to comment privately? Send an email to <a href="mailto:{{ site.email }}" class="break">{{ site.email }}</a>. 

{% if page.has_comments %}
  <div id="commento"></div>
  <script async src="https://cdn.commento.io/js/commento.js"></script>
 {% endif %}