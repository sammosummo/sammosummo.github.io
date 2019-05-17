---
layout: page
title: Publications
---

{% assign counter=0 %}
{% for paper in site.data.my_papers.my_papers %}
  {% assign counter=counter | plus:1 %}
{% endfor %}

I currently have {{counter}} first-authored or coauthored peer-reviewed publications. The
following is my "official" publication list and is maintained manually. It may differ
slightly from the automatically generated lists at
[PubMed](https://www.ncbi.nlm.nih.gov/pubmed/?term=mathias+sr%5BAuthor%5D) and
[Google Scholar](https://scholar.google.com/citations?user=fRRZs_4AAAAJ&hl=en).

If a manuscript is behind a paywall 🙄 
[send me an email](mailto:reprints@crackedbassoon.com) and I'll send you a PDF copy as
soon as possible.

<ul>
{% assign sorted = site.data.my_papers.my_papers | sort: 'sort' | reverse %}
{% for paper in sorted %}
  <p><li>
  {% if paper.book %}
    {{ paper.authors }}
    ({{ paper.year }}).
    {{ paper.title }}
    {{ paper.editor }},
    <i>{{ paper.editor }}</i>
    {% if paper.collection %}
      ({{paper.collection }} vol. {{ paper.volume }}, pp. {{ paper.first_page }}–{{ paper.last_page }}).
    {% if paper.volume %}
      (vol. {{ paper.volume }}, pp. {{ paper.first_page }}–{{ paper.last_page }}).
    {% else %}
      (pp. {{ paper.first_page }}–{{ paper.last_page }}).
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
    </li></p>
  {% endif %}
{% endfor %}
</ul>

{% for book_group in site.data.books.book_groups %}
    {% assign sorted = book_group.books | sort: 'name' %}
    {% for book_or_series in sorted %}
        {% if book_or_series.series %}
            {% for book in book_or_series.books %}
                <li>
                    <a href="{{book.amazon_link}}">{{book.name}}</a>,
                    <i class="no-wrap">{{book_or_series.author}}</i>
                </li>
            {% endfor %}
        {% else %}
            {% assign book = book_or_series %}
            <li class="{{class}}">
                <a href="{{book.amazon_link}}">{{book.name}}</a>,
                <i class="no-wrap">{{book.author}}</i>
            </li>
        {% endif %}
    {% endfor %}
    <br/>
{% endfor %}

