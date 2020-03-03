---
layout: default
---
{% if page.has_code %}
  <link rel="stylesheet" type="text/css" href="{{ "/assets/css/code.css" | relative_url }}">
{% endif %}

{% if page.has_math %}
  {% include mathjax.html %}
{% endif %}

<h1 class="posttitle">{{ page.title }}</h1>

{% if page.tags %}
{% assign sorted = page.tags | sort %}
{% assign last = sorted | last %}
<b>Tags</b>: {% for tag in sorted %}<a href="/tags#{{ tag }}">{% if site.data.emojis contains tag %}{{ site.data.emojis[tag] }}{% else %}🏷️{% endif %} {{ tag }}</a>{% if tag == last %}{% else %} | {% endif %}{% endfor %}
{% endif %}

{{ content }}
<hr>
{% if page.include_references %}
  {% include references.html %}
{% endif %}

{% if page.date %}
  <h2>Version history</h2>
  <ul>
    <li>Originally posted {{ page.date | date: '%B %d, %Y' }}.</li>
    {% for revision in page.revisions %}
      <li>{{ revision.reason }} on {{ revision.date | date: '%B %d, %Y' }}.</li>
    {% endfor %}
  </ul>
{% endif %}

<br>

{% if page.has_comments %}
  <div id="commento"></div>
  <script async src="https://cdn.commento.io/js/commento.js"></script>
 {% endif %}