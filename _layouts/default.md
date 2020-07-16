---
layout: compress
---
<!doctype html>
<html lang="{{ page.lang | default: site.lang | default: "en" }}">
	<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width">
    <link rel="canonical" href="{{ site.url }}{{ page.url }}" />
    <link rel="shortcut icon" type="image/png" href="{{ "/assets/images/logo-small-square.png" | relative_url }}"/>
    <link rel="stylesheet" type="text/css" href="{{ "/assets/css/fonts.css" | relative_url }}">
    <link rel="stylesheet" type="text/css" href="{{ "/assets/css/links.css" | relative_url }}">
    <link rel="stylesheet" type="text/css" href="{{ "/assets/css/logo.css" | relative_url }}">
    <link rel="stylesheet" type="text/css" href="{{ "/assets/css/main.css" | relative_url }}">
    <title>{{ site.title | escape }}</title>
    {% feed_meta %}
  </head>  
  <body>
    <div id="main-container">
      <header>
        <img id="logo" src="/assets/images/logo-big-cropped.png" />
        <h1><a id="title" href="/">The Cracked Bassoon</a></h1>
        <nav>
          <a href="/about">About</a> |
          <a href="/writing">Writing</a> |
          <a href="/publications">Publications</a>
        </nav>
        <p></p>
        <hr>
      </header>
      <article>
        {{ content }}
      </article>
      <hr>
      <footer>
        <p>Opinions expressed here do not necessarily reflect those of my employer or
        colleagues. Distributed under an MIT license. Find the source code
        <a href="https://github.com/sammosummo/sammosummo.github.io">here</a>. Private
        comments can be made via <a href="mailto:{{ site.email }}" class="break">email</a>.</p>
          
      </footer>
    </div>
  </body>
</html>
