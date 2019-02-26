---
layout: post
title: "Intercepting Suspicious Chrome Extension Actions"
date:   2017-07-05 10:00:00 +0100
time_to_read: 4
redirect_from: writing/intercepting_suspicious_chrome_extension_actions
---

I just finished my masters project at [Imperial College London](http://www.imperial.ac.uk/)! I considered re-writing a shorter web version but honestly, I don't have the motivation yet. Maybe I'll get round to it one day but until then you can find my report and presentation here. Enjoy!

<img src="/assets/intercepting-suspicious-chrome-extension-actions/demo.gif" alt="Our modified browser intercepting suspicious extension actions">

### Abstract ###

Browser users have increasingly fallen victim to a variety of attacks carried out by malicious browser extensions. These extensions often have powerful privileges and can execute within the context of sensitive web-pages. Popular attacks include hijacking users' social media accounts, injecting or replacing advertisements and tracking users. Previous work to detect malice in extensions has not succeeded in providing adequate security guarantees about extensions running within browsers.

We present a novel extension security model that categorises certain actions as suspicious and prompts users to allow or prevent suspicious operations when executed by extensions. We propose minimal changes to the Chrome browser that implement this model and that provide guarantees that malicious extension actions cannot evade detection. In order to not inconvenience users, we build features that reduce the quantity of decisions that they are required to make.

We extensively evaluate our modified browser with regards to security guarantees, user interface, user understanding and performance overhead. Results demonstrate our browser's ability to intercept and stop malicious extension operations as they occur. However, our evaluation also suggests that users struggle with this responsibility and we find evidence of significant browser performance overheads.

### Open Access ###

My report, presentation and the implementation diff is freely available to anyone.

- <a href="{{ "/assets/intercepting-suspicious-chrome-extension-actions/report.pdf" | relative_url }}">report.pdf</a> (3.4 MB)
- <a href="{{ "/assets/intercepting-suspicious-chrome-extension-actions/presentation.pdf" | relative_url }}">presentation.pdf</a> (917 KB)
- <a href="{{ "/assets/intercepting-suspicious-chrome-extension-actions/patch.diff" | relative_url }}">patch.diff</a> (160 KB)
