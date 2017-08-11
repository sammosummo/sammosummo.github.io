---
layout: post
title: Staircases
---

In psychophysics, _staircases_ are experimental procedures that estimate a point
on the psychometric function by manipulating the dependent variable based on
the participant's response history. Many such procedures have been proposed, but
perhaps the most widely used staircase is the transformed up-down method (TUDM)
by Levitt (1971). Personally I prefer is Kaernbach's weighted up-down method
(WUDM), which I have used in some of my previous work (Mathias et al., 2010; 2011),
because it can estimate any point on the psychometric function—with the TUDM, one
is limited to a small number of values (50%, 70.9%, etc.)—and is slightly
more efficient (~10% better than the TUDM, according to Rammsayer, 1992).

# Mou

<!--- TOC-->
<!--{:toc}-->

<!--![Mou icon](http://mouapp.com/Mou_128.png)-->

## Overview

**Mou**, the missing Markdown editor for *web developers*.

Lorem ipsum dolor sit amet, has cu diam novum oblique, etiam regione bonorum ad per. Usu ignota assentior ut. Ex tollit eirmod mel. Ut cum quis velit, et vix inani eligendi gloriatur, ei accusam scaevola assueverit vel. Ex eum amet petentium interpretaris.

Propriae sententiae eam id, alia adipisci ne vis. Nusquam adversarium consectetuer ei usu, stet simul repudiandae sea te. Feugait minimum fastidii ea duo. Solet saepe cum et, eum adhuc dicta eu. An porro voluptaria eum, timeam expetendis dissentias eam cu, te regione tamquam lobortis his.

Urbanitas reprimique signiferumque ex vis. Id propriae gubergren vix. Bonorum fierent erroribus vim eu, mea sumo eligendi ad, an eam tacimates dissentiunt. Eu quaeque voluptaria mea, autem dicat omittantur no vis, sit prima animal reprehendunt eu. Natum melius meliore per at.

Ius minim assentior maiestatis cu, nam id veri civibus temporibus. Te his tation ocurreret scripserit, vim ei malis saepe eirmod. Ut sed vide luptatum reprehendunt, ei justo praesent inciderint qui. Ne per tale saepe accommodare, et aeque latine sea, vel timeam delicata at. Atqui principes cu duo, consulatu intellegat deterruisset ea ius, pro ut electram pertinacia.

Ei pro oblique perpetua. Scaevola oportere neglegentur at cum, quem harum decore eam eu. Ei case dicta est. Ex eam omnes partem habemus, sed falli delicata in. Te sea volumus omittam voluptatum.

Has ut saepe phaedrum. Te graeci nominati nam. Cu minimum invidunt referrentur usu, vocent accumsan appetere vel ea. Recteque scribentur no pro, ex qui sale sonet docendi. Error posidonium constituam ne has, vel justo urbanitas ex, no idque nostro dignissim quo. An idque tibique propriae per, te vix case ubique. Te omittantur dissentiunt neglegentur eam, an cum percipit complectitur.

Eu diam tritani principes vix, eos reque mundi at, sit et epicuri expetendis. Usu et posidonium intellegebat. Ad duo sumo sale noster. Ne sit aliquip feugiat efficiendi, an sea corpora dignissim eloquentiam.

Reque antiopam deseruisse quo et, vim id tritani appareat theophrastus. Ad repudiare sadipscing vix, vix ut nonumy vidisse consequat. Putant timeam feugiat cu usu, has ad harum ocurreret neglegentur. Dolorem pertinax et sea, gloriatur incorrupte ius ex. Sit dicta forensibus philosophia eu, usu porro expetenda id. Falli saepe ignota ius in.

Nec mucius mnesarchum an, duo cu idque veniam. Adhuc suscipiantur cu mea, atqui urbanitas eu usu. Sed reque philosophia at. Viderer signiferumque at cum.

Ut atqui diceret blandit duo, cibo recteque cum ex. Duis prima laudem at nec, no dicant utinam usu. Mea utamur indoctum principes cu, his ei atqui definiebas, praesent temporibus an sea. Nec ad eros prodesset scriptorem.

### Syntax

#### Strong and Emphasize

**strong** or __strong__ ( Cmd + B )

*emphasize* or _emphasize_ ( Cmd + I )

**Sometimes I want a lot of text to be bold.
Like, seriously, a _LOT_ of text**

#### Blockquotes

> Right angle brackets &gt; are used for block quotes.

#### Links and Email

An email <example@example.com> link.

Simple inline link <http://chenluois.com>, another inline link [Smaller](http://smallerapp.com), one more inline link with title [Resize](http://resizesafari.com "a Safari extension").

A [reference style][id] link. Input id, then anywhere in the doc, define the link with corresponding id:

[id]: http://mouapp.com "Markdown editor on Mac OS X"

Titles ( or called tool tips ) in the links are optional.

#### Images

An inline image ![Smaller icon](http://smallerapp.com/favicon.ico "Title here"), title is optional.

A ![Resize icon][2] reference style image.

[2]: http://resizesafari.com/favicon.ico "Title"

#### Inline code and Block code

Inline code are surround by `backtick` key. To create a block code:

  Indent each line by at least 1 tab, or 4 spaces.
    var Mou = exactlyTheAppIwant;

####  Ordered Lists

Ordered lists are created using "1." + Space:

1. Ordered list item
2. Ordered list item
3. Ordered list item

#### Unordered Lists

Unordered list are created using "*" + Space:

* Unordered list item
* Unordered list item
* Unordered list item

Or using "-" + Space:

- Unordered list item
- Unordered list item
- Unordered list item

#### Hard Linebreak

End a line with two or more spaces will create a hard linebreak, called `<br />` in HTML. ( Control + Return )
Above line ended with 2 spaces.

#### Horizontal Rules

Three or more asterisks or dashes:

***

---

- - - -

#### Headers

Setext-style:

This is H1
==========

This is H2
----------

atx-style:

# This is H1
## This is H2
### This is H3
#### This is H4
##### This is H5
###### This is H6

### Extra Syntax

#### Footnotes

Footnotes work mostly like reference-style links. A footnote is made of two things: a marker in the text that will become a superscript number; a footnote definition that will be placed in a list of footnotes at the end of the document. A footnote looks like this:

That's some text with a footnote.[^1]

[^1]: And that's the footnote.

#### Strikethrough

Wrap with 2 tilde characters:

~~Strikethrough~~

#### Fenced Code Blocks

Start with a line containing 3 or more backticks, and ends with the first line with the same number of backticks:

```
Fenced code blocks are like Stardard Markdown’s regular code
blocks, except that they’re not indented and instead rely on
a start and end fence lines to delimit the code block.
```

#### Tables

A simple table looks like this:

First Header | Second Header | Third Header
------------ | ------------- | ------------
Content Cell | Content Cell  | Content Cell
Content Cell | Content Cell  | Content Cell

If you wish, you can add a leading and tailing pipe to each line of the table:

| First Header | Second Header | Third Header |
| ------------ | ------------- | ------------ |
| Content Cell | Content Cell  | Content Cell |
| Content Cell | Content Cell  | Content Cell |

Specify alignement for each column by adding colons to separator lines:

First Header | Second Header | Third Header
:----------- | :-----------: | -----------:
Left         | Center        | Right
Left         | Center        | Right

<!-- Standard buttons -->
<a class="button" href="#">Anchor button</a>
<button>Button element</button>
<input type="submit" value="submit input">
<input type="button" value="button input">

<!-- Primary buttons -->
<a class="button button-primary" href="#">Anchor button</a>
<button class="button-primary">Button element</button>
<input class="button-primary" type="submit" value="submit input">
<input class="button-primary" type="button" value="button input">
