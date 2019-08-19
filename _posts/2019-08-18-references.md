---
layout: post
title: Reference lists in Jekyll
date: 2019-08-18
has_code: true
has_comments: true
include_references: true
references:
 - Gelman2006a
---

Academic work needs to cite its sources. There's nothing to say that the personal websites
of academics have to adhere to the same rigorous standards as papers, but still, I think
it's nice to include proper references on webpages. This can be a chore, which is why I
came up with the following method to generate reference lists programmatically in
[Jekyll](https://jekyllrb.com/).

When I want to add a new reference to a blog post, I first add its record to
`/_data/references.yaml`. Here's what the top of this file looks like (showing the first
record):

```yaml
references:

 - id: "Gelman2006a"
   authors: "Gelman, A."
   volume: "48"
   issue: "3"
   year: "2006"
   title: "Multilevel (hierarchical) modeling: What it can and cannot do."
   first_page: "432"
   last_page: "435"
   doi: "10.1198/004017005000000661"
   journal: "Technometrics"
```

Next I add the record's ID to the front matter of the post. For example, the front matter
of this post, which cites above paper by [Gelman (2006)](#Gelman2006a), reads like this:

```yaml
---
layout: post
title: Reference lists in Jekyll
date: 2019-08-18
has_code: true
has_comments: true
include_references: true
references:
 - Gelman2006a
---
```

The inline citation above looks like this:

```markdown
Next I add the record's ID to the front matter of the post. For example, the front matter
of this post, which cites above paper by [Gelman (2006)](#Gelman2006a), reads like this:
```

Finally, the following HTML/Liquid code, included in the `post.md` layout file, picks up
and formats the appropriate record(s) into a reference list at the end of the file.

{% raw %}
```liquid
{% if page.include_references %}
<hr>
<h2>References</h2>
<ul class="refs">
{% assign sorted = site.data.references.references | sort: 'authors' %}
  {% for paper in sorted %}
    {% if page.references contains paper.id %}
    <li><a name="{{ paper.id }}"></a>
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
    {% if paper.arXiv %}
      arXiv: <a href="https://arxiv.org/abs/{{ paper.arXiv }}">{{ paper.arXiv }}</a>.
    {% endif %}
    {% if paper.pmid %}
      PMID: <a href="https://www.ncbi.nlm.nih.gov/pubmed/?term={{ paper.pmid }}">{{ paper.pmid }}</a>.
    {% endif %}
    </li>
  {% endif %}  
{% endfor %}
</ul>
{% endif %}
```
{% endraw %}

The reference style does not conform exactly to any particular standard—I like to call it
"APA-ish." It handles whole books, book chapters, regular journal articles, and preprints
reasonably well. I might change or update it in the future.

I use a similar method to create a [list of my own publications](/publications), which I'll
describe in a future post.