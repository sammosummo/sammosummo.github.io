"""Contains a function to generate pure tones.

"""
import numpy as np
import sounddevice as sd

a0 = 1e-5  # reference amplitude
sr = 44100  # sample rate


def sinusoid(d, f, phi, l, a0=a0, sr=sr):
    """Generates a pure tone.

    A pure tone or sinusoid is a periodic waveform that is some variation on the sine
    wave.

    Args:
        d (float): Duration in s.
        f (float): Ordinary in Hz.
        phi (float): Starting phase in rad.
        l (float): Level in dB.
        a0 (:obj:`float`, optional): Amplitude of a 0-dB tone. Default is 1e-5.
        sr (:obj:`int`, optional): Sample rate in Hz. Default is 44100.

    Returns:
        waveform (np.ndarray): Sinusoidal waveform.

    """
    t = np.arange(0, int(round(d * sr))) / sr
    return a0 * 10 ** (l / 20) * np.sin(2 * np.pi * f * t + phi)


if __name__ == "__main__":

    tone = sinusoid(1, 1000, 0, 60)
    sd.play(tone, 44100)
    sd.wait()
