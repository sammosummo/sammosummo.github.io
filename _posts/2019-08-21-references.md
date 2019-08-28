---
layout: post
title: Reference lists in Jekyll
date: 2019-08-21
has_code: true
has_comments: true
include_references: true
references:
 - Gelman2006a
tags:
 - Jekyll
 - Liquid
---

While there is nothing to say that the personal websites of academics have to adhere to
the same rigor as academic publications, I think it's nice when webpages include proper
references. Formatting such references by hand can be a chore, however, which is why I
came up with the following method to generate reference lists programmatically in
[Jekyll](https://jekyllrb.com/).

When I want to add a new reference to a blog post, I first add a record of the reference
to a special [YAML](https://yaml.org/) file called `references.yaml` stored within the
`/_data/` subdirectory. Any YAML-formatted data within this directory becomes accessible
throughout the site via [Liquid](https://shopify.github.io/liquid/). Here's what the top
of `references.yaml` currently looks like, showing the first record:

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

Next I add the `id` of the reference I wish to cite and a boolean variable called
`include_references` to the [front matter](https://jekyllrb.com/docs/front-matter/) of the
post, as follows:

```yaml
---
include_references: true
references:
 - Gelman2006a
---
```

I also include an in-line citation, such as [Gelman (2006)](#Gelman2006a), to the
appropriate place in the main body of the post. Jekyll posts are written in 
[Markdown](https://daringfireball.net/projects/markdown/), and the citation is a Markdown
internal hyperlink with same label as the reference's `id`. For example:

```markdown
[Gelman (2006)](#Gelman2006a)
```

Two additional files are necessary to evaluate the reference `id` stored in the front
matter and resolve the in-line citation's hyperlink. The first is the `post.md`
[layout file](https://jekyllrb.com/docs/layouts/). This file contains the following three
lines of Liquid code, which include another HTML is the current one if
`include_references` is `True`:

{% raw %}
```liquid
{% if page.include_references %}
  {% include references.html %}
{% endif %}
```
{% endraw %}

Finally, `references.html` contains more Liquid code that loops over all records within
`references.yaml`, filters them by whether their `id` appears in the front matter of the
current post, formats these references, and displays them in a list. Here is what this
file currently looks like:

{% raw %}
```liquid
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
```
{% endraw %}

The reference style is my own creation and doesn't conform exactly to any particular
standard—I call it "APA-ish." It handles whole books, book chapters, regular journal
articles, and preprints reasonably well. I might change or update it in the future.

I use a similar method to create a [list of my own publications](/publications), which I'll
describe in a future post.