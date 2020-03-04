---
layout: default
---
<br>

This is the personal website of <a href="about">Sam Mathias</a>, a curmudgeonly English researcher based in
Boston, MA. It contains code snippets, stray observations, and wildly misinformed opinions
on a range of science-related topics. Perhaps you’ll find something interesting here, but
probably not. I wouldn’t stick around if I were you.

<h2>Latest writing</h2>
    
<ul>
<li>
{% for post in site.posts limit:1%}
    {% include post.html %}
{% endfor %}
</li>
</ul>

Fair warning: because none of what appears on this website has been peer-reviewed, it might be pure
nonsense! <a href="writing">Click here for the archive</a>.

<h2>Latest publication</h2>

{% assign paper = site.data.my_papers | sort | last %}
{% include citation.html %}

<a href="publications">Click here for the complete list.</a>
