---
date: 2020-06-24
has_code: true
has_comments: true
layout: post
revisions:
- date: 2020-07-02
  reason: Re-wrote lots of text
short_title: Audiobooks I
tags:
- audiobooks
- jekyll
- liquid
- python
title: Audiobooks-o-rama
---

I love fiction, but I'm a very slow reader. I'm 35 now, and I've read about 50 books in my life, which is pretty terrible.
If I'd read the same number of books per year as the average person ([which is 12, apparently](https://irisreading.com/how-many-books-does-the-average-person-read/)),
I should be well past 200 by now. My wife—a prolific reader herself [with a blog on the
topic](https://emmablogsbooks.com)—suggested I try audiobooks. I discovered [Libby](https://www.overdrive.com/apps/libby/) in March 2019,
and it completely transformed how I consume literature. Now, just over a year and around
100 audiobooks later, I decided to compile some thoughts on the topic and review everything
I've listened to so far. This post goes covers [how I acquire audiobooks](#acquisition), [what I like](#taste),
and provides geeky details of how I compiled [a database of my reviews](#code). If you don't
care about any of this and just want some recommendations, I suggest jumping to my [next post, which lists
my favorites](audiobooks-2).

## Where I get them<a name="acquisition"></a>

About 90% of my audiobooks come from [Libby](https://www.overdrive.com/apps/libby/). Libby
is a free mobile app from [Overdrive](https://company.overdrive.com/?_ga=2.215002079.990475370.1586801728-e87a6c4b-3216-4681-8f15-ed356a1f4f29)
that connects to many local libraries across the USA. If you're a member of one or more of
these libraries ([see here for a list](https://www.overdrive.com/libraries)), you can use
it will deliver loans straight to your e-reader or phone for free.
Given that audiobooks can be pretty expensive, Libby may save you a small fortune.

![](/assets/images/libby-icon.png)
*The Libby icon. From [their website](https://www.overdrive.com/apps/libby/).*

As a resident of Massachusetts, I'm eligible for membership of all libraries in my state.
Individual town libraries are typically syndicated into larger networks, allowing them to
offer larger catalogs, but even these networks tend have fairly limited audiobook offerings.
Initially I signed up to several small-town networks, but found that many of the audiobooks I
wanted either had few copies, leading to long hold times (more on holds shortly),
or no copies at all. Luckily for me, [Boston Public Library](https://www.bpl.org/) is huge,
and I can get most of what I'm after from there.

If you live outside the USA or in an area without a library in the Overdrive network, you can
sign up for membership of several big US libraries online for an annual fee. [Here is a useful article](https://www.aworldadventurebybook.com/blog/libraries-with-non-resident-borrowing-privileges).
I signed up for the [Brooklyn Public Library](https://www.bklynlibrary.org/). Membership
costs $50 a year for a non-resident and is absolutely worth the money.

If—and only if—a particular book isn't available through Libby, I use [Audible](https://www.audible.com/).
Audible's subscription service is quite expensive, but it's pretty good. As a member, you
get one or two credits per month, plus access to sales and special offers. I recommend signing up to
their newsletters so that you don't miss offers. When I first signed up, there was a sale on
fantasy novels; I picked up a ton of them for considerably less than the cost of credits.
Audible's no-questions-asked return policy is a big plus. Also, since my wife is part of
my [Amazon Household](https://www.amazon.com/myh/households), I'm able to take advantage of
[Whispersync](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000827761) to get books
she's already read and recommends at a reduced price.

There are numerous other paid audiobook services. I haven't tried any others yet because I
haven't encountered any instances where an audiobook was only available or much cheaper elsewhere. Some of these
other services are more supportive of independent booksellers and I suppose I should use them
instead of an Amazon company. If anyone has recommendations, feel
free to leave a comment at the end of this post.

## When I request and borrow

The major limitation of borrowing audiobooks is that you generally can't listen to what you
want when you want. There's just no way around the fact that hold times for popular books
tend to be long. One of the first books I tried to borrow was *The Blind Assassin* and I'm
still on hold, over a year later!

Using Libby requires a bit of planning and a lot of patience. Becoming a member of multiple
libraries helps a lot (see above). I tend to spam holds, placing them on everything I'm even
vaguely interested in, until I'm maxed out. I request the same book at multiple libraries.

But I also try to be nice to other borrowers. When a book is ready to be borrowed, I decide
whether I really want it, and whether I can realistically finish it, before borrowing. I
never have more than one copy of a book at a time, returning the copy with the shorter shelf
time. I'm aggressive in returning books I'm not enjoying. (What's the point of powering through
when I could be listening to something better? And if I change my mind, I'll just request it
again some other time.) I return a book as soon as I'm done, obviously.

## Listening speed

There's no way I could listen to so many audiobooks at their natural speed. I usually listen
to somewhere between 2.5 and 3 times speed, depending on the narrator and writing. If find
myself ramping up gradually throughout a performance, especially if I'm listening to books
from the same series back-to-back, since these usually have the same narrator(s).

My friends and family are incredulous about this and insist I must be constantly missing
plot details and nuances in the performances. They could be right—all I can say in my defense
is that I'm enjoying them regardless.

I get through books pretty quickly. I listen any time I'm doing something repetitious and
nonverbal, such as walking the dog, laundry, and the daily commute—that is, when I had a
daily commute in the pre-COVID-19 world. I'm able to finish a novella in a day, which
puts me roughly on par with my wife's book-reading.

## What I like<a name="taste"></a>

I really like grim, macabre, surreal stuff. My favorite things to read, watch, and listen
to are those that go right up to the edge of being enjoyable. This goes for all art forms.

I'm a man in his late thirties with a background in science, so yes, I listen to a lot of
sci fi and fantasy. I like all the magic and monsters and stuff. However, I am very aware
of the rampant misogyny that plagues both of these genres, and understand that this is a big
turn-off for many readers/listeners. It is a problem for me too, and I give extra credit
to books that manage to avoid sexist tropes and one-dimensional female characters.

I could care less about military fiction, true crime, romance, or young adult.
I'm game for most other genres. I listen to male and female writers fairly equally.

I haven't tried any non-fiction yet.

## My reviews 

I've reviewed every audiobook I've listened to since March 2019. I have given each book
and performance a rating independently, both out of 10. I take the mean to get an overall score.

I'm neither a critic nor a particularly good writer, and there are few things in the world
that interest me less than some amateur's prolix opinions about art on the internet. So
I try to keep my reviews sparse and direct. This is especially true of my performance reviews:
since one narrator will read many books with little appreciable variation in
quality, there isn't always much to say.

## The geeky bit<a name="code"></a>

I'm a quantitative scientist, so naturally I turned my audiobook reviews into a coding
side-project. This website is built using [Jekyll](https://jekyllrb.com/), which is capable of processing
data stored in [YAML](https://yaml.org/) via [Liquid](https://shopify.github.io/liquid/).
Each time I finish an audiobook, I add my review to a data file called `audiobooks.yaml`.
A typical entry looks like this:

```yaml
- audible_url: https://www.audible.com/pd/My-Year-of-Rest-and-Relaxation-Audiobook/B07BB2QD6Y?ref=a_author_Ot_c19_lProduct_1_2&pf_rd_p=1ae0e65e-ad09-4aa7-aa73-772cefb1b5e1&pf_rd_r=M5K9C1703TKWAZSZA5FG
book: 8
book_review:
  A bit lighter than Moshfegh’s previous works in the sense that nobody gets killed this time, but still pretty
  horrible. It is a testament to the quality of the writing that I was thoroughly entertained by the idea of
  self-obsessed New York hipster spending a year in bed. I found the descriptions of the artwork hilarious.
goodreads_id: "44279110"
performance: 8
performance_review:
  Great.
```

Notice that I only include information that I cannot get programmatically from other sources, such as my scores and
reviews. I use Python to read in the manual YAML data as a dictionary, update it, then re-save within `audiobooks.yaml`.

As the name suggests, `audible_url` stores the URL to the audiobook's Audible page. It turns out that Audible stores
lots of audiobook details, such as the title, author, narrator(s), and duration, within a bit of JSON at the top of
every page. I use the third-party package [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to
scrape this data:

```python
def audible(url):
    """Add book details from Audible.com webpage.

    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    jsn = soup.find_all("script", type="application/ld+json")[1]
    data = json.loads(jsn.contents[0])[0]
    m = data["duration"].lstrip("PT").split("H")[1].split("M")[0]
    dic = {
        "audible_popularity": int(data["aggregateRating"]["ratingCount"]),
        "audible_score": float(data["aggregateRating"]["ratingValue"]),
        "year": int(data["datePublished"].split("-")[0]),
        "month": int(data["datePublished"].split("-")[1]),
        "day": int(data["datePublished"].split("-")[2]),
        "hours": int(data["duration"].lstrip("PT").split("H")[0]),
        "minutes": int(m) if m else 0,
        "image": data["image"],
        "title": data["name"].replace("'", "’"),
        "authors": [a["name"] for a in data["author"]],
        "narrators": [r["name"] for r in data["readBy"]],
    }
    return dic
```

I also use `goodreads_id` to grab a bit more data via the [Goodreads API Client](https://pypi.org/project/goodreads-api-client/).
You will need your own API key to use the function below yourself.

```python
def goodreads(grid, key):
    """Add book details from Goodreads API.

    """
    client = goodreads_api_client.Client(developer_key=key)
    result = client.Book.show(grid)
    dic = {}

    if result["series_works"]:

        series = result["series_works"]["series_work"]
        series = [series] if not isinstance(series, list) else series
        dic["series"] = [s["series"]["title"].replace("'", "’") for s in series]
        dic["position_in_series"] = [s["user_position"] for s in series]

    dic["goodreads_score"] = float(result["average_rating"])
    dic["goodreads_popularity"] = int(result["ratings_count"])
    return dic
```

Finally, I clean up the data with some hard-coded edits. To display an audiobook's information on a page, I added an
HTML template with Liquid tags called `audiobooks.html` to my `_includes` directory, which looks something like this:

{% raw %}
```html
<p class="audiobooks">
<img src="{{ book.image }}" width="40%" />
<h3><i>{{ book.title }}</i> by {{ book.authors }}</h3>
<ul>
    {% if book.series %}
        <li>
            {% if book.series.size == 1 %}
                <b>Series</b>: {{ book.series }} (part {{ book.position_in_series }})
            {% else %}
                <b>Series</b>:
                <ul>
                    {% assign n = book.series.size | minus: 1 %}
                    {% for i in (0..n) %}
                        <li>
                            {% if book.position_in_series[i] %}
                                {{ book.series[i] }} (part {{ book.position_in_series[i] }})
                            {% else %}
                                {{ book.series[i] }}
                            {% endif %}
                        </li>
                    {% endfor %}
                </ul>
            {% endif %}
        </li>
    {% endif %}
    <li>
        {% if book.narrators.size == 1 %}
            <b>Narrator</b>: {{ book.narrators }}
        {% else %}
            <b>Narrators</b>:
            <ul>
                {% for narrator in book.narrators %}
                    <li>
                        {{ narrator }}
                    </li>
                {% endfor %}
            </ul>
        {% endif %}
    </li>
    <li>
        <b>Running time</b>: {{ book.hours }}h {{ book.minutes }}m
    </li>
    <li>
        <b>Abridgement or dramatization</b>:
        {% if book.abridged %}
            Yes.
        {% else %}
            No.
        {% endif %}
    </li>
    <li>
        <b>Book review</b>: {{ book.book_review }} <b>{{ book.book }}/10.</b>
    </li>
    <li>
        <b>Performance review</b>: {{ book.performance_review }} <b>{{ book.performance }}/10.</b>
    </li>
</ul>
<hr>
```
{% endraw %}

{% assign counter=0 %}
{% for audiobook in site.data.audiobooks %}
  {% assign counter=counter | plus:1 %}
{% endfor %}

Using this schema, I can create numerous kinds of dynamically updated statistics and lists. For example, so far
I've listened to **{{ counter }}** audiobooks. That number was generated using the following snippet:

{% raw %}
```liquid
{% assign counter=0 %}
{% for audiobook in site.data.audiobooks %}
  {% assign counter=counter | plus:1 %}
{% endfor %}
```
{% endraw %}

I will probably add to and modify this method as my ideas about how to present my reviews develop over time. For now,
feel free to peruse [my favorite audiobooks](audiobooks-2), [least favorite audiobooks](audiobooks-3), or [just a
list of everything I've reviewed so far](audiobooks-4).