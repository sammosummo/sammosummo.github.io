---
date: 2020-09-02
has_code: true
has_comments: true
include_references: true
layout: post
references:
- Myung2003a
tags:
- jekyll
- liquid
- references
- python
title: Scholarly references in Jekyll
---

This post is about properly referencing scholarly work in [Jekyll](https://jekyllrb.com/). Traditional academic media
use strictly codified reference systems, including _citations_ (inline acknowledgements of specific findings, ideas, or
quotations) and _bibliographies_ (complete lists of relevant work, alphabetically or chronologically organized, usually
found at the end of the document). Unfortunately, references in non-traditional media, such as blog posts, can be
frustratingly lackluster.

Since this website is mostly about science, I wanted it to have a strong reference system, like those found in
academic journals, with both inline citations and bibliographies. Crucially, I didn't want to simply type everything by
hand every time, since doing so would take forever and would likely introduce many errors. Like many academics, I use
[reference management software](https://en.wikipedia.org/wiki/Reference_management_software) routinely as part of my day
job, which takes the sting out of references when writing manuscripts. So I cobbled together a loose "system" that
vaguely resembles the functionality of a reference manager specifically for this website. It's not a particularly
elegant solution, but it gets the job done reasonably well. This post describes my system.

## Getting references

I've used practically every major reference manager over the years. My favorite by, a long way, is [Zotero](https://www.zotero.org/).
Among Zotero's many useful features is the "magic wand" button, which quickly adds items along with all metadata to
the library given the ISBN, DOI, or PubMed ID. You get slight but annoying differences in the metadata if you use the
different identifiers, but so long as you use DOI wherever possible, it works well most of the time.

My Zotero library contains all the references I need for work. Since the references for this website are a
subset of those, I wanted to make Jekyll talk to my Zotero library to grab the references needed for each blog post. I couldn't
come up with a fully automated way of doing this, unfortunately. Instead, I wrote a Python script to extract metadata
from each item in my Zotero library and store it in a [YAML](https://yaml.org/) file. By placing this YAML file in
Jekyll's special `_data` directory, the metadata gets read into Jekyll and is accessible via [Liquid](https://shopify.github.io/liquid/)
whenever my website is rebuilt. This Python script, reproduced below, uses the [Pyzotero](https://pyzotero.readthedocs.io/en/latest/)
third-party package. (Zotero's web API is another great advantage of this reference manager!) I run this script as part
of a collection of scripts every time I rebuild my site. I'll describe another script in this collection shortly.

```python
{{ site.data.code.zotero__py }}
```

A typical entry in the resulting `refs.yaml` file is:

```yaml
Myung2003a:
   authors: "Myung, I. J."
   year: "2003"
   title: "Tutorial on maximum likelihood estimation"
   journal: "Journal of Mathematical Psychology"
   volume: "47"
   issue: "1"
   doi: "10.1016/S0022-2496(02)00028-7"
   first_page: "90"
   last_page: "100"
   citep: "[(Myung, 2003)](#Myung2003a)"
   citenp: "[Myung, 2003](#Myung2003a)"
   citet: "[Myung (2003)](#Myung2003a)"
```

## Citations

In the YAML snippet from the previous section, the meanings of most of the different variables are probably obvious. The
last three are used to create inline citations via Liquid. For example, to include a citation I include the following in
the body of the text.

{% raw %}
```liquid
{{ site.data.refs.Myung2003a.citet }}
```
{% endraw %}

This produces: {{ site.data.refs.Myung2003a.citet }}. Notice how the citation is also an internal link to the
corresponding item in the bibliography! I'm quite proud of that bit. `citet` is for text citations, `citep` is for
parenthetical citations {{ site.data.refs.Myung2003a.citep }}, and `citenp` is for parenthetical citations
without the parentheses. `citenp` is useful for constructing parenthetical citations containing extra text (e.g.,
{{ site.data.refs.Myung2003a.citenp}}).

## Pulling out citations

My system requires that every post containing a reference needs that reference's key (e.g., `Myung2003a`) in a YAML list
called `references` in its front matter. I have another Python script that scans through all my existing posts to find
all citations and create this YAML list. It would be nice to make Jekyll do this instead of Python, but I don't know
how. Here's that script:

```python
{{ site.data.code.add_refs__py }}
```

### Generating the bibliography

The final part of my system is to generate the post's bibliography. I use a boolean variable in the front matter called
`include_references` to enable bibliography generation (I wrote about toggling features [previously](toggling)). Below
is the relevant Liquid snippet within my `post.md` template, placed immediately after {% raw %}`{{ content }}`{% endraw %}.

{% raw %}
```liquid
{% if page.include_references %}
  {% include references.html %}
{% endif %}
```
{% endraw %}

In my `_includes` folder is a template called `refences.html`, which looks like this:

{% raw %}
```liquid
<h2>References</h2>
{% assign refs = site.data.refs | sort %}
{% for paper in refs %}
    {% for ref in page.references %}
        {% if ref == paper[0] %}
            {% include citation.html %}
        {% endif %}
    {% endfor %}
{% endfor %}
```
{% endraw %}

This loops over each reference in the site-wide `references.yaml`; if a given reference is also in the `references` list
within the post's local YAML data, the reference is assigned the variable `paper`, which is then used in a third
template called `citation.html`:

{% raw %}
```liquid
<p class="refs"><a name="{{ paper[0] }}"></a>
    {{ paper[1].authors }} ({{ paper[1].year }}).
    {% if paper[1].title %}
        {{ paper[1].title }}.
    {% endif %}
    {% if paper[1].editor %}
        {{ paper[1].editor }},
    {% endif %}
    {% if paper[1].book and paper[1].collection and paper[1].volume %}
        <i>{{ paper[1].book }}</i> ({{ paper[1].collection }} vol {{ paper[1].volume }}, pp. {{ paper[1].first_page }}–{{ paper[1].last_page }}).
    {% else %}
        {% if paper[1].book and paper[1].volume %}
            <i>{{ paper[1].book }}</i> (vol {{ paper[1].volume }}, pp. {{ paper[1].first_page }}–{{ paper[1].last_page }}).
        {% else %}
            {% if paper[1].book and paper[1].first_page %}
                <i>{{ paper[1].book }}</i> (pp. {{ paper[1].first_page }}–{{ paper[1].last_page }}).
            {% else %}
                {% if paper[1].book and paper[1].edition %}
                    <i>{{ paper[1].book }}</i> ({{ paper[1].edition }} ed.).
                {% else %}
                    {% if paper[1].book %}
                        <i>{{ paper[1].book }}</i>.
                    {% endif %}
                {% endif %}
            {% endif %}
        {% endif %}
    {% endif %}
    {% if paper[1].book %}
        {{ paper[1].publisher }}.
    {% endif %}
    {% if paper[1].journal %}
        {% if paper[1].volume or paper[1].first_page %}
            <i>{{ paper[1].journal }}</i>,
            {% if paper[1].volume %}
                {% if paper[1].issue %}
                    {% if paper[1].first_page %}
                        <i>{{ paper[1].volume }}</i>({{ paper[1].issue }}),
                    {% else %}
                        <i>{{ paper[1].volume }}</i>({{ paper[1].issue }}).
                    {% endif %}
                {% else %}
                    {% if paper[1].first_page %}
                        <i>{{ paper[1].volume }}</i>,
                    {% else %}
                        <i>{{ paper[1].volume }}</i>.
                    {% endif %}
                {% endif %}
            {% endif %}
            {% if paper[1].first_page %}
                {% if paper[1].last_page %}
                    {{ paper[1].first_page }}–{{paper[1].last_page }}.
                {% else %}
                    {{ paper[1].first_page }}.
                {% endif %}
            {% endif %}
        {% else %}
            <i>{{ paper[1].journal }}</i>.
        {% endif %}
    {% endif %}
    {% if paper[1].doi %}
    <a href="https://doi.org/{{ paper[1].doi }}">{{ paper[1].doi }}</a>
    {% endif %}
    {% if paper[1].arXiv %}
        arXiv:<a href="https://arxiv.org/abs/{{ paper[1].arXiv }}">{{ paper[1].arXiv }}</a>.
    {% endif %}
</p>
```
{% endraw %}

The above code is quite involved and difficult to read. Basically, it takes the information stored within `paper` and
formats it into a style I call "APAish." You can see the results immediately below.