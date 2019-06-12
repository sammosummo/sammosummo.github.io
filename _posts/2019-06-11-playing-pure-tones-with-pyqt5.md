---
layout: post
title: Playing pure tones with PyQt5
date: 2019-06-11
has_code: true
has_comments: true
---

In an [earlier post](getting-started-with-python-for-sound), I recommended using a third-party package called [sounddevice](https://python-sounddevice.readthedocs.io/en/latest/) for playing sounds with Python. I also mentioned that there were some alternatives with similar functions. Overall, I still recommend sounddevice because I find it to be the most straitforward to use and the easiest to install on macOS, Windows, and Linux. However, [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5) is an alternative certainly worth looking at. PyQt5 provides bindings for [Qt](https://www.qt.io/), software for building complete applications with graphical user interfaces (GUIs). So if you are interested in building a Python app with an audio component, PyQt5 seems like a smart choice.

Unfortunately, I’ve really struggled to use PyQt5’s built-in audio features effectively. Latency issues, clicking, and clipping can be difficult to avoid. This is much to my own chagrin: I use PyQt5 _all the time_ for building psychological experiments, so relying on an extra pacakge for sound playback when this is included within PyQt5 is infuriating. I think a major problem is that there aren’t enough working examples online. I guess people don't use PyQt5 for audio as often as other tasks. In this post, I decided to try to rectify the balance in a small way, by taking an [already existing script](https://wiki.python.org/moin/PyQt/Playing%20a%20sound%20with%20QtMultimedia) and fixing some of its problems. By the end, we will have a Python script that creates a GUI from which the user can play pure tones of different frequencies and levels.

## Setup

This example is included in my [`klangfarbe` GitHub repo](https://github.com/sammosummo/klangfarbe/tree/master). If you decide to clone it, I recommend setting up a conda Python environment of the same name, as per my [getting-started post](getting-started-with-python-for-sound). You will need to install PyQt5 within this environment. Please note that, at the time of writing, the conda version of PyQt5 does not include all the necessary sub-components to play sounds. Therefore, you should install it via `pip install PyQt5` instead.

## Original code

Its very likely that the original webpage will outlive _The Cracked Bassoon_, but nevertheless, here is the example script:

```python
from math import pi, sin
import struct, sys

from PyQt4.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PyQt4.QtGui import QApplication, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QSlider, QVBoxLayout, QWidget
from PyQt4.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput

class Window(QWidget):

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        format = QAudioFormat()
        format.setChannels(1)
        format.setFrequency(22050)
        format.setSampleSize(16)
        format.setCodec("audio/pcm")
        format.setByteOrder(QAudioFormat.LittleEndian)
        format.setSampleType(QAudioFormat.SignedInt)
        self.output = QAudioOutput(format, self)
        
        self.frequency = 440
        self.volume = 0
        self.buffer = QBuffer()
        self.data = QByteArray()
        
        self.deviceLineEdit = QLineEdit()
        self.deviceLineEdit.setReadOnly(True)
        self.deviceLineEdit.setText(QAudioDeviceInfo.defaultOutputDevice().deviceName())
        
        self.pitchSlider = QSlider(Qt.Horizontal)
        self.pitchSlider.setMaximum(100)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setMaximum(32767)
        self.volumeSlider.setPageStep(1024)
        
        self.playButton = QPushButton(self.tr("&Play"))
        
        self.pitchSlider.valueChanged.connect(self.changeFrequency)
        self.volumeSlider.valueChanged.connect(self.changeVolume)
        self.playButton.clicked.connect(self.play)
        
        formLayout = QFormLayout()
        formLayout.addRow(self.tr("Device:"), self.deviceLineEdit)
        formLayout.addRow(self.tr("P&itch:"), self.pitchSlider)
        formLayout.addRow(self.tr("&Volume:"), self.volumeSlider)
        
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addStretch()
        
        horizontalLayout = QHBoxLayout(self)
        horizontalLayout.addLayout(formLayout)
        horizontalLayout.addLayout(buttonLayout)
    
    def changeFrequency(self, value):
    
        self.frequency = 440 + (value * 2)
    
    def play(self):
    
        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
        
        if self.buffer.isOpen():
            self.buffer.close()
        
        self.createData()
        
        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        
        self.output.start(self.buffer)
    
    def changeVolume(self, value):
    
        self.volume = value
    
    def createData(self):
    
        # Create 2 seconds of data with 22050 samples per second, each sample
        # being 16 bits (2 bytes).
        
        self.data.clear()
        for i in xrange(2 * 22050):
            t = i / 22050.0
            value = int(self.volume * sin(2 * pi * self.frequency * t))
            self.data.append(struct.pack("<h", value))


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
```

## PyQt4 → PyQt5

The first issue with this example is that it was written for PyQt4, not PyQt5, so we need to change the `import` statements. 

```python
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PyQt5.QtWidgets import QApplication, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QSlider, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput
```

Note that in addition to changing the imported base package, the `QtGui` sub-package is now called `QtWidgets`.

A couple of methods in `QAudioFormat` have also been renamed. Lines 17–18 should read,

```python
        format.setChannelCount(1)
        format.setSampleRate(22050)
```


Because the `xrange` function was renamed `range` in Python 3, we also need to modify line 89:

```python
for i in range(2 * 22050):
```

## Play a tone

Now you should be able to run this script. When you do, and see something like this:

![](/assets/images/pyqt5_puretone_gui.png)
*This is what the GUI looks like on my mac.*

First, drag the Volume slider up a bit, then press the Play button. Did you hear something. Yes? Great!

## Playing more than once

Now click it again. Oh …

Let’s do a little debugging to figure out why this script only plays a single tone. I’ve added two `print` calls to the `play` method,

```python
    def play(self):

        print("about to play:", self.output.state(), self.output.error())

        if self.output.state() == QAudio.ActiveState:
            self.output.stop()

        if self.buffer.isOpen():
            self.buffer.close()

        self.createData()

        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)

        self.output.start(self.buffer)

        print("played:", self.output.state(), self.output.error())
```

When we rerun the script and press the Play button twice, we see the following:

```
about to play: 2 0
played: 0 0
about to play: 3 3
played: 2 1
```

The first integer on each line is the output of `self.output.state()`. From the [docs](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtmultimedia/qaudio.html#State), it returns various status codes. Initially the status is 2 (stopped), then immediately after the tone starts to play it changes to 0 (active). Some time before we press Play again, it changes to 3 (idle), which means it “has no data and [the] buffer is empty, this state is set after start() is called and while no audio data is available to be processed.” This all makes sense. I’m still not clear on why it changes back to 2 after we pressed Play a second time, but whatever.

The second integer per line is the output of `self.output.error()` (see the [docs](https://www.riverbankcomputing.com/static/Docs/PyQt5/api/qtmultimedia/qaudio.html#Error)). No errors were raised when playing the first tone. But sometime after that—I assume when the first tone finished playing and the status of the output changed to idle—we got an `UnderrunError`, which means “audio data is not being fed to the audio device at a fast enough rate.” Finally, we got an `IOError` when we pressed Play again, which makes sense because the output device was closed.

You might think that pressing Play for a third time would actually play a tone, because the status out the output has reverted to 2. But it doesn’t, presumably because of the errors.

There is probably a correct way to close the output after the sound has ended that prevents it producing an `UnderrunError` in the first place, but at the time of writing, I’m still not sure what this is. However, another way get the code to play a tone each time we press Play is to check for the error and reset the output if one is found, like so (added to lines 70–71):

```python
if self.output.error() == QAudio.UnderrunError:
    self.output.reset()
```

Now we can hear as many tones as we like. Hooray!

## Latency issues

You might have noticed a lag between pressing the button and hearing the sound, particularly if you have a slower computer. Let’s measure it. We start by importing the `time` module from the Python standard library (line 8),

```python
import time
```

Then we modify the `play` method for a second time:

```python
    def play(self):

        now = time.time()
        print("about to play:", self.output.state(), self.output.error())

        if self.output.state() == QAudio.ActiveState:
            self.output.stop()

        if self.buffer.isOpen():
            self.buffer.close()

        if self.output.error() == QAudio.UnderrunError:
            self.output.reset()

        self.createData()

        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)

        self.output.start(self.buffer)

        print("played:", self.output.state(), self.output.error())
        t = round((time.time() - now) * 1000)
        print(f"this took {t} milliseconds") 
```

Running the script and pressing Play a few times produces

```
about to play: 2 0
played: 0 0
this took 53 milliseconds
about to play: 3 3
played: 0 0
this took 46 milliseconds
about to play: 3 3
played: 0 0
this took 45 milliseconds
```

Fifty milliseconds is _horrendous_ latency. We can re-write the `play` method again to isolate the culprit.

```python
    def play(self):

        now = time.time()
        print("about to play:", self.output.state(), self.output.error())

        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
            t = round((time.time() - now) * 1000)
            print(f"stopping a playing tone took {t} milliseconds")

        if self.buffer.isOpen():
            self.buffer.close()
            t = round((time.time() - now) * 1000)
            print(f"closing an open buffer took {t} milliseconds")

        if self.output.error() == QAudio.UnderrunError:
            self.output.reset()
            t = round((time.time() - now) * 1000)
            print(f"resetting broken output took {t} milliseconds")

        self.createData()
        t = round((time.time() - now) * 1000)
        print(f"writing the waveform took {t} milliseconds")

        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        t = round((time.time() - now) * 1000)
        print(f"writing the buffer took {t} milliseconds")

        self.output.start(self.buffer)

        print("played:", self.output.state(), self.output.error())
        t = round((time.time() - now) * 1000)
        print(f"playing took {t} milliseconds")
```

```
about to play: 2 0
writing the waveform took 43 milliseconds
writing the buffer took 43 milliseconds
played: 0 0
playing took 60 milliseconds
about to play: 3 3
closing an open buffer took 0 milliseconds
resetting broken output took 0 milliseconds
writing the waveform took 43 milliseconds
writing the buffer took 43 milliseconds
played: 0 0
playing took 43 milliseconds
about to play: 3 3
closing an open buffer took 0 milliseconds
resetting broken output took 0 milliseconds
writing the waveform took 42 milliseconds
writing the buffer took 42 milliseconds
played: 0 0
playing took 42 milliseconds
```

Clearly,  it’s re-writing the waveform on each `play` call that’s causing the lion’s share of the lag. We could speed this up by replacing `createData` with a method that uses NumPy, as described in my previous posts. But we could also simply move this call out of the `play` method. Now the relevant portion of the code looks like this:

```python
    def changeFrequency(self, value):

        self.frequency = 440 + (value * 2)
        self.createData()

    def play(self):

        now = time.time()
        print("about to play:", self.output.state(), self.output.error())

        if self.output.state() == QAudio.ActiveState:
            self.output.stop()
            t = round((time.time() - now) * 1000)
            print(f"stopping a playing tone took {t} milliseconds")

        if self.buffer.isOpen():
            self.buffer.close()
            t = round((time.time() - now) * 1000)
            print(f"closing an open buffer took {t} milliseconds")

        if self.output.error() == QAudio.UnderrunError:
            self.output.reset()
            t = round((time.time() - now) * 1000)
            print(f"resetting broken output took {t} milliseconds")

        self.buffer.setData(self.data)
        self.buffer.open(QIODevice.ReadOnly)
        self.buffer.seek(0)
        t = round((time.time() - now) * 1000)
        print(f"writing the buffer took {t} milliseconds")

        self.output.start(self.buffer)

        print("played:", self.output.state(), self.output.error())
        t = round((time.time() - now) * 1000)
        print(f"playing took {t} milliseconds")

    def changeVolume(self, value):

        self.volume = value
        self.createData()
```

For safety, I’ve also added a call to `createData` to the `__init__` method. Now we get something like the following:

```
about to play: 2 0
writing the buffer took 0 milliseconds
played: 0 0
playing took 8 milliseconds
about to play: 3 3
closing an open buffer took 0 milliseconds
resetting broken output took 0 milliseconds
writing the buffer took 0 milliseconds
played: 0 0
playing took 0 milliseconds
```

This modification actually makes the code much less efficient because it re-writes the waveform every time either slider moves, rather than only when it actually needs to play another waveform. But it did eliminate (most of) the lag.

## Poor latency on initial play

Latencies are much better for the second play onwards,  but the first one is still poor. I have not figured out the source of this, and I find it annoying as all hell. My hacky workaround is to add a call to `play` during the `__init__` method.  Thus, upon initialization, the object plays an empty buffer, which eats up the initial lag. Again, this is inefficient, but it’s the best I could come up with.

## Final code

Now we have a short, simple script that plays tones with sub-millisecond latencies. This might be sufficient for some purposes, such as certain behavioral psychological experiments. The complete code, tidied up and with comments and `print` calls removed, is provided as a Gist below. It’s also included in [my repo](https://github.com/sammosummo/klangfarbe/tree/master).

<script src="https://gist.github.com/sammosummo/0b85e27d6ff02bbf8809dab24be5158b.js"></script>

To be clear, this is not good code! The latency is below 1 millisecond but this is still not great. It wouldn’t work in circumstances where timing is absolutely critical, such as in a electrophysiology experiment, and I hate the play-silence-during-init hack. If anyone reading this has any suggestions for further improvements, please feel free to leave a comment below.