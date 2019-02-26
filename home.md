---
layout: default
---

{% include about_short.html %}

<h3>Latest writing</h3>
<ul>
{% for post in site.posts limit:1%}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a> ({{ post.date | date: '%B %d, %Y'}})
    </li>
{% endfor %}
</ul>
<h3>Most recent publication</h3>
<ul>
{% assign sorted = site.data.my_papers.my_papers | sort: 'sort' | reverse %}
{% for paper in sorted limit:1 %}
  <p><li>
  {{ paper.authors }}
  ({{ paper.year }}).
  {{ paper.title }}
  {% if paper.first_page %}
    <i>{{ paper.journal }}</i>,
    {% if paper.volume %}
      {% if paper.issue %}
        {{ paper.volume }} ({{ paper.issue }}),
      {% else %}
         {{ paper.volume }},
      {% endif %}
    {% endif %}
    {% if paper.last_page %}
      {{ paper.first_page }}–{{ paper.last_page }}.
    {% else %}
      {{ paper.first_page }}.
    {% endif %}
  {% else %}
    <i>{{ paper.journal }}</i>.
  {% endif %}
  DOI: <a href="{{ paper.doi_link }}">{{ paper.doi }}</a>.
  PubMed: <a href="{{ paper.pmid_link }}">{{ paper.pmid }}</a>.
  </li></p>
{% endfor %}
</ul>

<h3>Contact</h3>
{% include contact.html %}