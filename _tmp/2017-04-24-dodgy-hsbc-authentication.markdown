---
layout: post
title:  "Dodgy HSBC Authentication"
date:   2017-04-24 12:00:00 +0100
time_to_read: 2
redirect_from: writing/dodgy-hsbc-authentication
---

I don't trust [HSBC](https://www.hsbc.co.uk/1/2/)'s method of authentication for their online banking website. Well, at least not one of them.

HSBC allows two forms of authentication. The first involves using a [keypad ](https://www.reddit.com/r/cryptography/comments/v3dsc/how_does_the_new_hsbc_internet_banking_security/) that hopefully provides similar security to [Google Authenticator](https://en.wikipedia.org/wiki/Google_Authenticator) or [Duo](https://duo.com/). This provides the highest level of privilege to your bank account and lets you pay new people.

The other form of authentication is the one I (and [others](https://www.reddit.com/r/AskNetsec/comments/2vta6k/explain_to_me_why_hsbcs_method_of_authentication/)) take issue with. HSBC lets users log onto their online banking (with fewer privileges) when they provide the answer to a memorable question and certain characters of their password. HSBC (and [others](https://www.tradeking.com/faq/whyuseanonscreenkeyboard)) do this in order to protect against key loggers.

<img src="/assets/imgs/hsbc-logon.png" alt="HSBC's Online Authentication Page" />

#### The problems ####
* Your password is not hashed and salted (the [industry standard](https://security.stackexchange.com/questions/51959/why-are-salted-hashes-more-secure-for-password-storage)).
* You cannot easily use a password manager.
* [Memorable](https://security.stackexchange.com/questions/121217/memorable-word-and-answers-to-security-questions-when-resetting-password) [questions](https://security.stackexchange.com/questions/4024/do-security-questions-subvert-passwords) and [answers](https://stackoverflow.com/questions/104592/whats-a-good-alternative-to-security-questions) are [bad](https://www.schneier.com/blog/archives/2005/02/the_curse_of_th.html). They are easy to guess (check my LinkedIn to determine my first employer) and if they are leaked, you cannot change them without lying (similarly to how you cannot change your fingerprint).
* It potentially reduces the strength of your password as attackers need only guess three characters (once they have your memorable answer).

#### The solution ####

Firstly, don't answer your secret questions correctly! Instead, get your password manager to generate a random string and use this as the answer to your secret questions. The real answers to most security questions (e.g. Who was your first employer?) are probably public knowledge and if not, they could have already been compromised.

Secondly, it is especially important not to reuse your HSBC password anywhere else. If HSBC experiences a password breach, your password might be recoverable (as it is not hashed) and attackers could access other accounts that use the same password.
