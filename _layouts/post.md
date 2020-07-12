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

<h2>Related posts</h2>
<ul>

{% assign sorted = page.tags | sort %}
<li>Filed under: {% for tag in sorted %}<a href="/tags#{{ tag }}">{% if site.data.emojis contains tag %}{{ site.data.emojis[tag] }}{% else %}🏷️{% endif %} {{ tag }}</a>{% if tag == last %}{% else %} | {% endif %}{% endfor %}</li>
<li>Related:
<div class="related"><ul>
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
</ul></div>
</li>
{% if page.previous.url %}
  {% assign post = page.previous %}
  <li>Previous:<ul><div class="related"><li>{% include post.html %}</li></div></ul></li>
{% endif %}
{% if page.next.url %}
  {% assign post = page.next %}
  <li>Next:<ul><div class="related"><li>{% include post.html %}</li></div></ul></li>
{% endif %}



</ul>