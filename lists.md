---
layout: page
title: Lists
---

I enjoy reading, so here's a non-exhaustive list of books I've read, grouped by year in descending order. I've excluded any I didn't finish or any whose plot I don't remember.

{% assign counter=0 %}
{% for book_group in site.data.books.book_groups %}
    {% assign sorted = book_group.books | sort: 'name' %}
    {% for book_or_series in sorted %}
        {% if book_or_series.series %}
            {% for book in book_or_series.books %}
                {% assign counter=counter | plus:1 %}
            {% endfor %}
        {% else %}
            {% assign counter=counter | plus:1 %}
        {% endif %}
    {% endfor %}
{% endfor %}

<b>Total count:</b> {{counter}}

<ul>
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
</ul>
