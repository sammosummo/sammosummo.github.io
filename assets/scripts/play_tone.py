"""Simply generates a pure tone using numpy and plays it via sounddevice.

As always, make sure your volume settings are low before running this script, especially
if you are using headphones!

"""
import numpy as np
import sounddevice as sd

if __name__ == "__main__":
    tone = np.sin(2 * np.pi * 440 * np.arange(0, 1, 1 / 44100))  # generate the tone
    sd.play(tone, 44100)  # play it
    sd.wait()  # wait for the tone to finish
