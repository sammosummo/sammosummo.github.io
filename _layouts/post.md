---
layout: default
---
{% if page.has_code %}
  <link rel="stylesheet" type="text/css" href="{{ "/assets/css/code.css" | relative_url }}">
{% endif %}

{% if page.has_math %}
  {% include mathjax.html %}
{% endif %}

<h1>{{ page.title }}</h1>
{{ content }}
{% if page.include_references %}
  {% include references.html %}
{% endif %}

{% if page.date %}
<hr>
  <h2>Version history</h2>
  <ul>
    <li>Originally posted {{ page.date | date: '%B %d, %Y' }}.</li>
    {% for revision in page.revisions %}
      <li>{{ revision.reason }} on {{ revision.date | date: '%B %d, %Y' }}.</li>
    {% endfor %}
  </ul>
{% endif %}


{% if page.has_comments %}
<hr>
<h2>Comments</h2>
  <div id="commento"></div>
  <script async src="https://cdn.commento.io/js/commento.js"></script>
 {% endif %}