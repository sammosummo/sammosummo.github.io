---
layout: post
title: Getting started with Python for sound
date: 2019-02-13 
has_code: true
has_comments: true
revisions:
 - date: 2019-03-16
   reason: Reformatted code blocks
 - date: 2019-03-17
   reason: Added links to second post
---

This is the first post in a series about generating and playing sounds using the Python
programming language. The series will go slowly and cover several topics, including Python
best practices, psychoacoustics, and digital audio. My hope is that by the end, a reader
will able to perform sound synthesis with a firm basis in psychoacoustics using idiomatic
Python. To kick things off, I present my (highly opinionated) guide to getting started
with Python. I assume no prior knowledge, so readers already familiar with Python and its
core concepts—packages, environments, and so on—may wish to
[skip to the next post](playing-a-pure-tone-interactively),
which will actually get down to the business of making sounds.

## Get a GitHub account, fork the repository

My first piece of advice on getting started with Python doesn't involve Python at all.
[GitHub](https://github.com/) is an online service for hosting code, built on top of the
popular version control software (VCS) [Git](https://git-scm.com/). There are several
similar alternative services, including [BitBucket](https://bitbucket.org) and
[GitLab](https://about.gitlab.com), and the internet is replete with comparisons between
them. GitHub is simply the only one I have tried and I haven't found any reason to switch.

For this series of posts, I have created a public GitHub repository or _repo_ called
`klangfarbe`, the German word for timbre (literally, “sound color”). The German language
makes for an excellent generator for repository names, in my opinion. Head over to the
[GitHub website](https://github.com/), sign up for a free account and _fork_ (create your
own copy of) [this repo](https://github.com/sammosummo/klangfarbe). Since
[Microsoft acquired GitHub](https://www.msn.com/en-us/news/technology/microsoft-completes-github-acquisition/ar-BBOVVOT),
with a free account, users can create unlimited private repositories, so you can make
yours private, if you wish.

## Install Git (if not using a Mac)

In order to follow my recommendations later on, you’ll need [Git](https://git-scm.com/)
installed on your computer. Macs come with an old version of Git pre-installed, which you
may update if you wish. Personally, I find this version to work just fine. If you are
using Windows, however, you won’t have a pre-installed version so you’ll need to download
and install Git. I’m not sure whether Git comes with Linux; I assume it depends on your
distribution.

## Install conda and Python

Programming  languages are either _compiled_ or _interpreted_. [Python](https://www.python.org/)
is interpreted, meaning that it requires an _interpreter_ to execute the code. There are
many different ways to obtain a Python interpreter, but I strongly recommend using
[conda](https://conda.io/en/latest/).

Conda is software for managing installing and managing other software. It runs on Windows,
macOS and Linux. In my opinion, conda is currently the best way to install Python for
scientists and engineers. One of the primary advantages of conda over other approaches is
that it installs everything in your local directory by default. This means that you never
require administrator privileges, making it easy to use your own particular Python
instances on multi-user computers or remote servers. For example, I sometimes use a
relatively obscure Python package with numerous dependencies called 
[HDDM](http://ski.clps.brown.edu/hddm_docs/). Typically it is not feasible to install HDDM
on academic computing clusters using the Python interpreter(s) provided by the admins, so
instead I just install a local Python interpreter into my user directory via conda. A
potential disadvantage of conda is that it is maintained by a for-profit company called
[Anaconda, Inc.](https://www.anaconda.com/), which means there is a possibility for them
to change their business model in the future. 

The most direct way to get conda is to download and install [Miniconda](https://conda.io/miniconda.html),
a software bundle containing just conda and its dependencies. Alternatively, you can use
the "full-stack" [Anaconda distribution](https://www.anaconda.com/distribution/), which
includes conda, Python, [R](https://www.r-project.org/), over a thousand third-party
packages and their dependencies. I prefer Miniconda because I will probably never use the
majority of packages included in Anaconda, and those I do need can be installed easily
later.

If you are on a Mac, an alternative approach to obtaining a Python interpreter is
[Homebrew](https://docs.brew.sh/Homebrew-and-Python). Homebrew is a package manager
similar to conda. While I personally use Homebrew for other software, I don’t recommend
it for Python because installing Hombrew to begin with requires administrator privileges.

A third approach is to download and install Python [directly from the official website](https://www.python.org/downloads/).
This is fine but requires a little more work, since you’ll need to install at least one
extra thing, [pip](https://pypi.org/project/pip/), yourself. I’ll talk about pip again
later.

## Create a new environment

_Environments_—sometimes called _virtual environments_ or simply _envs_—are separate
instances of Python that are isolated from one another. You can modify Python within an
environment without influencing other environments. To return to my earlier example, some
time ago, HDDM only worked with
[out-of-date versions of NumPy](https://groups.google.com/forum/#!topic/hddm-users/pAj9eCLhIss).
My (temporary) solution to this problem was to create an environment with NumPy rolled
back to its earlier version. This allowed me to run my HDDM project within this
environment without screwing up my other projects, which relied on the latest version of
NumPy.

Python has multiple methods for creating environments; see
[here](https://realpython.com/python-virtual-environments-a-primer/) for a nice primer
describing some of them. However, because environment management is one of the primary
functions of conda, you should use this one, assuming you have followed my advice up to
now.

I like to create a new conda environment for each new project, and give it the same name
as its GitHub repository, in this case `klangfarbe`. Do this yourself by typing the
following command into a terminal.

```bash
conda create -n klangfarbe
```

While we are on the subject of terminals, I recommend Mac users consider
[iTerm](https://www.iterm2.com/) as a replacement for the built-in terminal tool. Windows
users, if you installed Mini/Anaconda with the default configuration options, you won’t be
able to access conda from the standard command prompt. Instead, you can use the
[Anaconda Prompt](https://docs.anaconda.com/anaconda/user-guide/getting-started/#write-a-python-program-using-anaconda-prompt-or-terminal)
utility. Alternatively, if for whatever reason you have a burning desire to run conda
from the command prompt, simply locate and execute `\Scripts\activate.bat`, which should
be somewhere in your Mini/Anaconda installation directory.

## Install NumPy

Conceivably, we could use nothing but the
[Python standard library](https://docs.python.org/3/library/) for sound synthesis and
playback, but this would require writing a huge amount of code. A better approach is to
take advantage of third-party packages to perform as much of the heavy lifting as
possible. For now, install one such package, [NumPy](http://www.numpy.org/). Others will
be installed later, as and when required.

NumPy is the foundational package for scientific Python, adding support for array-based
computation. Without NumPy, creating and manipulating sound waveforms would be tedious
and inefficient. Our code would be long and slow to run.

Conda can install packages into specific environments. The simplest way to do this is to
_activate_ the desired environment, then install the package without additional arguments:

```bash
conda activate klangfarbe
conda install numpy
```

If you have been following my recommendations up to this point, and are using Miniconda,
the above commands will install NumPy and all its dependencies for you. One of these
dependencies is the Python interpreter itself.  Therefore, the above might take a few
minutes to complete.

Conda packages are curated by the Anaconda team. This means that a particular package
might exist within the conda package repository, or that its latest version might not be
available. Fortunately, conda also installs
[pip](https://www.w3schools.com/python/python_pip.asp), Python’s de facto package manager,
by default. Conda and pip generally play well together. When it comes to installing a new
package, I recommend trying `conda install <packagename>` first, and if that fails, try
`pip install <packagename>`. You can also use either method to remove packages.

Depending on the package, a little playing around with conda and pip might be necessary.
For example, recently I wanted to use [PyQt5](https://pypi.org/project/PyQt5/), a set of
Python bindings for [Qt](https://www.qt.io/). While `conda install pyqt` installed the
packages successfully, many of Qt’s features were actually missing (`QtMultimedia`, for
instance). This was quickly remedied by installing a newer version of PyQt5 via
`pip install PyQt5`.

## Install PyCharm, clone the repository, configure

Serious coding is facilitated enormously by an integrated development environment (IDE).
Python ships with a bare-bones IDE called [IDLE](https://docs.python.org/3/library/idle.html),
which is OK for [hello-world](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program)ing
but is not suited to serious projects. [Spyder](https://www.spyder-ide.org/) is a popular
powerful IDE, but my favorite is [PyCharm](https://www.jetbrains.com/pycharm/). Like
conda, PyCharm is made by a for-profit company, although its community edition is free and
the professional edition can be obtained for free if you are in full-time education (you
just need a `.edu` email address).

PyCharm is awesome. It has highly sophisticated code introspection tools, a powerful
debugger, and
[tight integration with VCS, including Git](https://www.jetbrains.com/help/pycharm/version-control-integration.html).
I cannot emphasize strongly enough how convenient I find PyCharm’s Git integration. I
hate dealing with Git directly from the terminal and PyCharm allows me to eschew this.

The unit of PyCharm is called a _project_, which is really just a directory containing
your Python scripts. When you launch PyCharm for the first time, you will be presented
with the option to
[Checkout from Version Control](https://www.jetbrains.com/help/pycharm/set-up-a-git-repository.html).
Choose this, choose Git as your VCS—remember, Git must be installed for this to work!
Enter your GitHub credentials, and select your `klangfarbe` fork. PyCharm will then 
_clone_ (download a copy of) the repository, and the files will be visible within the
PyCharm window. 

Before running or writing any code, you should change PyCharm’s settings. Most
importantly, set the Python interpreter for the new project to be the `klangfarbe`
environment we created earlier. Now your repository, environment and project all have
identical names. After scanning your environment, PyCharm may recognize that there are
some missing dependencies based on the contents of `requirments.txt` and can attempt to
install them for you (another nice PyCharm feature!), but its easy enough to do this
yourself using conda and/or pip. Other settings I recommend but are entirely optional
include changing the right-hand margin in the text editor to 88 characters (this is the
value used by black, see later), using Google-style auto-completion for docstrings (again,
see later), enabling Pycharm to expand `main` into
[boilerplate](https://python-reference.readthedocs.io/en/latest/docs/boilerplate/), and
the darkula theme.

## Install Audacity (optional)

[Audacity](https://www.audacityteam.org/) has nothing to do with Python—it is software
for manipulating digital audio. This series won’t require Audacity, but it may be useful
for occasionally inspecting waveforms, spectrograms etc. of sounds you created. Audacity
is free, small (at least compared GarageBand or Audition) and easy to use.

## Learn Python!

The [Hitchiker’s Guide to Python](https://docs.python-guide.org/intro/learning/) provides
a comprehensive list of the best resources for learning Python. If you are completely new
to Python, you should go there and at the very least, work through
[one](https://thepythonguru.com/) [of](https://docs.python.org/3/tutorial/index.html)
[these](https://pythonbasics.org/) introductory tutorials. Since we’ll be using NumPy a
great deal in this series, you should also try a NumPy tutorial,
[such as this one](https://realpython.com/numpy-array-programming/).

I also recommend reading the entire
[Python glossary](https://docs.python.org/3/glossary.html) from start to finish. The
lion’s share of your Python knowledge will be learned while working on real projects and
fixing real issues in your code. I’m not exaggerating when I say that almost every coding
problem I have is solved by Googling it and finding that someone has posted almost the
exact same thing on [Stack Overflow](https://stackoverflow.com/questions/tagged/python).
Knowing how to describe a problem using the correct terminology is key to efficient
Googling/Stack Overflowing.

## Make your code “Pythonic”

In Python, there is usually a preferred or _Pythonic_ way of doing something. To quote
the [Zen of Python](There%20should%20be%20one%E2%80%94and%20preferably%20only%20one%E2%80%94obvious%20way%20to%20do%20it.),
“There should be one—and preferably only one—obvious way to do it.” This is worth keeping
in mind as you write your own code. For example, try to stick to the style rules laid out
in [Python Enhancement Proposal 8 (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
([see also here](https://realpython.com/python-pep8/)) and try to use
[Python idioms](https://en.wikibooks.org/wiki/Python_Programming/Idioms) wherever
possible.

Of course, time spent ensuring code is Pythonic could be spent writing more code. I try to
avoid wasting too much time on formatting and instead run all my scripts through
[black](https://black.readthedocs.io/en/stable/) after they’re done. Black can be
installed via pip, in your current environment if you wish.

Now code can be formatted directly from the terminal with `black <mysript.py>`
(or `black *.py` to run it on all Python scripts in the current directory).

## Write comprehensive documentation

Documenting your own code can feel like a chore but trust me, it is an incredibly
beneficial habit in the long run and you should try to cultivate it straight away. Force
yourself to document every script at the top level. Within each script, document all
functions and methods of all classes (even `__init__()`!). Consider adding a comment to
each line used to define an object unless it is absolutely 100% clear what the object
does and how it will be used. Pick a pre-existing documentation style and stick to
it—[Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
is my personal favorite, but
[NumPy style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html#example-numpy)
is good too.

## Make some sounds

Now that Python is installed and configured correctly, we can start to generate our first
sounds. [Continue to the next post](playing-a-pure-tone-interactively).
