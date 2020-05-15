---
date: 2020-04-05
has_code: true
has_comments: true
layout: post
short_title: Audiobooks I
tags:
- books
title: My journey into audiobooks
---

I love fiction, but I'm a very slow reader. I'm 35 now, and I've read about 50 books in my
life, which is pretty terrible: if I'd read the same number per year as the average person
([which is 12, apparently](https://irisreading.com/how-many-books-does-the-average-person-read/)),
I should be well past 200 by now.

My wife—a prolific reader herself [with a blog on the topic](https://emmablogsbooks.com)—suggested
I try audiobooks. In March of 2019 I discovered [Libby](https://www.overdrive.com/apps/libby/),
and it has completely transformed how I consume literature. Now, just over a year and almost
100 audiobooks later, I decided to compile some thoughts on the topic and review everything
I've heard. This post goes covers [how I acquire audiobooks](#acquisition), [what I like](#taste),
and provides geeky details of how I compiled [a dynamic
ordered list of my reviews](#code). If you don't care about any of this and just want
some recommendations, I suggesting jumping to my next post, which [lists my favorites](audiobooks-2).

## Where I get them<a name="acquisition"></a>

About 90% of my audiobooks come from [Libby](https://www.overdrive.com/apps/libby/). Libby
is a free mobile app from [Overdrive](https://company.overdrive.com/?_ga=2.215002079.990475370.1586801728-e87a6c4b-3216-4681-8f15-ed356a1f4f29),
that connects to many local libraries across the USA. If you're a member of one or more of
these libraries ([see here for a list](https://www.overdrive.com/libraries)), you can use
it will deliver loans straight to your e-reader, phone or other device, for free.
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
their newsletter so that you don't miss offers. When I first signed up, there was a sale on
fantasy novels; I picked up a ton of them for considerably less than the cost of credits.
Audible's no-questions-asked return policy is a big plus. Also, since my wife is part of
my [Amazon Household](https://www.amazon.com/myh/households), I'm able to take advantage of
[Whispersync](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000827761) to get books
she's already read and recommends at a reduced price.

There are numerous other paid audiobook services. I haven't tried any others yet because I
haven't encountered any instances where an audiobook was cheaper elsewhere. Some of these
other services are more supportive of independent booksellers and I suppose I should use them
instead of an Amazon company, especially considering how Amazon are treating
their employees during this current time of crisis. If anyone has recommendations, feel
free to leave a comment at the end of this post.

## When to request and borrow

The major limitation of borrowing audiobooks is that you generally can't listen to what you
want when you want. There's just no way around the fact that hold times for popular books
tend to be long. One of the first books I tried to borrow was *The Blind Assassin* and I'm
still on hold, over a year later!

Using Libby requires a bit of planning and a lot of patience. Becoming a member of multiple
libraries helps a lot (see above). I tend to spam holds, placing them on everything I'm even
vaguely interested in, until I'm maxed out. I request the same book at multiple libraries.

I also try to be nice to other borrowers. When a book is ready to be borrowed, I decide
whether I really want it, and whether I can realistically finish it, before borrowing. I
never have more than one copy of a book at a time, returning the copy with the shorter shelf
time. I'm aggressive in returning books I'm not enjoying. (What's the point of powering through
when I could be listening to something better? And if I change my mind, I'll just request it
again later). I return a book as soon as I'm done, obviously.

## Listening speed

There's no way I could listen to so many audiobooks at their natural speed. I usually listen
to somewhere between 2.5 and 3 times speed, depending on the narrator and writing. If find
myself ramping up gradually throughout a performance, especially if I'm listening to books
from the same series back-to-back, since these usually have the same narrator(s).

My friends and family are incredulous about this and insist I must be constantly missing
plots details and nuances in the performances. All I can say is that I'm enjoying myself
just as much as during any book I've read or movie I've seen.

I get through books pretty quickly. I listen any time I'm doing something repetitious and
nonverbal, such as walking the dog, laundry, and the daily commute. I'm able to finish a
novella in a day, which puts me roughly on par with my wife's book-reading.

## What I like <a name="taste"></a>

I'm a man in his late thirties with a background in science, so yes, I listen to a lot of
sci fi and fantasy, although I try to be open to new styles and genres. I really like
grim, grotesque, and surreal; my favorite things are those that go right up to the edge of
enjoyable. (I feel like this about music and films as well.) I really dislike YA. I can't
put my finger on why and I'm really trying not to be a snob or pretentious about it.
Perhaps one day I'll discover something really excellent in that genre.

## My reviewing system<a name="code"></a>

I'm a quantitative scientist, so naturally I turned my reviews into a coding project.

This website is built using [Jekyll](https://jekyllrb.com/), which is capable of processing
data stored in [YAML](https://yaml.org/) via [Liquid](https://shopify.github.io/liquid/). Each time I finish an audiobook, I add my review
to a data file called `audiobooks.yaml`. A typical entry looks like this:

```yaml
  - title: The Heart Goes Last
    author: Margaret Atwood
    narrator: [Cassandra Campbell, Mark Deakins]
    image: https://m.media-amazon.com/images/I/51qLjWpd7XL._SL500_.jpg
    book: 7
    performance: 8
    review: >-
      More farcical than Atwood's other dystopian fiction. Much preferred it over <i>Oryx and Crake</i> and its sequels.
      Performances are splendid.
    finished: y
    goodreads: "24388326"
    tags: [female-writer, dystopian, soft-sci-fi, multiple-narrators]
```

Notice that I'm storing a lot of extra information here, which will allow me to create
numerous kinds of dynamically updated lists and statistics in the future. So far I've made
a [simple list of every audiobook I've finished, ordered by score](audiobooks-2) and a
my [favorite audiobooks of all time](audiobooks-3), my [favorite audiobooks of all time](audiobooks-3)


keep posts dynamically updated, count how many books
I've listened to, plot my scores, and so on. As time goes on and I acquire more data, I plan
to make nice figures of scores as a function or author and narrator.

## My reviews

Find out my favorite audiobooks[the best](audiobooks-2), [the worst](audiobooks-4), and [all the ones in
between](audiobooks-3). Here's a [dispassionate list for quick reference](audiobooks-5).

hell0!

{% for book in site.data.audiobooks %}
{% include audiobook.html %}
{% endfor %}