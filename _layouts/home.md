---
layout: default
---

<h2>What is this?</h2>

<i>The Cracked Bassoon</i> is the personal website of <a href="about">Sam Mathias</a>, a curmudgeonly English researcher based in
Boston, MA. It contains code snippets, stray observations, and wildly misinformed opinions
on a range of science-related topics. Perhaps you’ll find something interesting here, but
probably not. I wouldn’t stick around if I were you.

<h2>Latest writing</h2>

Please note that because the following has not been peer reviewed, it might be pure
nonsense. <a href="writing">Click here for the archive</a>.

<ul>
<li>
{% for post in site.posts limit:1%}
  <a href="{{ post.url }}">{{ post.title }}</a>, posted {{ post.date | date: '%B %d, %Y'}}.
{% endfor %}
</li>
</ul>
<h2>Latest publication</h2>

The following has been peer reviewed, so is less likely to be nonsense.
<a href="publications">Click here for the complete list</a>.
<ul>
<li>
{% assign sorted = site.data.my_papers.my_papers | sort: 'sort' | reverse %}
{% for paper in sorted limit:1 %}
  {% if paper.book %}
    {{ paper.authors }}
    ({{ paper.year }}).
    {{ paper.title }}
    {{ paper.editor }},
    <i>{{ paper.book }}</i>
    {% if paper.collection %}
      ({{ paper.collection }}, vol. {{ paper.volume }}, pp. {{ paper.first_page }}–{{ paper.last_page }}).
    {% else %}
      {% if paper.volume %}
        (vol. {{ paper.volume }}, pp. {{ paper.first_page }}–{{ paper.last_page }}).
      {% else %}
        (pp. {{ paper.first_page }}–{{ paper.last_page }}).
      {% endif %}
    {% endif %}
    {{ paper.city }}, {{ paper.state }}: {{ paper.publisher }}.
  {% else %}
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
    DOI: <a href="{{ paper.doi_link }}" class="break">{{ paper.doi }}</a>.
    {% if paper.pmid %}
      PubMed: <a href="{{ paper.pmid_link }}" class="break">{{ paper.pmid }}</a>.
    {% endif %}
  {% endif %}
{% endfor %}
</li>
</ul>