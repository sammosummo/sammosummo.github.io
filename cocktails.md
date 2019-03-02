---
layout: page
title: Cocktails
---

Here are some of my favorite cocktail recipes. 🍸

<ul>
{% for cocktail in site.data.cocktails.cocktails %}
  <li><h3>{{cocktail.name}}</h3></li>
  <ul>{% for ingredient in cocktail.ingredients %}<li>{{ingredient}}</li>{% endfor %}</ul>
  <p>{{cocktail.recipe}}</p>
  <p><i>{{cocktail.notes}}</i></p>
{% endfor %}
</ul>
