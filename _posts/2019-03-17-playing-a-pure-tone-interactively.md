---
layout: post
title: Playing a tone interactively using Python
date: 2019-03-17 
has_code: true
has_comments: true
tags:
 - Python
 - sound
revisions:
 - date: 2019-03-24
   reason: Added links to third post
---

This is the second post in a series about using Python to generate and play sounds.
Here, I describe how to play a pure tone interactively from the terminal. This is super
basic stuff. As I wrote in the [first post](getting-started-with-python-for-sound), I
want to go slowly and not to assume any prior knowledge of either Python or sound
synthesis. I do assume, however, that you read and followed the recommendations in my
first post. In particular, I assume that you installed conda and created a new conda
environment called `klangfarbe`. If you didn’t do those things, the code examples below
might not work exactly as described.

Before running any of these commands, make sure that the volume on your computer is set
**very low**, especially if you are using headphones!

## Install sounddevice

Windows users should open their
[Anaconda prompt](https://docs.anaconda.com/anaconda/user-guide/getting-started/#write-a-python-program-using-anaconda-prompt-or-terminal),
and macOS or linux users should open a terminal or terminal emulator (I recommend
[iTerm2](https://www.iterm2.com/) for Mac users). Then activate the `klangfarbe`
environment using the following command:
```bash
conda activate klangfarbe
```

Presumably you already installed NumPy into this environment. (If not, type
`conda install numpy`). Now we are going to install another third-party package called
[sounddevice](https://python-sounddevice.readthedocs.io/en/0.3.13/). This package
provides bindings for [PortAudio](http://www.portaudio.com/), a cross-platform audio
library, and a few convenience functions to play and record NumPy arrays. We will use
sounddevice to deliver NumPy arrays to the computer’s audio output. There are numerous
Python packages with similar functionality, such as
[simpleaudio](https://simpleaudio.readthedocs.io/en/latest/), [Qt](https://www.qt.io/),
and [pygame](https://www.pygame.org/news). I have experimented extensively with all of
these packages on different computers and operating systems, and for numerous reasons
that I won’t go into here, sounddevice is the one I recommend for most users. (I’ll
write a detailed comparison of these in a future post). Install sounddevice using the
following command:
```bash
pip install sounddevice
```

## Python interactive session

In the same window, simply type
```bash
python
```

This will launch a Python interactive session. Take a look at the three or four lines
that appear just above the Python prompt (`>>>`). In my case, they were
```
(klangfarbe) Samuels-MacBook-Air:~ smathias$ python
Python 3.7.2 (default, Dec 29 2018, 00:00:04)
[Clang 4.0.1 (tags/RELEASE_401/final)] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
```

These lines contain the words `Anaconda` and `klangfarbe`, so I know I’m running the
correct Python distribution within the correct environment. If in your case it says
something different—perhaps
`[GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.0.42)] on darwin`, for instance—
the rest of the commands in this post might not work correctly because the particular
distribution or environment might not contain the required packages.

## Import

Third-party Python packages are not immediately accessible. Type the following lines
into your terminal (which is now running an interactive Python session) to import the
two packages we need:
```python
import numpy as np
import sounddevice as sd
```

There are several ways to use the `import` statement. It can import whole packages
(`import pkg`, `import pkg as pk`, or `from pkg import *`), subpackages modules, or
specific objects (`from pkg.subpkg.mod import func`). The configuration
`import pkg as pk` imports the package `pkg` into the *namespace* `pk`. This is
preferable over `import pkg`, which imports into the longer namespace, because it
saves keystrokes in the long run. It is also preferable over `from pkg import *`,
which imports the package into the current namespace, potentially causing numerous
problems (see
[here](https://stackoverflow.com/questions/2360724/what-exactly-does-import-import)).

## Generate a pure tone

_Pure tones_ are arguably the simplest sounds that exist. They are also used as building
blocks in the synthesis of other sounds. I’ll talk more about pure tones in the future
posts. For now, we’ll simply create one of them with a single line of code.
```python
tone = np.sin(2 * np.pi * 440 * np.arange(0, 1, 1/44100))
```

Don’t worry too much about what this line actually does right now—I’ll explain
everything thoroughly in the future.

## Play the tone

Sounddevice makes it extremely easy to play NumPy arrays:
```python
sd.play(tone, 44100)
```

Upon execution of that last line, you should hear a tone. You should also notice that
as soon you as execute this line, it returns a fresh prompt (`>>>`). This is because
playback was _aysnchronous_, meaning that Python continued to process further commands
while the tone continued to play in the background. You can block Python from performing
any other actions until the sound has finished playing like this:
```python
sd.play(tone, 44100); sd.wait()
```

This second time, you should hear the same tone but the prompt will not appear until the
sound is over.

The meanings of the functions `sd.play()` and `sd.wait()` are obvious from their names.
It is also clear that the first argument we passed to `sd.play()` was the NumPy array we
wished to play. But what is the meaning of the second argument we passed to this
function, the integer `44100`? It is the _sample rate_, how many times per second the
waveform is evaluated. We will talk about sample rates again in the next post.

## As a script

Below is a script that will play the same tone when executed.

<script src="https://gist.github.com/sammosummo/ea1b006d1541c4f26ed6d554433d9c96.js"></script>

The script is also available in the [`klangfarbe` GitHub repository](https://github.com/sammosummo/klangfarbe/blob/master/play_tone.py).
If you followed my advice from the [first post](getting-started-with-python-for-sound)
in this series and cloned this repository, you can update it and the file will appear on
your computer.

## Next steps

We’ve played our first sound using Python. As I wrote at the beginning, this was basic
stuff. In the [next post](pure-tones), we will go a tiny bit deeper by considering the
pure tone in more detail.