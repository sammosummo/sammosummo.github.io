---
layout: default
title: test
---

## Heading h2

### Heading h3

#### Heading h4

This text is a paragraph.
This won't be another paragraph, it will join the line above it.

This will be another paragraph, as it has a blank line above it.

Text A
<!-- blank line -->
<br>
<!-- blank line -->
Text B

Text
<!-- blank line -->
----
<!-- blank line -->
Text

This is **bold** and this is _italic_.

[Text to display][identifier] will display a link.

[Another text][another-identifier] will do the same. Hover the mouse over it to see the title.

[This link] will do the same as well. It works as the identifier itself.

[This link][] (same as above), has a second pair of empty brakets to indicate that the following parenthesis does not contain a link.

<https://example.com> works too. Must be used for explicit links.

<!-- Identifiers, in alphabetical order -->

[another-identifier]: https://example.com "This example has a title"
[identifier]: http://example1.com
[this link]: http://example2.com

Paragraph:

1. Item one
   1. Sub item one
   2. Sub item two
   3. Sub item three
2. Item two

Paragraph:

1. Item one
   1. Sub item one
   1. Sub item two
1. Item two
1. Item three

Paragraph:

- Item 1
- Item 2
- Item 3
   - Sub item 1
   - Sub item 2
- Item 4

- list one - item 1
- list one - item 2
   - sub item 1
   - sub item 2
- list one - item 3
^
- list two - item A
- list two - item A
^
- list three - item _i_
- list three - item _ii_

[![An awesome example image](/images/path/to/folder/image.png "Hello World")*My caption*][about.gitlab.com]

<!-- blank line -->
<figure class="video_container">
  <iframe src="https://www.youtube.com/embed/enMumwvLAug" frameborder="0" allowfullscreen="true"> </iframe>
</figure>
<!-- blank line -->

- TOC
{:toc}