---
layout: page
title: Publications
---

{% assign counter=0 %}
{% for paper in site.data.my_papers %}
  {% assign counter=counter | plus:1 %}
{% endfor %}

I currently have {{counter}} first-authored or coauthored peer-reviewed publications. The
following is my "official" publication list and is maintained manually. It may differ
slightly from the automatically generated lists at
[PubMed](https://www.ncbi.nlm.nih.gov/pubmed/?term=mathias+sr%5BAuthor%5D) and
[Google Scholar](https://scholar.google.com/citations?user=fRRZs_4AAAAJ&hl=en). If a
manuscript is behind a paywall 🙄 please feel free to
[drop me an email](mailto:reprints@crackedbassoon.com).

{% assign papers = site.data.my_papers | sort %}
{% for paper in papers reversed %}
  {% include citation.html %}
{% endfor %}
