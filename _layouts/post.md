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
    <div><p><i>Originally posted {{ page.date | date: '%B %d, %Y' }}.</i></p></div>
  {% endif %}

  {{ content }}
  </br>
  <hr>
  {% if page.date %}
    <h2>Version history</h2>
    <ul><li>Originally posted {{ page.date | date: '%B %d, %Y' }}.</li>
    {% for revision in page.revisions %}
      <li>{{ revision.reason }} on {{ revision.date | date: '%B %d, %Y' }}.</li>
    {% endfor %}
    </ul>
    {% endif %}
</section>
</br>
<hr>

{% if page.has_comments %}
  <div id="commento"></div>
  <script async src="https://cdn.commento.io/js/commento.js"></script>
 {% endif %}
 
<p><i>If you’d like to comment privately on anything you’ve seen here,
email me at <a href="mailto:{{ site.email }}" class="break">{{ site.email }}</a>.

Along with the rest of this website, this page is distributed under an MIT license. Do what
you like with it. In fact, here’s the <a href="https://github.com/sammosummo/sammosummo.github.io">source code</a>!
</i></p>