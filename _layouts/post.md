---
layout: default
---
{% if page.has_code %}
  <link rel="stylesheet" type="text/css" href="{{ "/assets/css/code.css" | relative_url }}">
{% endif %}

{% if page.has_math %}
  {% include mathjax.html %}
{% endif %}

{% if page.title contains ":" %}
  {% assign parts = page.title | split: ":" %}
  <h1 class="posttitle">{{ parts[0] | append: ":" }}</h1>
  <div class="subtitle">{{ parts[1] }}</div>
{% else %}
  <h1 class="posttitle">{{ page.title | replace: ":", ": <br>"}}</h1>
{% endif %}


{% if page.tags %}
  {% assign sorted = page.tags | sort %}
  {% assign last = sorted | last %}
  <div class="tags">Filed under {% for tag in sorted %}<a href="/tags#{{ tag }}">{{ tag }}</a>{% if tag == last %}.{% else %}, {% endif %}{% endfor %}</div>
{% endif %}

{{ content }}

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

<h2>Related posts</h2>

<ul>
{% assign maxRelated = 4 %}
{% assign minCommonTags =  2 %}
{% assign maxRelatedCounter = 0 %}
{% for post in site.posts %}
  {% assign sameTagCount = 0 %}
  {% assign commonTags = '' %}
  {% for tag in post.tags %}
    {% if post.url != page.url %}
      {% if page.tags contains tag %}
        {% assign sameTagCount = sameTagCount | plus: 1 %}
        {% capture tagmarkup %}{% if site.data.emojis contains tag %}<a href="/tags#{{ tag }}">{{ site.data.emojis[tag] }}</a>{% endif %}{% endcapture %}
        {% assign commonTags = commonTags | append: tagmarkup %}
      {% endif %}
    {% endif %}
  {% endfor %}
  {% if sameTagCount >= minCommonTags %}
    <li>{% include post.html %}</li>
    {% assign maxRelatedCounter = maxRelatedCounter | plus: 1 %}
    {% if maxRelatedCounter >= maxRelated %}
      {% break %}
    {% endif %}
  {% endif %}
{% endfor %}
{% assign sorted = page.tags | sort %}
{% assign last = sorted | last %}
<li>All posts filed under {% for tag in sorted %}<a href="/tags#{{ tag }}">{{ tag }}</a>{% if tag == last %}.{% else %}, {% endif %}{% endfor %}</li>
</ul>

{% if page.has_comments %}
  <div id="commento"></div>
  <script async src="https://cdn.commento.io/js/commento.js"></script>
{% endif %}