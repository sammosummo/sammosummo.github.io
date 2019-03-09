<!doctype html>
<html lang="{{ page.lang | default: site.lang | default: "en" }}">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width">
        <link rel="canonical" href="{{ site.url }}{{ page.url }}" />
        <link rel="shortcut icon" type="image/png" href="{{ "/favicon.png" | relative_url }}"/>
        <link rel="stylesheet" type="text/css" href="{{ "/assets/index.css" | relative_url }}">
        <title>{{ site.title | escape }}</title>
        {% feed_meta %}
        <style>
          @media (max-width:600px) {
            img#profile-photo {
              display: none;
            }
          }
        </style>
    </head>
    <body>
        <div id="main-container">

            <div id="header" class="border-bottom">

                <div id="title-nav-bar">
                  <h1><a id="title" href="/">
                      <div id="title-profile-photo">The Cracked Bassoon</div>
                  </a></h1>

                  <div id="nav-bar">
                      <a href="/about" class="nav-bar__item">About</a>
                      <a href="/writing" class="nav-bar__item">Writing</a>
                      <a href="/publications" class="nav-bar__item">Publications</a>
                      <a href="/cocktails" class="nav-bar__item">Cocktails</a>
                  </div>
                </div>

                <div id="title-profile-photo">
                  <img id="profile-photo" src="/assets/logos/02.png" />
                </div>

                <div style="clear: left; clear right"></div>
            </div

            {{ content }}
        </div>
    </body>
</html>
