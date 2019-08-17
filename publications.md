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
[Google Scholar](https://scholar.google.com/citations?user=fRRZs_4AAAAJ&hl=en). If a
manuscript is behind a paywall 🙄  please feel free to
[drop me an email](mailto:reprints@crackedbassoon.com).

<ul class="refs">
{% assign sorted = site.data.my_papers.my_papers | sort: 'sort' | reverse %}
{% for paper in sorted %}
  <li>
  {{ paper.authors }} ({{ paper.year }}). {{ paper.title }}
  {% if paper.editor %}{{ paper.editor }},{% endif %}
  {% if paper.book and paper.collection and paper.volume %}
    <i>{{ paper.book }}</i> ({{ paper.collection }} vol {{ paper.volume }},
    pp. {{ paper.first_page }}–{{ paper.last_page }}).
  {% else %}
    {% if paper.book and paper.volume %}
      <i>{{ paper.book }}</i> (vol {{ paper.volume }},
      pp. {{ paper.first_page }}–{{ paper.last_page }}).
    {% else %}
      {% if paper.book and paper.first_page %}
        <i>{{ paper.book }}</i> (pp. {{ paper.first_page }}–{{ paper.last_page }}).
        {% else %}
          {% if paper.book %}<i>{{ paper.book }}</i>.{% endif %}
        {% endif %}   
    {% endif %}
  {% endif %}
  {% if paper.book %}
    {{ paper.city }}, {{paper.state }}: {{ paper.publisher }}.
  {% endif %}
  
  {% if paper.journal %}
    {% if paper.volume or paper.first_page %}
      <i>{{ paper.journal }}</i>,
      {% if paper.volume %}
        {% if paper.issue %}
          {% if paper.first_page %}
            <i>{{ paper.volume }}</i>({{ paper.issue }}),
          {% else %}
            <i>{{ paper.volume }}</i>({{ paper.issue }}).
          {% endif %}
        {% else %}
          {% if paper.first_page %}
            <i>{{ paper.volume }}</i>,
          {% else %}
            <i>{{ paper.volume }}</i>.
          {% endif %}
        {% endif %}
      {% endif %}
      {% if paper.first_page %}
        {% if paper.last_page %}
          {{ paper.first_page }}–{{paper.last_page }}.   
        {% else %}
          {{ paper.first_page }}.
        {% endif %}
      {% endif %}
    {% else %}
      <i>{{ paper.journal }}</i>.
    {% endif %}
  {% endif %}
  {% if paper.doi %}
    DOI: <a href="https://doi.org/{{ paper.doi }}">{{ paper.doi }}</a>.
  {% endif %}
  {% if paper.pmid %}
    PMID: <a href="https://www.ncbi.nlm.nih.gov/pubmed/?term={{ paper.pmid }}">{{ paper.pmid }}</a>.
  {% endif %}
  </li>
{% endfor %}
